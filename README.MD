THIS IS A (WORKING) PROTOTYPE:

Issues:
Discord Bot needs cleaning up

Todo:
Create a web application with different types of bots fed different context
API

dependancies that I can remember:

pip install python-dotenv
pip install -qU bs4 tiktoken openai langchain pinecone-client[grpc]
pip install discord
pip install datasets
pip install git-lfs
huggingface-cli login
pip install huggingface_hub

How to use:

1) create a .env file with the following information that can be obtained from https://platform.openai.com/login/ and https://app.pinecone.io/ :

```
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=
PINECONE_INDEX_NAME=
DISCORD_TOKEN=
HF_API_KEY=
```

2) running setupnbot.py scrapes a given website or processes a json

3) asknbot.py file can be edited and ran with your question

4) running clearnbot.py cleares the vector file and starts a fresh one

5) running /home/ubuntu/NomadsAI/database/database_menu.py allows you to manage pinecone database


