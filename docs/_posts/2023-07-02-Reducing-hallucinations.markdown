---
layout: post
title:  "Reducing Hallucinations"
date:   2023-06-28 08:24:51 +0200
categories: jekyll update
---

# Introduction
LLMs suffer from hallucinations. This is a problem that is being addressed by the research community. The aim of this project is to reduce hallucinations in LLMs. Today, applications use an LLM alongside a database

# Quivr

## How it works
The Quivr application is a web app that was introduced as a second brain. It allows users to upload pdfs, images, etc or websites and then query the "second brain" at a later time. Users need not go through all the information again but the application answers the queries using an LLM. The application uses Langchain Document Query api to retrieve the correct source and correct chunk and supplies it to the LLM as context. The context along with the query is input to the LLM and the LLM answers appropriately. 

## Problems with the application
I tried uploading a bunch of pdfs and asked a bunch of questions. The LLM would incorrectly use it's hallucinations to answer the question. The hallucinations were not even close to the answer. This would imply that the context supplied to the LLM is not relevant to the query being asked. A better way to supply context is required.

# COLBERT model from Stanford
Developed by the Stanford NLP group, Omar Khatab.

## How it works
I noticed the COLBERT2 retriever which used late interaction to retrieve relevant context from a huge corpus given a query. The model does not convert the whole paragraph to an embedding, i.e. it does not use the final fully connected layer in transformers to obtain a single embedding, but leaves the output as a bunch of embeddings as is produced from a decoder of a transformer.
All the chunks in the corpus are converted to such group of embeddings and kept aside to be used during runtime. The query when input, is processed and output as a bunch of embeddings. These embeddings are now compared against each other on a token level rather than on a sentence level, and the result noticed is greatly better than than a sentence level comparison.

## Applications
The COLBERT model was demonstrated on the wikipedia corpus. Given a sentence "When was Titanic released?" and "Titanic, a classic, was out in theatres by 2nd October.", the model gave a high similarity score for the tokens, "released" and "out in", "titanic" with "titanic", "When" with "2nd October".

# The DSP model
Developed by the Stanford NLP group, Omar Khatab.

## How it works
The Demonstrate Search Predict framework, combines both the COLBERT model and the LLM. The DSP model is a multihop process. The LLM tries to break the question into multiple questions. It tries to determine the information required to answer the question. The information to be acquired is posed as a question to the COLBERT2 model which fetches the relevant context. It returns the most relevant k chunks. These chunks are given to the LLM as context, the model then uses the context to either answer the question or decide to ask more questions to make a better decision.

## NCERT Question-Answer Retriever
The DSP framework requires a manual setting of the number of hops it has to take before arriving at an answer.
I tested out the system on the NCERT Chemistry 12th standard TextBooks and asked it the questions posed to students as part of their CBSE board examination and received the correct in answer in 80 percent of the cases. 
Few of the questions, it failed to answer correctly since the PDF couldn't be converted to a text format as it was a scanned copy. The equations were converted in a jumbled manner and the sections were not formatte properly. The PDFConverter used was the Langchain API.
Another factor was the size of the chunk to divide the text into; I estimate the accuracy would have been better if specific sections and paragraphs were converted as one chunk instead of division on the basis of number of tokens in a chunk.
I write a more detailed blog on the NCERT Question-Answer Retriever in another blog post.