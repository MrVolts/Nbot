import os
import json
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

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

def extract_message_info(message):
    author_name = message['author']['name']
    author_id = message['author']['id']

    content = message['content']
    info = {'author_name': author_name, 'author_id': author_id, 'content': content}
    return json.dumps(info)

# Read all JSON files from the sourcesnbot folder
sourcesnbot_dir = "sourcesnbot"
json_files = [f for f in os.listdir(sourcesnbot_dir) if f.endswith(".json")]

# Load data from JSON files
data = []
for file_name in json_files:
    channel = os.path.splitext(file_name)[0]
    with open(os.path.join(sourcesnbot_dir, file_name), "r") as file:
        json_data = json.load(file)
        messages = json_data['messages']
        extracted_messages = [extract_message_info(message) for message in messages]
        content = "[" + ", ".join(extracted_messages) + "]"
        data.append({"text": content, "channel": channel})

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

# Process the data
chunks = []

for idx, record in enumerate(tqdm(data)):
    texts = text_splitter.split_text(record['text'])

    # Get the timestamp from the first message and convert it to a short date
    first_message_original = messages[0]
    timestamp = first_message_original['timestamp']
    dt = parse(timestamp)
    short_date = dt.strftime("%Y-%m-%d")

    # Include the timestamp at the start of the chunk
    chunks.extend([{
        'id': str(uuid4()),
        'text': f"Timestamp: {short_date}\n" + "{" + texts[i],
        'chunk': i,
        'channel': record['channel']
    } for i in range(len(texts))])
    
# Print 5 random elements from the chunks list with full text
print("5 random elements in chunks list:")
for i in random.sample(range(len(chunks)), 5):
    print(f"{i+1}. ID: {chunks[i]['id']}, Channel: {chunks[i]['channel']}, Chunk: {chunks[i]['chunk']}\nText:\n{chunks[i]['text']}\n")

# initialize openai API key
openai.api_key = openai_api_key

embed_model = "text-embedding-ada-002"

res = openai.Embedding.create(
    input=[
        "Sample document text goes here",
        "there will be several phrases in each batch"
    ], engine=embed_model
)

index_name = pinecone_index_name

# initialize connection to pinecone
pinecone.init(
    api_key=pinecone_api_key,
    environment=pinecone_environment
)

# check if index already exists (it shouldn't if this is first time)
if index_name not in pinecone.list_indexes():
    # if does not exist, create index
    pinecone.create_index(
        index_name,
        dimension=len(res['data'][0]['embedding']),
        metric='dotproduct'
    )
# connect to index
index = pinecone.GRPCIndex(index_name)
# view index stats
index.describe_index_stats()

batch_size = 100  # how many embeddings we create and insert at once

for i in tqdm(range(0, len(chunks), batch_size)):
    # find end of batch
    i_end = min(len(chunks), i+batch_size)
    meta_batch = chunks[i:i_end]
    # get ids
    ids_batch = [x['id'] for x in meta_batch]
    # get texts to encode
    texts = [x['text'] for x in meta_batch]
    # create embeddings (try-except added to avoid RateLimitError)
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
    # cleanup metadata
    meta_batch = [{
        'text': x['text'],
        'chunk': x['chunk'],
        'channel': x['channel']
    } for x in meta_batch]
    to_upsert = list(zip(ids_batch, embeds, meta_batch))
    # upsert to Pinecone
    index.upsert(vectors=to_upsert)