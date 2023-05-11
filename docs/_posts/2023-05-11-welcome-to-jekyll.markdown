---
layout: post
title:  "Privacy Preserving in ML"
date:   2023-05-11 08:24:51 +0200
categories: jekyll update
---


PrivateGPT

Just identifies PII pf 50+ categories and removes it, not really privacy

Homomorphic Encryption

It is a cryptographic method to perform computations tht are encrypted and produce 
the same product had the operations been performed on an unencrypted data

Applying to ML 

https://youtu.be/culuNbMPP0k

Existing work talk about construction of ML models with the computing infrastructure for 
HME. But can HME based methods be applied to existing LLM models like OpenAI GPT-3.5?

Applying to OpenAI models - FlanT5

What are the computations done by FlanT5 model ?

https://huggingface.co/blog/sentiment-analysis-fhe


Applying it to ResNet-20: A case study
https://arxiv.org/pdf/2106.07229.pdf

Dont think its possible presently
Have to develop FHE specific architecture models from scratch
https://blog.openmined.org/ckks-explained-part-5-rescaling/
https://github.com/zama-ai/concrete-ml/tree/release/1.0.x
https://www.youtube.com/watch?v=-lhn2GdHhGc&ab_channel=GoogleTechTalks
https://huggingface.co/papers/2305.05973
https://arxiv.org/pdf/2210.02574.pdf
https://www.youtube.com/watch?v=culuNbMPP0k&t=3397s&ab_channel=TheIACR


MPC based solution


https://arxiv.org/pdf/2211.01452.pdf