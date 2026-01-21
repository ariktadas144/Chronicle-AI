from qdrant_client.http import models
from qdrant.client import get_qdrant_client
from embeddings.text_embedder import TextEmbedder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_memories(query: str, collection_name="memories", limit=5, filters=None):
    embedder = TextEmbedder()
    client = get_qdrant_client()

    query_vector = embedder.embed(query)
    logger.info(f"Qdrant Search - Query: '{query}', Vector dimensions: {len(query_vector)}, Collection: {collection_name}")

    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit,
        query_filter=filters
    )

    for i, result in enumerate(search_result):
        logger.info(f"Result {i+1}: ID={result.id}, Score={result.score:.4f}, Type={result.payload.get('type', 'unknown')}")

    logger.info(f"Qdrant Search completed - Found {len(search_result)} results")
    return search_result

def build_filter(department=None, date_from=None, date_to=None, outcome=None, type_filter=None, location=None, tags=None):
    conditions = []
    if department:
        conditions.append(models.FieldCondition(
            key="department",
            match=models.MatchValue(value=department)
        ))
    if outcome:
        conditions.append(models.FieldCondition(
            key="outcome",
            match=models.MatchValue(value=outcome)
        ))
    if type_filter:
        conditions.append(models.FieldCondition(
            key="type",
            match=models.MatchValue(value=type_filter)
        ))
    if location:
        conditions.append(models.FieldCondition(
            key="location",
            match=models.MatchValue(value=location)
        ))
    if tags:
        tag_conditions = []
        for tag in tags:
            tag_conditions.append(models.FieldCondition(
                key="tags",
                match=models.MatchValue(value=tag)
            ))
        if tag_conditions:
            conditions.append(models.FieldCondition(
                key="tags",
                match=models.MatchAny(any=tag_conditions)
            ))
    if date_from or date_to:
        date_conditions = {}
        if date_from:
            date_conditions["gte"] = date_from
        if date_to:
            date_conditions["lte"] = date_to
        conditions.append(models.FieldCondition(
            key="date",
            range=models.DatetimeRange(**date_conditions)
        ))

    return models.Filter(must=conditions) if conditions else None