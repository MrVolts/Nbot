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
# Add a namespace variable (change this as needed)
namespace = "Networking"
openai.api_key = openai_api_key
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index_name = pinecone_index_name
index = pinecone.GRPCIndex(index_name)
embed_model = "text-embedding-ada-002"

def create_embedding(text):
    res = openai.Embedding.create(input=[text], engine=embed_model)
    return res['data'][0]['embedding']

def query_pinecone(embedding, top_k=4, include_metadata=True, namespace=None):
    res = index.query(embedding, top_k=top_k, include_metadata=include_metadata, namespace=namespace)
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
    print("Keywords used:", ', '.join(keywords)+ "\n")
    keyword_query = ' '.join(keywords)
    xq = create_embedding(keyword_query)

    # Retrieve relevant contexts from Pinecone
    matches = query_pinecone(xq, namespace=namespace)

    # Augment the query with the retrieved contexts
    contexts = [item['metadata']['text'] for item in matches]
    augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query

    # Print the prompt given to GPT-3.5
    print("Prompt given to GPT-3.5:")
    print(augmented_query)
    print("\n")

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


# Example usage
query = """
What is the Network core?
"""
response = ask_question(query)
print("Answer" + "\n" + response)
