import os
from datasets import load_dataset
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

data = load_dataset(
    'MrVolts/Nomads',
    name='⚫-general-internal', # Change this to dataset name
    split='train',
    streaming=True
)

pinecone.init(
    api_key=pinecone_api_key,  # app.pinecone.io
    environment=pinecone_environment  # next to API key in console
)

if pinecone_index_name not in pinecone.list_indexes():
    raise ValueError(
        f"No '{pinecone_index_name}' index exists. You must create the index before "
        "running this notebook. Please refer to the walkthrough at "
        "'github.com/pinecone-io/examples'."  # TODO add full link
    )

index = pinecone.Index(pinecone_index_name)

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

vectordb = Pinecone(
    index=index,
    embedding_function=embeddings.embed_query,
    text_key="text" # which metadata field contains the text to embed
)

llm=ChatOpenAI(
    openai_api_key=openai_api_key,
    temperature=0,
    model_name='gpt-3.5-turbo'
)