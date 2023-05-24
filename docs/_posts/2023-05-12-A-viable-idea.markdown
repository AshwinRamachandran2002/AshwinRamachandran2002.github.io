---
layout: post
title:  "A viable IDEA"
date:   2023-05-12 08:24:51 +0200
categories: jekyll update
---


# Method 1: Toward Privacy-preserving Text Embedding Similarity with Homomorphic Encryption
## CKKS

A fourth generation HE, that has the ability to perform the operations:

1. Add(ct1, ct2)
2. Mult(ct1, ct2)
3. Bootstrap(ct1)

The above operations can also be performed between CipherText and PlainText, this has 
less noise increase than between CipherText and CipherText.

## Approximating the Cosine Similarity function

For Language Models, the input is initially transformed to tokens and then it's embeddings from a 
fixed dictionary module. We attempt to provide privacy by constructing embeddings using encrypted text input

cos(Theta) = u.v / (||u|| ||v||)
           = (u1v1 + u2v2 ...) / (sqroot((u1^2 + u2^2) x (v1^2 + v2^2))


Approximation of the Square Root Inverse:
Derivation: 

Have an initialisation value y0 = 1, f(y) = (1/y)^2 - x
y_(n+1) = y_n - ((1/y_n)^2 - x) / (-2/y_n^3)
y_(n+1) = y_n + (1/2)(y_n - x * y_n^3)
y_(n+1) = (1/2)(3 * y_n - x * y_n^3)
y_(n+1) = (1/2) * y_n * (3 - x*y_n^2)

Hence we obtain a y' such that y' ~ 1/root(x), given an x
But here, x is a CipherText in CKKS

# Code 

We first import Seal package and set up parameters for CKKS (get the appropriate parameters from Paper)

```
import random
import numpy as np
import seal

# Set up CKKS parameters
parms = seal.CKKSParameters(seal.SchemeType.ckks)
parms.set_poly_modulus_degree(8192)
parms.set_coeff_modulus(seal.coeff_modulus_128(8192))
parms.set_plain_modulus(1 << 8)

```

Create the CKKS encryptor

```
# Create a CKKS encryptor
context = seal.SEALContext(parms)
keygen = seal.KeyGenerator(context)
public_key = keygen.public_key()
encryptor = seal.Encryptor(context, public_key)

```

We import the HuggingFace Sentence-Transformer to embed the sentence

```
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

PlainTextSentence = "Hi! I am some years old, can I spend money?"
PlainTextEmbedding = model.encode([PlainTextSentence])

CipherTextSentence = "Hi! I am some years old, can I spend money?"
CipherTextEmbedding = model.encode([CipherTextSentence])

# Encrypt the CipherTextEmbedding
CipherTextEncrypted = []
for value in CipherTextEmbedding:
    plaintext = seal.Plaintext()
    encoder = seal.CKKSEncoder(context)
    encoder.encode(value, parms.plain_modulus(), plaintext)
    encrypted = seal.Ciphertext()
    encryptor.encrypt(plaintext, encrypted)
    encrypted_vector.append(encrypted)

```

We now have the CipherTextEncrypted, we can now perform the operations on it

```
# Compute the dot product of the two vectors
result = seal.Ciphertext()
evaluator.multiply_plain(encrypted_vector, PlainTextEmbedding) # Multiply encrypted vector with plaintext
evaluator.add_many(encrypted_vector, result) # Sum the encrypted vector
plain_result = seal.Plaintext()
decryptor.decrypt(result, plain_result) # Decrypt the result
dot_product = encoder.decode(plain_result) # Decode the plaintext as a numpy array

print("Dot product result:", dot_product)

```

# Thoughts

This can be used to give the LLM another prompt altogether, but then it may not be 
what the user is expecting. Cannot be used in the LLM situation.

We need the original embeddings going to the LLM in an encrypted fashion. (Can input embeddings directly to HuggingFace Models)
We require that all computation of PT.PT can also be done as CT.CT.

2-PC: currently has very heavy compuations for matrix-matrix operation, matrix-vector is simpler (Cheetah: Lean and fast secure two-party deep neural network inference)





## Operations in a Transformer
1.   

# Method 2: TextFusion: Privacy-Preserving Pre-trained Model Inference via Token Fusion
## Token Fusion

User computes intermediate representations of the tokens and during this computation tokens
are selectively fused to provide a final representation that is deterrent to privacy attacks (Text inversion attacks)

Will need to retrain the entire model (fine tune) along with token predictors



# Idea 1: Converting Encrypted Embeddings input to LLM to their most similar Embeddings

User will send us their encrypted embedding matrix: (N x d), where N is the number of tokens, d is the dimension of embedding.
We will strive to convert this particular matrix to it's most similar Non-encrypted Embedding matrix

Question: I earn $75K, have $30K in savings, no debt, rent from my parents who are losing home. Should I buy home now or save?

Such a question need not be posted to LLM carrying such specifics, the user can simply expect back, an abstract answer???
