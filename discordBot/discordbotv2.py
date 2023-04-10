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
    
    
    
                increment_message_count(message.author.id)
            if message.content.startswith("!ai context"):
                await process_context(message)
            elif message.content.startswith("!ai"):
                await process_message(message)
