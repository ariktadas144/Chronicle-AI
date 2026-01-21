from qdrant_client import QdrantClient
import os

def get_qdrant_client():
    url = os.getenv("QDRANT_URL", "./qdrant_storage")
    if url == ":memory:":
        return QdrantClient(":memory:")
    elif "://" in url:
        return QdrantClient(url=url)
    else:
        return QdrantClient(path=url)