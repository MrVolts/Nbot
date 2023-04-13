import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Set up the Pinecone environment
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index_name = pinecone_index_name

def clear_index(index_name):
    # Check if the index exists
    if index_name in pinecone.list_indexes():
        # Delete the index
        pinecone.delete_index(index_name)
        print(f"Deleted index: {index_name}")

        # Recreate the index
        dimension = 1536  # Update this with the correct dimension for your embeddings
        pinecone.create_index(index_name, dimension=dimension, metric='dotproduct')
        print(f"Recreated index: {index_name}")
    else:
        print(f"Index '{index_name}' does not exist.")

# Clear the index
clear_index(index_name)