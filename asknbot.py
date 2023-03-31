import openai
import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Set up the OpenAI API key and Pinecone environment
openai.api_key = openai_api_key
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index_name = pinecone_index_name
index = pinecone.GRPCIndex(index_name)
embed_model = "text-embedding-ada-002"

def create_embedding(text):
    res = openai.Embedding.create(input=[text], engine=embed_model)
    return res['data'][0]['embedding']

def query_pinecone(embedding, top_k=5, include_metadata=True):
    res = index.query(embedding, top_k=top_k, include_metadata=include_metadata)
    return res['matches']

def ask_question(query):
    # Create the query embedding
    xq = create_embedding(query)

    # Retrieve relevant contexts from Pinecone
    matches = query_pinecone(xq)

    # Augment the query with the retrieved contexts
    contexts = [item['metadata']['text'] for item in matches]
    augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query

    # Set up the system message to prime the model
    primer = f"""You are Q&A bot. A highly intelligent system that answers
    user questions based on the information provided by the user above
    each question. All the provided information is from a discord community called: Nomads. 
    If the information cannot be found in the information
    provided by the user, you truthfully say "I don't know".
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

# Example usage
query = """
Is there the possibility someone in Nomads is a spy, even if it's small and tell me the names with evidence
"""
response = ask_question(query)
print(query + "\n" + response)