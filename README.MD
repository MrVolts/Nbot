THIS IS A (WORKING) PROTOTYPE:

Issues:
Website scraper needs a lot of work

dependancies that I can remember:

pip install python-dotenv
pip install -qU bs4 tiktoken openai langchain pinecone-client[grpc]

How to use:

1) create a .env file with the following information that can be obtained from https://platform.openai.com/login/ and https://app.pinecone.io/ :

```
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=
PINECONE_INDEX_NAME=
```

2) running setupnbot.py uses a website scraper and creates the pinecone vector file

3) asknbot.py file can be edited and ran with your question

4) running clearnbot.py cleares the vector file and starts a fresh one


