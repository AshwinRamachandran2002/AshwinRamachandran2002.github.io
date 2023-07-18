#!/usr/bin/env python
from eva import EvaProgram, Input, Output, evaluate
from eva import evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
from random import uniform
import numpy as np
import unittest
import math
import time


def linear(x, y):
    return np.matmul(x, y)


def generate_inputs(N, K):
    inputs = dict()
    inputs_np = np.zeros((N, K))
    i = 0
    for n in range(N):
        for k in range(K):
            inputs[f"x_{n}_{k}"] = [i]
            inputs_np[n, k] = i
            i += 1
    return inputs, inputs_np


def generate_weights(K, M):
    inputs = dict()
    inputs_np = np.zeros((K, M))
    i = 0
    for k in range(K):
        for m in range(M):
            inputs[f"w_{k}_{m}"] = [i]
            inputs_np[k, m] = i
            i += 1
    return inputs, inputs_np


def generate_matmul(N, K, M):
    gemm = EvaProgram("gemm", vec_size=1)
    with gemm:
        a = np.array([Input(f"x_{n}_{k}") for n in range(N) for k in range(K)]).reshape(
            N, K
        )
        b = np.array([Input(f"w_{k}_{m}") for k in range(K) for m in range(M)]).reshape(
            K, M
        )

        out = linear(a, b)

        for n in range(out.shape[0]):
            for m in range(out.shape[1]):
                Output(f"y_{n}_{m}", out[n][m])

    gemm.set_input_scales(32)
    gemm.set_output_ranges(32)
    return gemm


def benchmark_matmul(N, K, M):
    inputs, inputs_np = generate_inputs(N, K)
    weights, weights_np = generate_weights(K, M)

    matmul = generate_matmul(N, K, M)

    data = {**weights, **inputs}
    compiler = CKKSCompiler(config={"security_level": "128", "warn_vec_size": "false"})
    compiled, params, signature = compiler.compile(matmul)
    public_ctx, secret_ctx = generate_keys(params)
    enc_inputs = public_ctx.encrypt(data, signature)
    start = time.time()
    enc_outputs = public_ctx.execute(compiled, enc_inputs)
    end = time.time()
    run_time = end - start

    outputs = secret_ctx.decrypt(enc_outputs, signature)

    y = np.array([outputs[f"y_{n}_{m}"] for n in range(N) for m in range(M)]).reshape(
        N, M
    )

    start = time.time()
    true_y = linear(inputs_np, weights_np)
    end = time.time()
    plain_run_time = end - start

    correct = np.allclose(y, true_y)
    if not correct:
        raise ValueError(f"We were wrong for size {N}")
    return run_time, plain_run_time


if __name__ == "__main__":
    results_cipher = dict()
    results_plain = dict()
    for size in [4, 8, 16, 32]:
        N, K, M = size, size, size
        time_cipher, time_plain = benchmark_matmul(N, K, M)
        results_cipher[f"{N}_{K}_{M}"] = time_cipher
        results_plain[f"{N}_{K}_{M}"] = time_plain
        print(results_cipher)
        print(results_plain)
        print()
