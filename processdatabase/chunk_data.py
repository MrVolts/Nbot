import os
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from uuid import uuid4
from tqdm.auto import tqdm
import json
import random
from tqdm.auto import tqdm

def load_input_data(input_filename):
    with open(input_filename, 'r') as f:
        text = f.read()
    return [{'text': text}]

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

        # Get user_folder name
        user_folder = os.path.splitext(os.path.basename(input_filepath))[0]

        # Folder and filename to store the data
        output_filename = f'{user_folder}/{user_folder}_data.jsonl'

        # Process the input data and save it in the required format
        process_data_and_save_output(data, user_folder, output_filename)

        # Delete the processed input file
        os.remove(input_filepath)

def process_data_and_save_output(data, user_folder, output_filename):
    if isinstance(data, str):
        data = [{'text': data}]
        
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
        chunks.extend([{
            'id': str(uuid4()),
            'text': t,
            'chunk': i,
            'channel': user_folder
        } for i, t in enumerate(text_splitter.split_text(record['text']))])


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

    print(f"File: {output_filename}")
    print("5 random elements in chunks list:")
    for i in random.sample(range(len(chunks)), 5):
        print(f"{i+1}. ID: {chunks[i]['id']}, Channel: {chunks[i]['channel']}, Chunk: {chunks[i]['chunk']}\nText:\n{chunks[i]['text']}\n")
    

if __name__ == "__main__":
    main()
