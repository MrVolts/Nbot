import requests
from bs4 import BeautifulSoup
import urllib.parse
import html
import re
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from tqdm.auto import tqdm
import openai
import pinecone
from tqdm.auto import tqdm
import datetime
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

res = requests.get("https://python.langchain.com/en/latest/index.html")
res

domain = "https://langchain.readthedocs.io/"
domain_full = domain+"en/latest/"

def scrape(url: str):
    res = requests.get(url)
    if res.status_code != 200:
        print(f"{res.status_code} for '{url}'")
        return None
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find all links to local pages on the website
    local_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith(domain) or href.startswith('./') \
            or href.startswith('/') or href.startswith('modules') \
            or href.startswith('use_cases'):
            local_links.append(urllib.parse.urljoin(domain_full, href))

    # Find the main content using CSS selectors
    main_content = soup.select('body main')[0]

    # Extract the HTML code of the main content
    main_content_html = str(main_content)

    # Extract the plaintext of the main content
    main_content_text = main_content.get_text()

    # Remove all HTML tags
    main_content_text = re.sub(r'<[^>]+>', '', main_content_text)

    # Remove extra white space
    main_content_text = ' '.join(main_content_text.split())

    # Replace HTML entities with their corresponding characters
    main_content_text = html.unescape(main_content_text)

    # return as json
    return {
        "url": url,
        "text": main_content_text
    }, local_links
     

links = ["https://langchain.readthedocs.io/en/latest/"]
scraped = set()
data = []

while True:
    if len(links) == 0:
        print("Complete")
        break
    url = links[0]
    print(url)
    res = scrape(url)
    scraped.add(url)
    if res is not None:
        page_content, local_links = res
        data.append(page_content)
        # add new links to links list
        links.extend(local_links)
        # remove duplicates
        links = list(set(links))
    # remove links already scraped
    links = [link for link in links if link not in scraped]

    
tokenizer = tiktoken.get_encoding('p50k_base')

# create the length function
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
    separators=["\n\n", "\n", " ", ""]
)

chunks = []

for idx, record in enumerate(tqdm(data)):
    texts = text_splitter.split_text(record['text'])
    chunks.extend([{
        'id': str(uuid4()),
        'text': texts[i],
        'chunk': i,
        'url': record['url']
    } for i in range(len(texts))])

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
        'url': x['url']
    } for x in meta_batch]
    to_upsert = list(zip(ids_batch, embeds, meta_batch))
    # upsert to Pinecone
    index.upsert(vectors=to_upsert)
