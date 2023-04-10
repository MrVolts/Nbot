import os
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from uuid import uuid4
from tqdm.auto import tqdm
import json
import random

# Source directory and filename
source_directory = 'source'
input_filename = f'{source_directory}/input_data.json'

# Folder and filename to store the data
user_folder = 'user1'
output_filename = f'{user_folder}/{user_folder}_data.jsonl'

##############################################
Main code
##############################################

# Where the data is stored
data = []
# Where the chunks are stored
chunks = []

# cl100k is for gpt-3.5-turbo and gpt-4
tokenizer = tiktoken.get_encoding('cl100k_base')

# create the length function find lengh of text in tokens
def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

# Split the text into chunks of x tokens with y token overlap
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,  # number of tokens overlap between chunks
    length_function=tiktoken_len,
    separators=['\n\n', '\n', ' ', '']
)

# Split the text into chunks
for idx, record in enumerate(tqdm(data)):
    texts = text_splitter.split_text(record['text'])

    # Include the timestamp at the start of the chunk
    chunks.extend([{
        'id': str(uuid4()),
        'text': "{" + texts[i],
        'chunk': i,
        'channel': record['channel']
    } for i in range(len(texts))])
    
# Create the user folder if it doesn't exist
os.makedirs(user_folder, exist_ok=True)

# Save the chunks to the jsonl file
if os.path.exists(output_filename):
    # If the file exists, append the new chunks
    with open(output_filename, 'a') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + '\n')
else:
    # If the file doesn't exist, create a new one and save the chunks
    with open(output_filename, 'w') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + '\n')
        
        
        
        
    
# Print 5 random elements from the chunks list with full text
print("5 random elements in chunks list:")
for i in random.sample(range(len(chunks)), 5):
    print(f"{i+1}. ID: {chunks[i]['id']}, Channel: {chunks[i]['channel']}, Chunk: {chunks[i]['chunk']}\nText:\n{chunks[i]['text']}\n")
