import json
import os
from tqdm.auto import tqdm
import openai
import pinecone
from time import sleep
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Initialize openai API key
openai.api_key = openai_api_key

embed_model = "text-embedding-ada-002"

# Initialize connection to Pinecone
pinecone.init(
    api_key=pinecone_api_key,
    environment=pinecone_environment
)

def process_chunk(chunk, embed_model, index, namespace):
    # Get metadata
    meta = {
        'id': chunk['id'],
        'text': chunk['text'],
        'chunk': chunk['chunk'],
        'source': chunk['source'],
        'date': chunk['date'],
        'namespace': chunk['namespace'],
        'index': chunk['index']
    }
    # Create embeddings (try-except added to avoid RateLimitError)
    try:
        res = openai.Embedding.create(input=[chunk['text']], engine=embed_model)
    except:
        done = False
        while not done:
            sleep(5)
            try:
                res = openai.Embedding.create(input=[chunk['text']], engine=embed_model)
                done = True
            except:
                pass
    embeds = [record['embedding'] for record in res['data']]
    # Upsert to Pinecone with metadata
    record = (meta['id'], embeds[0], meta)  # Add metadata to the record
    index.upsert(vectors=[record], namespace=namespace)


# Define function for processing a batch of chunks
def process_batch(batch, embed_model, index):
    namespace_dict = {}
    for chunk in batch:
        namespace = chunk['namespace']
        if namespace not in namespace_dict:
            namespace_dict[namespace] = []
        namespace_dict[namespace].append(chunk)
    for namespace in namespace_dict:
        meta_batch = namespace_dict[namespace]
        for chunk in meta_batch:
            process_chunk(chunk, embed_model, index, namespace)

# Define function for processing a single file
def process_file(file_path, embed_model, index):
    with open(file_path, 'r') as f:
        chunks = [json.loads(line) for line in f]
    for i in tqdm(range(0, len(chunks), batch_size)):
        # Find end of batch
        i_end = min(len(chunks), i + batch_size)
        batch = chunks[i:i_end]
        process_batch(batch, embed_model, index)

batch_size = 100
index_name = pinecone_index_name

# Check if index already exists (it shouldn't if this is first time)
if index_name not in pinecone.list_indexes():
    # If does not exist, create index
    res = openai.Embedding.create(input=["sample text"], engine=embed_model)
    dimension = len(res['data'][0]['embedding'])
    pinecone.create_index(index_name, dimension=dimension, metric='dotproduct')

# Connect to index
index = pinecone.Index(index_name)

# Process all files in data directory
root_dir = "data"
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(subdir, file)
        process_file(file_path, embed_model, index)