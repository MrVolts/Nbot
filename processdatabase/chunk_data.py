import os
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from uuid import uuid4
from tqdm.auto import tqdm
import json
import random
from tqdm.auto import tqdm
import datetime

global_chunk_counter = 0

def read_chunk_counter(file_name="chunk_counter.txt"):
    try:
        with open(file_name, "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def write_chunk_counter(value, file_name="chunk_counter.txt"):
    with open(file_name, "w") as f:
        f.write(str(value))

def load_input_data(input_filename):
    with open(input_filename, 'r') as f:
        text = f.read()
    return [{'text': text}]

def get_input_filepaths_recursive(dir_path):
    input_filepaths = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            input_filepaths.append(os.path.join(root, file))
    return input_filepaths

def main():
    # Define source directory
    current_directory = os.path.abspath(os.path.dirname(__file__))
    parent_directory = os.path.dirname(current_directory)
    source_directory = os.path.join(parent_directory, 'sampledata')

    # Get all input file paths in the source directory
    input_filepaths = [os.path.join(source_directory, f) for f in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, f))]

    # Process each input file
    for input_filepath in input_filepaths:
        # Load the data from the input file
        data = load_input_data(input_filepath)

        # Get user_folder name and source name
        user_folder = os.path.relpath(os.path.dirname(input_filepath), source_directory)
        source_name = os.path.splitext(os.path.basename(input_filepath))[0]

        # Folder and filename to store the data
        output_filename = f'{user_folder}/{source_name}_data.jsonl'

        # Process the input data and save it in the required format
        process_data_and_save_output(data, user_folder, output_filename, source_name)

        # Delete the processed input file
        os.remove(input_filepath)

def process_data_and_save_output(data, user_folder, output_filename, source_name):
    global global_chunk_counter
    if isinstance(data, str):
        data = [{'text': data}]
        
    global_chunk_counter = read_chunk_counter()
        
    chunks = []

    # Use the p50k_base tokenizer
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
        chunk_size=500,
        chunk_overlap=20,  # number of tokens overlap between chunks
        length_function=tiktoken_len,
        separators=["\n\n", "\n", " ", ""]
    )
        
    for idx, record in enumerate(tqdm(data)):
        chunk_texts = text_splitter.split_text(record['text'])
        for i, t in enumerate(chunk_texts):
            chunk = {
                'id': str(uuid4()),
                'text': t,
                'chunk': global_chunk_counter,
                'source': source_name,  # Use channel_name instead of user_folder
                'date': datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
            }
            chunks.append(chunk)
            global_chunk_counter += 1

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
                
    write_chunk_counter(global_chunk_counter)

    print(f"File: {output_filename}")
    print("5 random elements in chunks list:")
    for i in random.sample(range(len(chunks)), 5):
        print(f"{i+1}. ID: {chunks[i]['id']}, source: {chunks[i]['source']}, Chunk: {chunks[i]['chunk']}, Date: {chunks[i]['date']}\nText:\n{chunks[i]['text']}\n")
    

if __name__ == "__main__":
    main()
