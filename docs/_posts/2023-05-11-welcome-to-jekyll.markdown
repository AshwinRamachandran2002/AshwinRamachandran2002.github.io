---
layout: post
title:  "Privacy Preservation in ML"
description: march & april, looking forward to summer
date:   2023-05-27 08:24:51 +0200
categories: jekyll update
---

## Introduction
Presently, the user prompt input to models such as ChatGPT and Bard are not encrypted. This is a major privacy concern as the user may input sensitive information to the model. The company may use the information to train the model further or other purposes. A way to introduce prompts in a more privacy preserving manner is required.

## PrivateGPT
A agent introduced to tackle the issue of PII present in the prompts input by users. But the agent uses a heurisitic method where it identifies PII of 50+ categories and removes it from the prompt. This is not a scalable solution as the number of categories can be infinite.

## Encrypted Input
The best solution would be to have the input encrypted using a Secret Key known only to the user and have the model use it's present trained weights in some way to perform computations on the encrypted input and return the encrypted output. The user can then decrypt the output using the same Secret Key. While searching for such a solution, I came across Homomorphic Encryption.

# Homomorphic Encryption

It is a cryptographic method to perform computations that are encrypted and produce the same product had the operations been performed on an unencrypted data. Almost all the operations can be performed in this space but with a certain amount of latency. The latency is due to the fact that the encrypted data is represented as a polynomial and the operations are performed on the polynomial.
I came across a variety of papers and talks that focused on building models whose computations were performed in the encrypted space. The models were built from scratch and the computations were performed using the CKKS scheme. But can HME based methods be applied to existing LLM models like OpenAI GPT-3.5?


## Applying to OpenAI models - FlanT5
I tried to arrive at a solution wherein you split the input embedding suitably into multiple embeddings (not encrypted) (in a reversible way). Then, pass the embeddings individually receiving output embedding for each input embedding and then constructing the final output embedding. Splitting the embeddings into even two parts has been proven to make it difficult for an adversary to figure out the original embedding. What are the computations done by FlanT5 model ?

# Applying it to ResNet-20: A case study
https://arxiv.org/pdf/2106.07229.pdf

# MPC based solution
Multi Party Computation is another technique like HME to introduce privacy
https://arxiv.org/pdf/2211.01452.pdf

## Interesting Links 
Sentiment Analysis on Encrypoted Data:
https://huggingface.co/blog/sentiment-analysis-fhe

How Crypto is predicted to define ML:
https://youtu.be/culuNbMPP0k

CKKS Encryotion Scheme:
https://blog.openmined.org/ckks-explained-part-5-rescaling/

ZAMA AI's ML models using HME:
https://github.com/zama-ai/concrete-ml/tree/release/1.0.x
https://www.youtube.com/watch?v=-lhn2GdHhGc&ab_channel=GoogleTechTalks

Privacy-Preserving Recommender Systems:
https://huggingface.co/papers/2305.05973

Privacy-Preserving Text Classification:
https://arxiv.org/pdf/2210.02574.pdf
