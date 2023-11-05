---
layout: post
title:  "NCERT solution retriever"
description: march & april, looking forward to summer
date:   2023-07-02 08:24:51 +0200
categories: jekyll update
---

# Introduction
The aim of the project is to make it easier for students to get answers to their NCERT book questions along with references to the relevant pages in the book. The project is a web app that takes in a question and returns the answer along with the relevant paragraphs.

# How it works

## Input Question
The user inserts a query that he may have. We assume for now that the query is a question that requires answer in a textual form and not a equation form

## Answer Retrieval

### Step 1: Identify the relevant page
We use the dsp framework to first construct a search query that will help answer the question. It can any number of search queries that are created. 
The pdfs uploaded to the database are stored as chunk embeddings. We use the search query to find the most relevant chunk embeddings. We then return these chunk embeddings to the frontend along with the page numbers they lie across. 
The frontend now uses the context retrieved to frame the next search query and the backend is pinged with the new search query along with the page numbers.