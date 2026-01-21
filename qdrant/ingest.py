import json
from qdrant_client.http import models
from qdrant.client import get_qdrant_client
from embeddings.text_embedder import TextEmbedder
from embeddings.image_embedder import ImageEmbedder
import hashlib
import os
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_documents(documents_path="data/processed/documents.json",
                     metadata_path="data/processed/metadata.json",
                     collection_name="memories"):
    embedder = TextEmbedder()
    client = get_qdrant_client()

    with open(documents_path, 'r') as f:
        documents = json.load(f)

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    points = []
    for doc, meta in zip(documents, metadata):
        vector = embedder.embed(doc['text'])
        payload = {**meta, "text": doc['text']}
        points.append(
            models.PointStruct(
                id=int(doc['id']),
                vector=vector,
                payload=payload
            )
        )

    client.upsert(collection_name=collection_name, points=points)
    print(f"Ingested {len(points)} documents into {collection_name}")

def ingest_single_document(text: Optional[str] = None, image_path: Optional[str] = None, metadata: Optional[dict] = None, collection_name="memories"):
    if metadata is None:
        metadata = {}
    client = get_qdrant_client()
    payload = metadata.copy()

    vector = None
    if metadata.get("type") == "text" and text:
        embedder = TextEmbedder()
        vector = embedder.embed(text)
        payload["text"] = text
        logger.info(f"Qdrant Ingest - Text embedding created, dimensions: {len(vector)}")
    elif metadata.get("type") == "image" and image_path:
        embedder = ImageEmbedder()
        vector = embedder.embed(image_path)
        payload["image_url"] = image_path
        if text:
            payload["text"] = text
        logger.info(f"Qdrant Ingest - Image embedding created, dimensions: {len(vector)}, file: {image_path}")
    else:
        raise ValueError("Invalid type or missing content")

    content = text if text else image_path
    content_hash = hashlib.md5((content + str(metadata)).encode()).hexdigest()
    doc_id = int(content_hash[:16], 16)

    point = models.PointStruct(
        id=doc_id,
        vector=vector,
        payload=payload
    )

    client.upsert(collection_name=collection_name, points=[point])
    logger.info(f"Qdrant Ingest - Successfully stored {metadata['type']} in collection '{collection_name}' with ID {doc_id}")
    print(f"Ingested {metadata['type']} into {collection_name} with ID {doc_id}")

def update_memory_document(memory_id: str, update_data: dict, collection_name="memories"):
    client = get_qdrant_client()

    try:
        existing_points = client.retrieve(collection_name=collection_name, ids=[int(memory_id)])
        if not existing_points:
            raise ValueError(f"Memory with ID {memory_id} not found")

        existing_point = existing_points[0]
        current_payload = existing_point.payload
        current_vector = existing_point.vector

        updated_payload = current_payload.copy()
        updated_payload.update(update_data)

        vector_updated = False
        if 'text' in update_data and update_data['text'] and current_payload.get('type') == 'text':
            embedder = TextEmbedder()
            current_vector = embedder.embed(update_data['text'])
            vector_updated = True
            logger.info(f"Qdrant Update - Re-embedded text, dimensions: {len(current_vector)}")
        elif 'image_path' in update_data and update_data['image_path'] and current_payload.get('type') == 'image':
            embedder = ImageEmbedder()
            current_vector = embedder.embed(update_data['image_path'])
            updated_payload['image_url'] = update_data['image_path']
            vector_updated = True
            logger.info(f"Qdrant Update - Re-embedded image, dimensions: {len(current_vector)}")

        updated_point = models.PointStruct(
            id=int(memory_id),
            vector=current_vector,
            payload=updated_payload
        )

        client.upsert(collection_name=collection_name, points=[updated_point])
        logger.info(f"Qdrant Update - Successfully updated memory {memory_id} in collection '{collection_name}'")
        print(f"Updated memory {memory_id} in {collection_name}")

    except Exception as e:
        logger.error(f"Qdrant Update failed for memory {memory_id}: {str(e)}")
        raise

def ingest_images(images_dir="data/raw/images", collection_name="memories"):
    embedder = ImageEmbedder()
    client = get_qdrant_client()

    points = []
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(images_dir, filename)
            vector = embedder.embed(image_path)
            metadata = {
                "id": filename,
                "department": "Unknown",
                "date": "2024-01-01",
                "outcome": "unknown",
                "type": "image",
                "tags": []
            }
            payload = {**metadata, "image_url": image_path}
            points.append(
                models.PointStruct(
                    id=hash(filename) % 1000000,
                    vector=vector,
                    payload=payload
                )
            )

    if points:
        client.upsert(collection_name=collection_name, points=points)
        print(f"Ingested {len(points)} images into {collection_name}")
    else:
        print("No images found to ingest")