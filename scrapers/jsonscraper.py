import os
import json

def extract_message_info(message):
    author_name = message['author']['name']
    author_id = message['author']['id']

    content = message['content']
    info = {'author_name': author_name, 'author_id': author_id, 'content': content}
    return json.dumps(info)

def get_json_data():
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

    return data
