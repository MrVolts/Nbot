import os
from dotenv import load_dotenv
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.utilities import GoogleSearchAPIWrapper

load_dotenv()

os.environ["GOOGLE_CSE_ID"] = os.getenv("GOOGLE_CSE_ID")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

pinecone.init(
    api_key=pinecone_api_key,
    environment=pinecone_environment
)

if pinecone_index_name not in pinecone.list_indexes():
    raise ValueError(
        f"No '{pinecone_index_name}' index exists. You must create the index before "
        "running this notebook. Please refer to the walkthrough at "
        "'github.com/pinecone-io/examples'."
    )

index = pinecone.Index(pinecone_index_name)

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

vectordb = Pinecone(
    index=index,
    embedding_function=embeddings.embed_query,
    text_key="text"
)

llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    temperature=0,
    model_name='gpt-3.5-turbo'
)

retriever = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
)

search = GoogleSearchAPIWrapper()

tools = [
    Tool(
        name='Nomads Discord Message Logs',
        func=retriever.run,
        description="""This tool allows you to query the Pinecone index to get relevant chat logs from the Nomad discord.
        This tool can also be used for follow-up questions from the user.""",
    ),
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
]

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,
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

sys_msg = """You are Nbot, a conversational agent that can answer questions."""

prompt = conversational_agent.agent.create_prompt(
    system_message=sys_msg,
    tools=tools
)

print(conversational_agent.agent.llm_chain.prompt.messages)

# Start conversation loop
while True:
    user_input = input("Enter your question (type 'exit' to end the conversation): ")
    if user_input.lower() == 'exit':
        break

    response = conversational_agent(user_input)
    print(response)


