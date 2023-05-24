---
layout: post
title:  "Codeforces 872"
date:   2023-05-11 08:24:51 +0200
categories: jekyll update
published: false
---

# Question

n floating islands, make a tree
want to visit k people, k = min(n, 3)
island good only if sum of dist from it to k is minimal
what is expect number of good islands overall distri of k ppl in n islands

# Solution

Case when n=1, Ans = 1
Case when n=2, Ans = (2 + 1 + 1) / 3
Case when n >= 3, k = 3,
Only one possible per tuple of 3, nC3 x 1 / nC3

Case when n >= 3, k = 2,
For one tuple of 2, (shortest path + 1) good islands
We have to find the expected distance between two nodes
If I know the distance from root of a subtree to every node inside, then the node above the root will have
expected distance 1 + (expected from subtree root)

We calculate the expected distance from a node keeping that as one of the edge vertex

Case when n>=3, k = 1,
Only one possible, island itself, so nC1 x 1 / nC1