# [Capstone project 1 - RAG](https://github.com/bakhridinova/advanced-generative-ai-capstone-project/tree/master/rag)

## Objective

Build a Customer Support solution able to answer questions and raise support tickets.

## Business features

Via web chat user can ask questions and get answers from datasources

If the answer is not found the system suggest user to create a support ticket

User can instruct system to create a support ticket

Support ticket should have user name, user email, summary (title) and description with details

Support ticket should be put into issue tracking system (Jira/Trello/Github etc.)

System should cite document and page when answering from data, e.g. if the answer is from toyota-hilux manual system should mention the file name and the page with source

System should support conversation history and keep the chat messages in context window

AI system should know about the company it's working in, like name and contact information (phone/email)

## Data

at least 3 documents should be used as a datasource

at least 2 documents should be PDF

at least 1 document should have 400 or more pages of PDF

## Technical requirements

Solution should be build with python

Python version and dependencies should be in the repository

Solution may use any vector storage

Function calling is a must

## Interface

Web UI should be build with Streamlit or Gradio

## Deployment

Solution should be hosted at HuggingFace spaces

# [Capstone project 2 - Art](https://github.com/bakhridinova/advanced-generative-ai-capstone-project/tree/master/art)

## Objective

Design new cover for the media piece. You goal is to create alternative variation of some iconic media, like a book, cd album, vinyl album or DVD box with movie.

## Requirements

Image should be generated with self-hosted solution running either in cloud or locally. You are not allowed to use any publicly available tool for image generation like sora/replicate or their APIs. Only self-hosted solutions allowed.

Final result should be a .md file containing:

* original work (cover for album/book/movie)
* AI-generated work (at least 1 variation of book,  one for video and one for audio album, 3 in total)
* workflow:
  1. image generation model used (name, version, link)
  2. loras/adapters/extentions if any
  3. technical generation details: steps, CFG, sampler etc.
  4. screenshot of the pipeline or configuration after the execution
  5. prompts used
* resources used: webui for generation, local or cloud version, hardware used 

Media options to pick up:
*   compact disk album
*   vinyl album
*   VHS tape
*   DVD box
*   book