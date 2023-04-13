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

global global_chunk_counter

def read_global_chunk_counter(file_name="global_chunk_counter.txt"):
    try:
        with open(file_name, "r") as f:
            return int(f.readline().strip())
    except FileNotFoundError:
        return 0

def write_global_chunk_counter(value, file_name="global_chunk_counter.txt"):
    with open(file_name, "w") as f:
        f.write(str(value))

def read_channel_message_ids(file_name="channel_message_ids.txt"):
    try:
        with open(file_name, "r") as f:
            message_ids = {}
            for line in f:
                channel_name, message_id = line.strip().split(',')
                if message_id == "None":
                    message_ids[channel_name] = None
                else:
                    message_ids[channel_name] = int(message_id)
            return message_ids
    except FileNotFoundError:
        return {}

def write_channel_message_ids(channel_name, value, file_name="channel_message_ids.txt"):
    message_ids = read_channel_message_ids(file_name)

    if value is not None:  # only update message ID if it is not None
        message_ids[channel_name] = value

    with open(file_name, "w") as f:
        for channel, message_id in message_ids.items():
            if message_id is None:
                f.write(f"{channel},None\n")
            else:
                f.write(f"{channel},{message_id}\n")

def load_input_data(input_filename, channel_name=None):
    _, file_extension = os.path.splitext(input_filename)

    # Get last_message_id for the channel from channel_message_ids.txt file
    if channel_name:
        message_ids = read_channel_message_ids()
        last_message_id = message_ids.get(channel_name, None)
    else:
        last_message_id = None

    # If the file is a JSONL file, read it line by line as separate JSON objects
    if file_extension.lower() == '.jsonl':
        extracted_messages = []
        last_processed_message_id = None
        with open(input_filename, 'r') as f:
            past_last_processed = last_message_id is None
            for line in f:
                message = json.loads(line)

                if not past_last_processed:
                    if 'message_id' in message and message['message_id'] == last_message_id:
                        past_last_processed = True
                    continue

                if 'author_id' in message and 'author_name' in message and 'content' in message:
                    info = {'author_id': message['author_id'], 'author_name': message['author_name'], 'content': message['content']}
                    extracted_messages.append(json.dumps(info))
                    if 'message_id' in message:
                        last_processed_message_id = message['message_id']
        
        content = "\n".join(extracted_messages)
        return [{'text': content}], last_processed_message_id
    else:
        with open(input_filename, 'r') as f:
            text = f.read()
        data = [{'text': text}], None
    
    return data


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
        source_name = os.path.splitext(os.path.basename(input_filepath))[0]
        data, last_processed_message_id = load_input_data(input_filepath, channel_name=source_name)

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
        should_update_message_id, global_chunk_counter = process_data_and_save_output(data, user_data_folder, output_filename, source_name, namespace=namespace, index=index)
        
        write_global_chunk_counter(global_chunk_counter)

        if data and should_update_message_id:
            write_channel_message_ids(source_name, last_processed_message_id)
            
        # Delete the processed input file
        # os.remove(input_filepath)

def process_data_and_save_output(data, user_folder, output_filename, source_name, namespace=None, index=None):
    if isinstance(data, str):
        data = [{'text': data}]
        
    should_update_message_id = True
    
    global_chunk_counter = read_global_chunk_counter()
        
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
    
    # Merge chunks that are smaller than min_chunk_size
    def merge_small_chunks(chunks, min_chunk_size, length_function):
        merged_chunks = []
        for chunk in chunks:
            chunk_size = length_function(chunk)
            if merged_chunks and length_function(merged_chunks[-1]) < min_chunk_size:
                merged_chunks[-1] += chunk
            else:
                merged_chunks.append(chunk)
        return merged_chunks
        
    for idx, record in enumerate(tqdm(data)):
        chunk_texts = text_splitter.split_text(record['text'])
        chunk_texts = merge_small_chunks(chunk_texts, 250, tiktoken_len)

        # Check if chunk_texts is empty and skip processing the file
        if not chunk_texts:
            print(f"Skipped file: {source_name} (No chunks)")
            should_update_message_id = False
            continue

        # Skip processing the file if the first chunk is smaller than the threshold
        if len(chunk_texts) < 2:
            print(f"Skipped file: {source_name} (Less than two chunks)")
            should_update_message_id = False
            continue

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

    print(f"File: {output_filename}")
    sample_chunk = 5

    if len(chunks) > 0:
        try:
            print("5 random elements in chunks list:\n")
            for i in random.sample(range(len(chunks)), sample_chunk):
                print(f"{i+1}. ID: {chunks[i]['id']}, source: {chunks[i]['source']}, Chunk: {chunks[i]['chunk']}, Date: {chunks[i]['date']}, Namespace: {chunks[i]['namespace']}, Index: {chunks[i]['index']}\nText:\n{chunks[i]['text']}\n")
        except ValueError:
            print(f"There are less than {sample_chunk} elements in the chunks list.\n")
    else:
        print("The chunks list is empty.\n")

    return should_update_message_id, global_chunk_counter
    

if __name__ == "__main__":
    main()