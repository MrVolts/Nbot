THIS IS A (WORKING) PROTOTYPE:

Issues:
Bot code is a rush job atm, works but not the cleanest looking
discord bot repeats the open ai code multiple times, can turn into just one function

dependancies that I can remember:

pip install python-dotenv
pip install -qU bs4 tiktoken openai langchain pinecone-client[grpc]
pip install discord

How to use:

1) create a .env file with the following information that can be obtained from https://platform.openai.com/login/ and https://app.pinecone.io/ :

```
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=
PINECONE_INDEX_NAME=
DISCORD_TOKEN=
```

2) running setupnbot.py uses all the json files inside sourcesnbot.py

3) asknbot.py file can be edited and ran with your question

4) running clearnbot.py cleares the vector file and starts a fresh one


