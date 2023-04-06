import os
import datetime
from urllib.parse import urlparse, urljoin
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from tqdm.auto import tqdm
import openai
import pinecone
from time import sleep
from dotenv import load_dotenv
from dateutil.parser import parse
import random
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from scrapers.webscraper import WebScraper
from scrapers.jsonscraper import get_json_data
from database.database_handler import DatabaseHandler

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")


data = []
chunks = []

# Add a namespace variable (change this as needed)
namespace = "testing"

# Use the WebScraper class
scraper = WebScraper()

# Use the scrape_text method to get the text from the web page
url = "https://example.com/"
scraped_text = scraper.scrape_text(url)

# Process the scraped_text and append it to the data list
data.append({"text": scraped_text, "channel": "website_scraper"})

# Get JSON data
# json_data = get_json_data()
# data.extend(json_data)

# Tokenizer and text splitter
tokenizer = tiktoken.get_encoding('p50k_base')

def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=20,
    length_function=tiktoken_len,
    separators=[", {", "\n\n", "\n", " ", ""]
)

for idx, record in enumerate(tqdm(data)):
    texts = text_splitter.split_text(record['text'])

    # Include the timestamp at the start of the chunk
    chunks.extend([{
        'id': str(uuid4()),
        'text': "{" + texts[i],
        'chunk': i,
        'channel': record['channel']
    } for i in range(len(texts))])

# Print 5 random elements from the chunks list with full text
print("5 random elements in chunks list:")
for i in random.sample(range(len(chunks)), 1):
    print(f"{i+1}. ID: {chunks[i]['id']}, Channel: {chunks[i]['channel']}, Chunk: {chunks[i]['chunk']}\nText:\n{chunks[i]['text']}\n")

# Initialize openai API key
openai.api_key = openai_api_key

embed_model = "text-embedding-ada-002"

res = openai.Embedding.create(
    input=[
        "Sample document text goes here",
        "there will be several phrases in each batch"
    ], engine=embed_model
)

index_name = pinecone_index_name

# Initialize connection to Pinecone
pinecone.init(
    api_key=pinecone_api_key,
    environment=pinecone_environment
)

# Check if index already exists (it shouldn't if this is first time)
if index_name not in pinecone.list_indexes():
    # If does not exist, create index
    pinecone.create_index(
        index_name,
        dimension=len(res['data'][0]['embedding']),
        metric='dotproduct'
    )
# Connect to index
index = pinecone.GRPCIndex(index_name)
# View index stats
index.describe_index_stats()

db_handler = DatabaseHandler(index)

# Your existing code for processing the data

batch_size = 100

for i in tqdm(range(0, len(chunks), batch_size)):
    # Find end of batch
    i_end = min(len(chunks), i + batch_size)
    meta_batch = chunks[i:i_end]
    # Get ids
    ids_batch = [x['id'] for x in meta_batch]
    # Get texts to encode
    texts = [x['text'] for x in meta_batch]
    # Create embeddings (try-except added to avoid RateLimitError)
    try:
        res = openai.Embedding.create(input=texts, engine=embed_model)
    except:
        done = False
        while not done:
            sleep(5)
            try:
                res = openai.Embedding.create(input=texts, engine=embed_model)
                done = True
            except:
                pass
    embeds = [record['embedding'] for record in res['data']]
    # Cleanup metadata
    meta_batch = [{
        'id': x['id'],
        'text': x['text'],
        'chunk': x['chunk'],
        'channel': x['channel']
    } for x in meta_batch]
    to_upsert = list(zip(ids_batch, embeds, meta_batch))
    # Upsert to Pinecone
    index.upsert(vectors=to_upsert, namespace=namespace)
    
    # Use a database connection to store Pinecone block information
for record in meta_batch:
    db_handler.insert_block(record['id'], record['channel'], namespace=namespace, created_at=datetime.datetime.utcnow())