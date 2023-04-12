import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from uuid import uuid4
from tqdm.auto import tqdm
import json
import random
from tqdm.auto import tqdm
import datetime
from sql_database_handler import DatabaseHandler
from dotenv import load_dotenv
from dateutil.parser import parse

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
    _, file_extension = os.path.splitext(input_filename)

    # If the file is a JSONL file, read it line by line as separate JSON objects
    if file_extension.lower() == '.jsonl':
        data = []
        with open(input_filename, 'r') as f:
            for line in f:
                data.append(json.loads(line))
        return data

    # Otherwise, read the whole file as a single text string (assuming it's a text file)
    else:
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
    # Load environment variables
    load_dotenv()
    
    # Define source directory
    current_directory = os.path.abspath(os.path.dirname(__file__))
    parent_directory = os.path.dirname(current_directory)
    source_directory = os.path.join(parent_directory, 'sampledata')

    # Create the data folder in the current directory if it doesn't exist
    data_folder = os.path.join(current_directory, "data")
    os.makedirs(data_folder, exist_ok=True)

    # Get all input file paths in the source directory
    input_filepaths = get_input_filepaths_recursive(source_directory)

    # Get the Pinecone index name from the .env file
    index = os.getenv("PINECONE_INDEX_NAME")

    # Process each input file
    for input_filepath in input_filepaths:
        # Load the data from the input file
        data = load_input_data(input_filepath)

        # Get user_folder name and source name
        user_folder = os.path.dirname(os.path.relpath(input_filepath, source_directory)).encode('utf-8')
        source_name = os.path.splitext(os.path.basename(input_filepath))[0]

        # Create the user folder inside the data folder if it doesn't exist
        user_data_folder = os.path.join(data_folder, user_folder.decode('utf-8'))
        os.makedirs(user_data_folder, exist_ok=True)

        # Folder and filename to store the data
        output_filename = os.path.join(user_data_folder, f'{source_name}_data.jsonl')

        # Get namespace (parent folder name)
        namespace = os.path.dirname(os.path.relpath(input_filepath, source_directory)).split(os.path.sep)[0]

        # Process the input data and save it in the required format
        process_data_and_save_output(data, user_data_folder, output_filename, source_name, namespace=namespace, index=index)

        # Delete the processed input file
        os.remove(input_filepath)

def process_data_and_save_output(data, user_folder, output_filename, source_name, namespace=None, index=None):
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
        separators=["},","\n\n", "\n", " ", ""]
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
                'namespace': namespace,
                'index': index
            }
            chunks.append(chunk)
            global_chunk_counter += 1

    # Create the user folder if it doesn't exist
    os.makedirs(user_folder, exist_ok=True)

    # Initialize the DatabaseHandler
    db_handler = DatabaseHandler()

    if os.path.exists(output_filename):
        # If the file exists, append the new chunks
        with open(output_filename, 'a') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk) + '\n')
                created_at = parse(chunk['date'])  # Convert the date string to a datetime object
                db_handler.insert_block(chunk['id'], chunk['source'], chunk['chunk'], namespace, index, created_at)
    else:
        # If the file doesn't exist, create a new one and save the chunks
        with open(output_filename, 'w') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk) + '\n')
                created_at = parse(chunk['date'])  # Convert the date string to a datetime object
                db_handler.insert_block(chunk['id'], chunk['source'], chunk['chunk'], namespace, index, created_at)

                
    write_chunk_counter(global_chunk_counter)

    print(f"File: {output_filename}")
    print("5 random elements in chunks list:")
    for i in random.sample(range(len(chunks)), 5):
        print(f"{i+1}. ID: {chunks[i]['id']}, source: {chunks[i]['source']}, Chunk: {chunks[i]['chunk']}, Date: {chunks[i]['date']}, Namespace: {chunks[i]['namespace']}, Index: {chunks[i]['index']}\nText:\n{chunks[i]['text']}\n")

    

if __name__ == "__main__":
    main()