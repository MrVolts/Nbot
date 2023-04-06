import openai
import discord
import asyncio
import io
import datetime
import os
from dotenv import load_dotenv
import pinecone

# Code for handling daily message limit
daily_message_limit = 10
user_message_count = {}

def check_message_limit(user_id):
    if user_id not in user_message_count:
        user_message_count[user_id] = 0
    if user_message_count[user_id] >= daily_message_limit:
        return True
    return False

def increment_message_count(user_id):
    if user_id not in user_message_count:
        user_message_count[user_id] = 0
    user_message_count[user_id] += 1
    
async def reset_message_count():
    while True:
        user_message_count.clear()
        now = datetime.datetime.now()
        next_reset = now + datetime.timedelta(days=1)
        next_reset = next_reset.replace(hour=0, minute=0, second=0, microsecond=0)
        await asyncio.sleep((next_reset - now).total_seconds())

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
discord_token = os.getenv("DISCORD_TOKEN")

# Initialize Pinecone
openai.api_key = openai_api_key
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index_name = pinecone_index_name
index = pinecone.GRPCIndex(index_name)
embed_model = "text-embedding-ada-002"

# for blacklisting users
blacklist = ["user_id_1", "user_id_2", "user_id_3"]

# Set up the OpenAI API key
openai.api_key = openai_api_key

# https://discordpy.readthedocs.io/en/stable/intents.html
intents = discord.Intents.default()
intents.message_content = True
# Set up the Discord client
client = discord.Client(intents=intents)

# Set up the message and code queues
message_queue = asyncio.Queue()
code_queue = asyncio.Queue()

# Set up the log file
log_file = open("GPT_log.txt", "a")

##########################################################################################
# Functions from asknbot.py                                                              #
##########################################################################################

def create_embedding(text):
    res = openai.Embedding.create(input=[text], engine=embed_model)
    return res['data'][0]['embedding']

def query_pinecone(embedding, top_k=5, include_metadata=True):
    res = index.query(embedding, top_k=top_k, include_metadata=include_metadata)
    return res['matches']

def extract_keywords(question):
    prompt = f"Identify the most relevant keywords from the following question that will help retrieve the best answer. Provide a comma-separated list of these keywords:\n{question}"
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    keywords = res['choices'][0]['message']['content']
    return keywords.strip().split(',')

def ask_question(query):
    # Extract keywords and create the query embedding
    keywords = extract_keywords(query)
    # print("Keywords used:", ', '.join(keywords)+ "\n") DEBUGGING
    keyword_query = ' '.join(keywords)
    xq = create_embedding(keyword_query)

    # Retrieve relevant contexts from Pinecone
    matches = query_pinecone(xq)

    # Augment the query with the retrieved contexts
    contexts = [item['metadata']['text'] for item in matches]
    augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query

    # Print the prompt given to GPT-3.5 DEBUGGING
    '''
    print("Prompt given to GPT-3.5:")
    print(augmented_query)
    print("\n")
    '''

    # Set up the system message to prime the model
    primer = f"""You are Nbot, a bot designed for the Nomads Discord community. For each user request, you will be provided with relevant information gathered from previous Discord chats
    to help you understand the context of the inquiry. Your goal is to respond in the most accurate and relevant manner, using your best judgment while considering the context provided.
    """

    # Send the query to the chatbot
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": primer},
            {"role": "user", "content": augmented_query}
        ]
    )

    response = res['choices'][0]['message']['content']
    return response

# Rest of Code
##########################################################################################

async def process_message(message):
    # Split the message by the !ai string and take the second part
    prompt = message.content.split("!ai")[1]

    # Log the message as a "message" type
    await log_message(message, "message")

    # Use a try-except block to handle any errors that might occur when calling the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            n=1,
            temperature=0.5
        )
        # Get the response text
        text = response['choices'][0]['message']['content']

        # Generate and send the response
        await generate_response(message, text)  
    except:
        # If an error occurs, send a message to the Discord channel
        await message.channel.send("Sorry, something went wrong. Please try again later.")

        
async def process_context(message):
    # Split the message by the "!ai context" string and take the second part
    prompt = message.content.split("!ai context")[1]

    # Log the message as a "message" type
    await log_message(message, "context")

    # Use a try-except block to handle any errors that might occur when calling the OpenAI API
    try:
        # Generate a response using the ask_question function
        text = ask_question(prompt)

        # Generate and send the response
        await generate_response(message, text)  
    except:
        # If an error occurs, send a message to the Discord channel
        await message.channel.send("Sorry, something went wrong. Please try again later.")


# Function for generating and sending responses
async def generate_response(message, text):
    # Check if the response is longer than 2000 characters
    if len(text) > 2000:
        # Create a discord.File object with the response text
        response_file = discord.File(io.BytesIO(text.encode()), filename="response.txt")

        # Send the response file to the Discord channel
        await message.reply(file=response_file)
    else:
        # If the response is not longer than 2000 characters, just send it as a message
        await message.reply("```" + text + "```")

# Function for logging messages
async def log_message(message, message_type):
    # Get the current date and time
    date_time = datetime.datetime.now()
    # Format the date and time using the desired format
    date_time_str = date_time.strftime("%Y-%m-%d %H:%M:%S")

    # Write the user ID, date and time, message type, and prompt to the log file
    log_file.write(f"{message.author.id}: {date_time_str}: {message_type}: {message.content}\n")


@client.event
async def on_message(message):
    # Don't process messages that are sent by the bot itself
    if message.author == client.user:
        return
    if message.author.id in blacklist:
        # If the message author is in the blacklist, do nothing
        return
    if isinstance(message.channel, discord.DMChannel):
        # If the message was sent in a direct message, do nothing
        return
    if message.content.startswith("!ai context") or message.content.startswith("!ai"):
        if check_message_limit(message.author.id):
            await message.reply(f"Sorry, you have reached the daily message limit of {daily_message_limit}. The quota will refresh tomorrow.")
        else:
            increment_message_count(message.author.id)
            if message.content.startswith("!ai context"):
                await process_context(message)
            elif message.content.startswith("!ai"):
                await process_message(message)

# Code for starting daily limit process
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(reset_message_count())
# Discord token
client.run(discord_token)

#author Mr Volts#1468
