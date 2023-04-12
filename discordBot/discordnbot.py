import openai
import discord
import asyncio
import io
import json
import datetime
from discord import option
import time
import os
import discord.utils
import pickler
from dotenv import load_dotenv
import pinecone


# guild number, of the server the bot is on
GUILDNO = 711625884771287151
# update frequency in seconds, how often the bot checks for new messages to add to database
update_frequency = 600
# location of where message logs are saved
default_save_path = "../sourcesnbot/"
# Code for handling daily message limit
daily_message_limit = 60
user_message_count = {}
# all channels on the bot's server
channel_names = {}
channel_ids = {}
# attempt to load list of channels to moniter
try:
    file = pickler.load("channels")
    added_channels = file["channels"]
    added_channelids = file["ids"]
except:
    added_channels = {}
    added_channelids = {}
    print("no channel file detected")
# attempt to load the time the bot last checked for new messages
try:
    # load the number of the last time there was an update
    with open("number.txt", "r") as f:
        last_update = float(f.read())#-1000000
except:
    last_update = 1509586802
    print("no number file detected")
# function that runs constantly to update the database


async def save_messages():
    global last_update, added_channelids
    # if server has more than this number of channels being monitered, increase this number.
    channelupdatetime = list([last_update]*1000)
    while True:
        time_updated_readable = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
        print("saving to", time_updated_readable)
        for id in added_channelids[GUILDNO]:
            channel = client.get_channel(id)
            messageblock = []
            try:
                messages = await channel.history(limit=1000000, after=datetime.datetime.fromtimestamp(channelupdatetime[added_channelids[GUILDNO].index(id)])).flatten()
                channelupdatetime[added_channelids[GUILDNO].index(
                    id)] = time.time()

            except discord.Forbidden as e:
                # Handle the specific Forbidden exception
                print("channel "+channel.name +
                      " is not accessible by the bot, removing from logging.")
                index = added_channelids[GUILDNO].index(id)
                del (added_channelids[GUILDNO][index])
                del (added_channels[GUILDNO][index])
                del (channelupdatetime[index])
                save_channels(added_channels, added_channelids, GUILDNO)

                continue
            for message in messages:
                if message.author.bot:
                    continue
                data = {
                    "author": {"id": message.author.id,
                               "name": message.author.name},
                    "content": message.content,
                }
                if data["content"]:
                    messageblock.append(data)
                    
            if messageblock:
                # make a directory if not exists for the guild
                if not os.path.exists(f"{default_save_path}{GUILDNO}"):
                    os.makedirs(f"{default_save_path}{GUILDNO}")
                # save or append the messageblock to a file, with each new item in the list being a new line
                try:
                    with open(f"{default_save_path}{GUILDNO}/{channel.name}.json", "r") as original:
                        data = json.load(original)
                        data["messages"].extend(messageblock)
                except:
                    data = {"messages":messageblock}
                
                with open(f"{default_save_path}{GUILDNO}/{channel.name}.json", "w") as f:
                    f.write(json.dumps(data,indent = 4))
                    #for item in messageblock:
                        # write each item in the list to a new line
                        #f.write(json.dumps(item)+"\n")

                if False:
                    # make a directory if not exists for the varible "time_updated_readable"
                    if not os.path.exists(f"{default_save_path}{GUILDNO}/{time_updated_readable}"):
                        os.makedirs(
                            f"{default_save_path}{GUILDNO}/{time_updated_readable}")
                    # save the contents of messageblock in a file that goes by the name of the channel
                    with open(f"{default_save_path}{GUILDNO}/{time_updated_readable}/{channel.name}.json", "w") as f:
                        json.dump((messageblock), f)  # ,indent = 4)

        last_update = time.time()
        save_number(last_update)
        print("backup done!")
        await asyncio.sleep(update_frequency)
# saves monitered channels to a file


def save_channels(channels, ids, GUILDNO):
    try:
        file = pickler.load("channels")
    except:
        file = {}
        print("no file detected")
    if not file:
        file["channels"] = channels
        file["ids"] = ids
    else:
        file["channels"][GUILDNO] = (channels[GUILDNO])
        file["ids"][GUILDNO] = (ids[GUILDNO])
    pickler.save(file, "channels")
# saves last update time to a file


def save_number(number):
    # save the time the bot last checked for new messages in plain text without using pickler
    with open("number.txt", "w") as f:
        f.write(str(number))


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
        next_reset = next_reset.replace(
            hour=0, minute=0, second=0, microsecond=0)
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
client = discord.Bot(intents=intents)

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
    res = index.query(embedding, top_k=top_k,
                      include_metadata=include_metadata)
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


async def process_context(message, slash_command=False):
    # Split the message by the "!ai context" string and take the second part
    prompt = message.content.split("!ai context")[1]

    # Log the message as a "message" type
    await log_message(message, "context")

    # Use a try-except block to handle any errors that might occur when calling the OpenAI API
    try:
        # Generate a response using the ask_question function
        text = ask_question(prompt)

        # Generate and send the response
        await generate_response(message, text,)
    except:
        # If an error occurs, send a message to the Discord channel
        await message.channel.send("Sorry, something went wrong. Please try again later.")


# Function for generating and sending responses
async def generate_response(message, text):
    # Check if the response is longer than 2000 characters
    if len(text) > 2000:
        # Create a discord.File object with the response text
        response_file = discord.File(io.BytesIO(
            text.encode()), filename="response.txt")

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
    log_file.write(
        f"{message.author.id}: {date_time_str}: {message_type}: {message.content}\n")


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


# asknbot slash command
@client.slash_command(name="asknbot", guild_ids=[GUILDNO], description="nbot is a chatgpt based bot provided with context from this discord")
@option("question", description="Choose a channel to ask nbot", required=True)
async def addchannel(
    ctx: discord.ApplicationContext,
    question: str,
):
    await ctx.defer()
    # check if somone on the blacklist sent it
    if ctx.author.id in blacklist:
        await ctx.respond(content="Sorry, you are blacklisted from using this bot.")
        return
    # check if they have reached the daily message limit
    if check_message_limit(ctx.author.id):
        await ctx.respond(content=f"Sorry, you have reached the daily message limit of {daily_message_limit}. The quota will refresh tomorrow.")
        return
    else:
        increment_message_count(ctx.author.id)
        print(question)
        text = ask_question(question)
        await ctx.respond(content=("```"+text+"```"))

########################## functions for monitering server############################


@client.slash_command(name="addchannel", guild_ids=[GUILDNO], description="Choose a channel to add to monitoring")
@option("addchannel", description="Choose a channel to add to monitoring")
async def addchannel(
    ctx: discord.ApplicationContext,
    addchannel: str,
):
    global added_channelids, added_channels
    try:
        addchannel = int(addchannel)
        # check if channel id is valid
        if addchannel not in channel_ids[GUILDNO]:
            await ctx.respond(content=f"channel not found, Available options are **{', '.join(channel_names[GUILDNO])}**.")
        elif addchannel in added_channelids[GUILDNO]:
            await ctx.respond(content=f"{channel_names[GUILDNO][channel_ids[GUILDNO].index(addchannel)]} already is added.")
        else:
            addchannel = channel_names[GUILDNO][channel_ids[GUILDNO].index(
                addchannel)]

    except:
        addchannel = addchannel.lower()
        if addchannel not in channel_names[GUILDNO]:
            await ctx.respond(content=f"channel not found, Available options are **{', '.join(channel_names[GUILDNO])}**.")
        elif addchannel in added_channels[GUILDNO]:
            await ctx.respond(content=f"{addchannel} already is added.")

        else:
            if addchannel == "allchannels":
                print("here")
                added_channelids[GUILDNO] = list(channel_ids[GUILDNO][1:])
                added_channels[GUILDNO] = list(channel_names[GUILDNO][1:])
            else:
                added_channelids[GUILDNO].append(
                    channel_ids[GUILDNO][channel_names[GUILDNO].index(addchannel)])
                added_channels[GUILDNO].append(addchannel)
            save_channels(added_channels, added_channelids, GUILDNO)
            print("new channel added to monitering:", addchannel)
            await ctx.respond(content=f"channel added! **{', '.join(added_channels[GUILDNO])}**.")


@client.slash_command(name="removechannel", guild_ids=[GUILDNO], description="remove a channel from monitering")
@option("removechannel", description="Choose a channel to remove from monitoring")
async def removechannel(
    ctx: discord.ApplicationContext,
    removechannel: str,
):
    global added_channelids, added_channels
    # if the channel is an integer, convert it to the channel name
    try:
        removechannel = int(removechannel)
        if removechannel not in channel_ids[GUILDNO]:
            await ctx.respond(content=f"channel not found, Available options are **{', '.join(channel_names[GUILDNO])}**.")
        elif removechannel not in added_channelids[GUILDNO]:
            await ctx.respond(content=f"**{channel_names[GUILDNO][channel_ids[GUILDNO].index(removechannel)]}** is not currently being monitored.")
        else:
            removechannel = channel_names[GUILDNO][channel_ids[GUILDNO].index(
                removechannel)]
    except:
        pass

    removechannel = removechannel.lower()
    if removechannel not in added_channels[GUILDNO] and removechannel not in channel_names[GUILDNO]:
        await ctx.respond(content=f"**{removechannel}** does not exist")
    elif removechannel not in added_channels[GUILDNO]:
        await ctx.respond(content=f"**{removechannel}** is not currently being monitored.")
    else:
        index = added_channels[GUILDNO].index(removechannel)
        del added_channels[GUILDNO][index]
        del added_channelids[GUILDNO][index]
        save_channels(added_channels, added_channelids, GUILDNO)
        print(removechannel, "removed from monitering")
        await ctx.respond(content=f"Channel **{removechannel}** removed from monitoring.")


@client.slash_command(name="listchannels", guild_ids=[GUILDNO], description="list monitered channels")
async def listchannels(
    ctx: discord.ApplicationContext,
):
    if not added_channels[GUILDNO]:
        await ctx.respond(content="No channels are currently being monitored.")
    else:
        channel_list = ", ".join(added_channels[GUILDNO])
        await ctx.respond(content=f"The currently monitored channels are:** {channel_list}**.")

########################## ^^functions for monitering server^^############################

# Code for starting daily limit process


@client.event
async def on_ready():
    global channel_ids, channel_names
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(reset_message_count())
    guild = client.get_guild(GUILDNO)
    channels = guild.channels
    channel_name = ["allchannels"]
    channel_id = ["allchannels"]
    for channel in channels:
        if isinstance(channel, discord.TextChannel):
            channel_name.append(channel.name)
            channel_id.append(channel.id)
    channel_names[GUILDNO] = channel_name
    channel_ids[GUILDNO] = channel_id
    if not added_channels:
        added_channelids[GUILDNO] = []
        added_channels[GUILDNO] = []
    await save_messages()

# Discord token
client.run(discord_token)

# author Mr Volts#1468
