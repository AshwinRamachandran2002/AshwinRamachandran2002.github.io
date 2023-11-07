---
layout: post
title:  "A Mini Project: A Third Party Service to Preserve Privacy in User Prompts to LLMs"
description: 
date:   2023-06-05 08:24:51 +0200
`---

## Introduction
This post explores a system which could be used as a third party service to preserve privacy in user prompts to LLMs. The service would require a database of prompts that users could ask the LLM, and then an encrypted input from the user. The service would approximate the most similar prompt from the database and then send it to the LLM. A future version of the service could also be used to generate prompts without the need for a database, by reconstructing the embeddings using the same principle as cosine similarity.

## Text Embedding Similarity with Homomorphic Encryption
The CKKS is a Homomorphic Encryption scheme that can be used to perform computations on encrypted data. CipherText is the encrypted data and PlainText is the unencrypted data. The CKKS scheme allows us to perform operations between CipherText and PlainText. The operations are performed on the CipherText and the result is a CipherText. The CipherText can then be decrypted to obtain the result.
It has the ability to perform the operations:

1. Add(ct1, ct2)
2. Mult(ct1, ct2)
3. Bootstrap(ct1)

# Approximating the Cosine Similarity function
In order to achieve our goal, we should be able to perform cosine similarity in the encrypted space. The cosine similarity function is defined as:

```
cos(Theta) = u.v / (||u|| ||v||)
           = (u1v1 + u2v2 ...) / (sqroot((u1^2 + u2^2) x (v1^2 + v2^2))
```
 

# Approximation of the Square Root Inverse:
Square root oepration is not possible in the HME space, hence we use the below approximation

Derivation: 

```
Have an initialisation value y0 = 1, f(y) = (1/y)^2 - x
y_(n+1) = y_n - ((1/y_n)^2 - x) / (-2/y_n^3)
y_(n+1) = y_n + (1/2)(y_n - x * y_n^3)
y_(n+1) = (1/2)(3 * y_n - x * y_n^3)
y_(n+1) = (1/2) * y_n * (3 - x*y_n^2)
```

Hence we obtain a y' such that y' ~ 1/root(x), given an x

# Procedure
The user input embeddings as recieved a encrypted embeddings; we use cosine similarity to try to calculate the score of the user input embedding with the embeddings in the database. The score is then used to approximate the most similar embedding in the database.
More specifically, the User will send us their encrypted embedding matrix: (N x d), where N is the number of tokens, d is the dimension of embedding.
We will strive to convert this particular matrix to it's most similar Non-encrypted Embedding matrix

# Code 
The code is written using the EVA library by Microsoft

```
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

```

# Notes

This can be used to give the LLM another prompt altogether, but then it may not be what the user is expecting. The use-case is hence narrow.



Question: I earn $75K, have $30K in savings, no debt, rent from my parents who are losing home. Should I buy home now or save?

Such a question need not be posted to LLM carrying such specifics, the user can simply expect back, an abstract answer???

## Another Method: TextFusion: Privacy-Preserving Pre-trained Model Inference via Token Fusion
# Token Fusion

User computes intermediate representations of the tokens and during this computation tokens are selectively fused to provide a final representation that is deterrent to privacy attacks (Text inversion attacks)

Will need to retrain the entire model (fine tune) along with token predictors
Reference: https://aclanthology.org/2022.emnlp-main.572/
