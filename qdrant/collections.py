from qdrant_client.http import models
from qdrant.client import get_qdrant_client

def create_memory_collection(collection_name="memories", vector_size=512):
    client = get_qdrant_client()
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE
        )
    )

def delete_collection(collection_name="memories"):
    client = get_qdrant_client()
    client.delete_collection(collection_name=collection_name)