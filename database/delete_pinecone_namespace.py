import os
import pinecone
from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
namespace_to_delete = "testing"

pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

index = pinecone.GRPCIndex(index_name=pinecone_index_name)

# Delete all vectors within the specified namespace
index.delete(delete_all=True, namespace=namespace_to_delete)