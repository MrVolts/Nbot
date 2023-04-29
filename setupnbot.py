Mr Volts
#1468



Text Channel
Outplay:announcements
Search

announcements chat
6 April 2023

Mr Volts — 06/04/2023 00:49
list and delete
[00:49]
maybe a bash file that can take arguments
[00:50]
I wanna beable to string multiple lists together e.g list namespace, channel, datetime
[00:51]
and have logs for everything added

Mr Volts — 06/04/2023 00:56
doesn't seem to delete the vector from pinecone
[00:56]
figure out how to use this:

import pinecone

pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENVIRONMENT")
index = pinecone.Index("example-index")

delete_response = index.delete(ids=["vec1", "vec2"], namespace="example-namespace")
[00:58]
I should get databasehandler to have a delete id function where it is fed the vector and it's namespace

Mr Volts — 06/04/2023 01:09
I verfified this works:

index.delete(ids=["0e3b3851-6dd6-40c6-af17-49933e166874"], namespace="testing")

Mr Volts — 06/04/2023 14:17
database_handler.py:

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, and_, func, select
import datetime
import os

Expand
message.txt
9 KB

Mr Volts — 06/04/2023 16:19


Mr Volts — 06/04/2023 16:36

[16:40]


Mr Volts — 06/04/2023 17:01

[17:01]


Mr Volts — 06/04/2023 17:10
index.delete(delete_all=True, namespace="testing")
7 April 2023

Mr Volts — 07/04/2023 01:42
Read z paper

Mr Volts — 07/04/2023 16:58


Mr Volts — 07/04/2023 17:53
https://www.youtube.com/watch?v=CfuhRVM1ntQ&t=155s
YouTube
James Briggs
Lex Fridman Podcast Chatbot with LangChain Agents + GPT 3.5

[17:54]
https://www.youtube.com/watch?v=eqOfr4AGLk8
YouTube
James Briggs
LangChain Data Loaders, Tokenizers, Chunking, and Datasets - Data P...

[17:54]
https://www.youtube.com/watch?v=rxE7xBzYU_o&t=634s
YouTube
James Briggs
OpenAI's ChatGPT API First Look

8 April 2023

Mr Volts — 08/04/2023 02:24
https://soundraw.io/edit_music?length=180&tempo=low,normal,high&mood=Dark
Soundraw
Your personal AI music generator.

[02:28]
https://beta.elevenlabs.io/https://www.youtube.com/watch?v=gpP_YEv_9jA
[02:29]
https://www.youtube.com/watch?v=gpP_YEv_9jA
YouTube
Obscurious
I Tried 200 AI Tools, These are the Best


Mr Volts — 08/04/2023 03:07
https://www.steamship.com/build/langchain-apps?ref=futuretools.io
Steamship
LangChain Apps - Steamship
Host managed LangChain Apps in seconds.


Mr Volts — 08/04/2023 03:17
https://github.com/logspace-ai/langflow
GitHub
GitHub - logspace-ai/langflow: ⛓️ LangFlow is a UI for LangChain, d...
⛓️ LangFlow is a UI for LangChain, designed with react-flow to provide an effortless way to experiment and prototype flows. - GitHub - logspace-ai/langflow: ⛓️ LangFlow is a UI for LangChain, desig...


Mr Volts — 08/04/2023 03:30
https://github.com/hwchase17/chat-langchain
GitHub
GitHub - hwchase17/chat-langchain
Contribute to hwchase17/chat-langchain development by creating an account on GitHub.

11 April 2023

Mr Volts — 11/04/2023 02:09
https://huggingface.co/docs/huggingface_hub/v0.13.4/guides/download
Download files from the Hub
12 April 2023

Mr Volts — 12/04/2023 02:24
https://www.strengthside.com/bulletproof-knees-routine
Join Guided for $19 (Daily Exclusive)

Mr Volts — 12/04/2023 22:28
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, and_, func, select
from sqlalchemy.orm import declarative_base, Session
import datetime
import os

Base = declarative_base()
Expand
message.txt
5 KB
13 April 2023

Mr Volts — 13/04/2023 00:35
https://youtu.be/pmpy_ZFIiaA?t=799
YouTube
Here's the Deal
MUST SEE: Cops Flip Script on ATF Agent Tased for NOT COMPLYING


Mr Volts — 13/04/2023 12:18
To stop files from being deleted after processing and to only load input data past the last processed message_id, you can follow these steps:

Replace the os.remove(input_filepath) line in the main() function with # os.remove(input_filepath) to prevent the deletion of files after processing.

Update the load_input_data() function to only load data past the last processed message_id. In order to do this, you can read the contents of the chunk_counter.txt file and check if the message_id exists in the data. If it exists, only load data past that point.

Expand
message.txt
9 KB
14 April 2023

Mr Volts — 14/04/2023 13:00
https://github.com/yoheinakajima/babyagi
GitHub
GitHub - yoheinakajima/babyagi
Contribute to yoheinakajima/babyagi development by creating an account on GitHub.
15 April 2023

Mr Volts — 15/04/2023 23:49
Goal 1: You are to optimise the code in the database folder. Currently only the database and chunker are set up
Goal 2: I would like you to research how Custom trained AI chatbots using langchain, long term memory and LLM's such as openai gpt3.5 can be made gpt-3.5-turbo with minimal cost
Goal 3: I would like you to build upon the code in the database folder to produce the backend and an API interface for the chatbot using research gathered in the previous step
Goal 4: I want you to then implement extra feautures such as tools and
16 April 2023

Mr Volts — 16/04/2023 00:15
Nbot here!  I am at Request failed with status code: 400
Response content: b'{"detail":{"status":"invalid_uid","message":"An invalid ID has been received: 'your-voice-id-1'. Make sure to provide a correct one."}}'
your service.
Describe your AI's role:  For example, 'an AI designed to autonomously develop and run businesses with the sole goal of increasing your net worth.'
Nbot is: an innovative AI expert programmer designed to autonomously build applications
Enter up to 5 goals for your AI:  For example: Increase net worth, Grow Twitter Account, Develop and manage multiple businesses autonomously'
Enter nothing to load defaults, enter nothing when finished.
Goal 1: you are to optimise the code in the database folder ignore the gpt-discord-bot-main for now. Currently only the database and chunker are set up
Goal 2: I would like you to research how Custom trained AI chatbots using langchain, long term memory (chroma) and LLM's such as openai gpt3.5 can be made gpt-3.5-turbo with minimal cost and maximum peformance on a server with 4 VCPU's, 24gb of memory and 200gb of storage. Make sure to post your findings in a detailed research paper in a researchpaper.txt file
Goal 3: I would like you to build upon the code in the database folder to produce the backend and an easy to use API interface for the chatbot using research gathered in the previous step. Make sure it can use langchain tools to access different databases and it is easy to produce custom chatbots by feeding them context. Produce documentation for the code as documentation.txt
Goal 4:

Mr Volts — 16/04/2023 01:17
################################################################################
### AUTO-GPT - GENERAL SETTINGS
################################################################################
# EXECUTE_LOCAL_COMMANDS - Allow local command execution (Example: False)
EXECUTE_LOCAL_COMMANDS=False
# BROWSE_CHUNK_MAX_LENGTH - When browsing website, define the length of chunk stored in memory
Expand
message.txt
6 KB
17 April 2023

Mr Volts — 17/04/2023 18:20
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=0,
    return_messages=True,
)

conversational_agent = initialize_agent(
    agent='chat-conversational-react-description', 
    tools=tools, 
    llm=llm,
    verbose=True,
    max_iterations=5,
    early_stopping_method="generate",
    memory=memory,
)

sys_msg = """You are Nbot, a conversational agent that can answer questions.
    """

prompt = conversational_agent.agent.create_prompt(
    system_message=sys_msg,
    tools=tools
)
conversational_agent.agent.llm_chain.prompt = prompt  # can just do conversational_agent.agent.llm_chain.prompt to use default prompt

#########################
#      Conversation     #
#########################

print(conversational_agent.agent.llm_chain.prompt.messages)


conversational_agent("Who is Issac Newton?")
19 April 2023

Mr Volts — 19/04/2023 13:32

21 April 2023

Mr Volts — 21/04/2023 17:02


Mr Volts — 21/04/2023 20:12
https://github.com/microsoft/semantic-kernel?utm_source=tlrdai
GitHub
GitHub - microsoft/semantic-kernel: Integrate cutting-edge LLM tech...
Integrate cutting-edge LLM technology quickly and easily into your apps - GitHub - microsoft/semantic-kernel: Integrate cutting-edge LLM technology quickly and easily into your apps

22 April 2023

Mr Volts — 22/04/2023 17:42
Integrate the information on these slides into the lecture notes

Slide 1:

Types and data encoding
How do we encode MiniJava values of different types using a single word?

int: signed (two's complement) integer
boolean: 0 for false; 1 for true
int[]: pointer to block of memory storing array
object types: pointer to a block of memory storing the object
This makes determining the memory layout for compiled programs easy: the memory needed for n values is always n words.

Slide 2:

Types and data encoding
Java:
long and double are 64-bit values, so 2 words on a 32-bit processor.
There is a fixed bound on the number of words needed to store a value.
C:
Often, long will be larger than machine word size.
struct (and hence C++ objects) are values and can be passed to/received from functions.
No fixed bound on number of words needed to store a value.
For a more complicated language, you need to know the type of each stored variable and the size of each type to determine memory layout.
23 April 2023

Mr Volts — 23/04/2023 17:38

[17:38]
Jj

Mr Volts — 23/04/2023 19:39
Summarize a lecture video transcript into structured notes in Markdown format using natural language processing. Identify main topics, create an outline, generate concise summaries for each section, and compile them into cohesive notes. Capture all important details, use clear language, avoid repetition, and format the notes using Markdown syntax.

Lecture Video Transcript:

You want to pause context-free grammars efficiently. We're going to use Earley's 
algorithm. The idea in Earley's algorithm is that we're going to look at each 
Expand
message.txt
11 KB
[19:40]
Pages34-36
[19:42]
Summarize a lecture video transcript into structured notes in Markdown format using natural language processing. Identify main topics, create an outline, generate concise summaries for each section, and compile them into cohesive notes. Capture all important details, use clear language, avoid repetition, and format the notes using Markdown syntax.

Lecture Video Transcript:

Earley's algorithm is a very elegant algorithm. It pauses all context-free 
grammars. It's not completely obvious. But once you understand a grammar flow 
Expand
message.txt
5 KB
24 April 2023

Mr Volts — 24/04/2023 15:21
https://wandb.ai/wandb/wb-announcements/reports/Introducing-W-B-Prompts-The-Present-Future-of-LLMOps--Vmlldzo0MTI4NjY5?utm_source=tldrai
W&B
Introducing W&B Prompts
Learn all about W&B's new LLMOps tools and how to use them. Made by Justin Tenuto using Weights & Biases

26 April 2023

Mr Volts — 26/04/2023 12:53

27 April 2023

Mr Volts — 27/04/2023 09:38
3985

Mr Volts — 27/04/2023 15:46
Benjamin Paul Cherry
28 April 2023

Mr Volts — Yesterday at 13:18
I'm really sorry I missed the deadline for module selection and any hassle that occurs because of it. I thought it was due in later due to my diagnosed ADHD and didn't realise it was in fact yesterday till today. I'd really appreciate if you accepted my list:

Data Science Algorithms and Tools    - CS3AI18
Blockchain Computing - CS3BC20
Data Integration and Visualisation - CS3DV20
Image Analysis - CS3IA16
Text Mining and Natural Language Processing - CS3TM20
Visual Intelligence - CS3VI18
Virtual Reality - CS3VR16

For a total of 70 credits.

Thankyou.
29 April 2023

Mr Volts — Today at 14:45
import os
import datetime
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from tqdm.auto import tqdm
import openai
import pinecone
from time import sleep
from dotenv import load_dotenv
from dateutil.parser import parse
import random
from scrapers.webscraper import WebScraper
from database.database_handler import DatabaseHandler

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")


data = []
chunks = []
websitescraper_data = []

# Add a namespace variable (change this as needed)
namespace = "testing"

url = "https://docs.pinecone.io/docs"

websitescraper_data = []

# Initialize the WebScraper class with a base_url
base_url = "https://docs.pinecone.io"
scraper = WebScraper(base_url)

# Call the scrape_text method with the starting URL, websitescraper_data, and the desired depth
max_depth = 1
scraper.scrape_text(url, websitescraper_data, max_depth=max_depth)

# Replace the previous appending line with the following line
data.extend(websitescraper_data)

# Get JSON data
# json_data = get_json_data()
# data.extend(json_data)

# Tokenizer and text splitter
tokenizer = tiktoken.get_encoding('p50k_base')

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
    separators=[", {", "\n\n", "\n", " ", ""]
)

for idx, record in enumerate(tqdm(data)):
    texts = text_splitter.split_text(record['text'])

    # Include the timestamp at the start of the chunk
    chunks.extend([{
        'id': str(uuid4()),
        'text': "{" + texts[i],
        'chunk': i,
        'channel': record['channel']
    } for i in range(len(texts))])

# Print 5 random elements from the chunks list with full text
print("5 random elements in chunks list:")
for i in random.sample(range(len(chunks)), 5):
    print(f"{i+1}. ID: {chunks[i]['id']}, Channel: {chunks[i]['channel']}, Chunk: {chunks[i]['chunk']}\nText:\n{chunks[i]['text']}\n")

# Initialize openai API key
openai.api_key = openai_api_key

embed_model = "text-embedding-ada-002"

res = openai.Embedding.create(
    input=[
        "Sample document text goes here",
        "there will be several phrases in each batch"
    ], engine=embed_model
)

index_name = pinecone_index_name

# Initialize connection to Pinecone
pinecone.init(
    api_key=pinecone_api_key,
    environment=pinecone_environment
... (56 lines left)
Collapse
message.txt
5 KB
[14:51]

[14:51]


Message #announcements
﻿




Members list for announcements (channel)
ADMINS, 1 MEMBERADMINS — 1

Mr Volts
BOT, 2 MEMBERSBOT — 2

T1
BOT
Playing back soon!

YOUR BOSS
BOT
Playing dyno.gg | ?help
import os
import datetime
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from tqdm.auto import tqdm
import openai
import pinecone
from time import sleep
from dotenv import load_dotenv
from dateutil.parser import parse
import random
from scrapers.webscraper import WebScraper
from database.database_handler import DatabaseHandler

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")


data = []
chunks = []
websitescraper_data = []

# Add a namespace variable (change this as needed)
namespace = "testing"

url = "https://docs.pinecone.io/docs"

websitescraper_data = []

# Initialize the WebScraper class with a base_url
base_url = "https://docs.pinecone.io"
scraper = WebScraper(base_url)

# Call the scrape_text method with the starting URL, websitescraper_data, and the desired depth
max_depth = 1
scraper.scrape_text(url, websitescraper_data, max_depth=max_depth)

# Replace the previous appending line with the following line
data.extend(websitescraper_data)

# Get JSON data
# json_data = get_json_data()
# data.extend(json_data)

# Tokenizer and text splitter
tokenizer = tiktoken.get_encoding('p50k_base')

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
    separators=[", {", "\n\n", "\n", " ", ""]
)

for idx, record in enumerate(tqdm(data)):
    texts = text_splitter.split_text(record['text'])

    # Include the timestamp at the start of the chunk
    chunks.extend([{
        'id': str(uuid4()),
        'text': "{" + texts[i],
        'chunk': i,
        'channel': record['channel']
    } for i in range(len(texts))])

# Print 5 random elements from the chunks list with full text
print("5 random elements in chunks list:")
for i in random.sample(range(len(chunks)), 5):
    print(f"{i+1}. ID: {chunks[i]['id']}, Channel: {chunks[i]['channel']}, Chunk: {chunks[i]['chunk']}\nText:\n{chunks[i]['text']}\n")

# Initialize openai API key
openai.api_key = openai_api_key

embed_model = "text-embedding-ada-002"

res = openai.Embedding.create(
    input=[
        "Sample document text goes here",
        "there will be several phrases in each batch"
    ], engine=embed_model
)

index_name = pinecone_index_name

# Initialize connection to Pinecone
pinecone.init(
    api_key=pinecone_api_key,
    environment=pinecone_environment
)

# Check if index already exists (it shouldn't if this is first time)
if index_name not in pinecone.list_indexes():
    # If does not exist, create index
    pinecone.create_index(
        index_name,
        dimension=len(res['data'][0]['embedding']),
        metric='dotproduct'
    )
# Connect to index
index = pinecone.GRPCIndex(index_name)
# View index stats
index.describe_index_stats()

db_handler = DatabaseHandler(index)

# Your existing code for processing the data

batch_size = 100

for i in tqdm(range(0, len(chunks), batch_size)):
    # Find end of batch
    i_end = min(len(chunks), i + batch_size)
    meta_batch = chunks[i:i_end]
    # Get ids
    ids_batch = [x['id'] for x in meta_batch]
    # Get texts to encode
    texts = [x['text'] for x in meta_batch]
    # Create embeddings (try-except added to avoid RateLimitError)
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
    # Cleanup metadata
    meta_batch = [{
        'id': x['id'],
        'text': x['text'],
        'chunk': x['chunk'],
        'channel': x['channel']
    } for x in meta_batch]
    to_upsert = list(zip(ids_batch, embeds, meta_batch))
    # Upsert to Pinecone
    index.upsert(vectors=to_upsert, namespace=namespace)
    
    # Use a database connection to store Pinecone block information
    for record in meta_batch:
        db_handler.insert_block(record['id'], record['channel'], namespace=namespace, created_at=datetime.datetime.utcnow())
