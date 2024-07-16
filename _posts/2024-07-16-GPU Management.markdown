---
layout: post
title: "GPU Management"
description: 
date: 2024-07-16 08:24:51 +0200
---

# Problem
This is a project born out of the problems I faced during my time as a student researcher at IIT Bombay. The institute had a limited set of GPUs and there always existed infighting amongst us students to get priority access to the GPUs. GPU management was required.


# Design of a V1 Solution
## First version limitations
- Will not be model specific, hence treating all models the same
    - Should not matter according our algorithm
    - Have to check how far off our algorithm is from the most efficient split of transformers
- Will not multi node
    - Probably will be easy since all iitb servers are connected
    - Overhead to be measured
- Assuming largest layer will fit in a single gpu
    - Otherwise will have to resort to tensor parallelism
- All layers together fill fit in all the gpus available in the node
    - Otherwise will have to resort to multi node
## Parallelization ways
- Data parallel
    - The zero implementation by deep speed
    - Split the params, gradients, optimizer states and the activations are stored in memory into multiple gpus
    - When going through one gpu, it gives all the other gpus the params and the activations in both passes and collects the gradients accumulated in backward pass
    - Pain points
        - How to determine the correct split of the three things
            - Split maybe just one if not able to
            - Compute the lowest possible split possible and each of the sections memory occupancy
                - Is this an effective strategy?
        - What to do if any of the gpus are not free
            - Calculate the coalesce of the splits
            - Thus the split will be discrete
        - What to do if suddenly a part of gpu is occupied or freed up
            - Every t interval, run the algorithm and determine effective split
            - Have to keep in mind the gpu-to-gpu transfer (the same overhead occurs when transferring the params, just the more memory, but that may be irrelevant
    - Model parallel and pipeline parallel
        - Model is sequentially split across the gpus
        - Data is divided into micro batches
        - Each micro batches pass through first split and then move on
        - Parameters of the model are not shared with any other gpu
    - Tensor parallelism
        - All gpus have all the data but the model parameters are split horizontally
## System design
- Assertion
    - largest layer will fit in a single gpu
    - All layers together fill fit in all the gpus available in the node
- Input variables
    - GPU memory
    - Gpu utilization

## Algorithm
- Step 1: Determine the memory occupied the model
    - Parameters
    - Gradients
    - Optimizer states
    - Input data
- Step 2 : Determine the splits for the model

## Version 1
- Given a single model of memory M, it has to discover the best place and deploy it
    - Input
        - Gpu memory
        - Gpu utlization
    - First version would be a simple model deployer, no ZERO configurations, no multiple nodes
    - Identify from among all the gpus
        - Where the model can fit
        - Where there is less gpu utilization
    - Deploy model to any of the best gpus
        - Through onnx
        - Wont involve changes to code
    - Through deepspeed
        - Will involve changes to code
# References
- https://huggingface.co/docs/transformers/v4.15.0/en/parallelism
- https://www.microsoft.com/en-us/research/blog/zero-deepspeed-new-system-optimizations-enable-training-models-with-over-100-billion-parameters/
- https://github.com/microsoft/DeepSpeed
- https://towardsdatascience.com/pytorch-lightning-vs-deepspeed-vs-fsdp-vs-ffcv-vs-e0d6b2a95719


