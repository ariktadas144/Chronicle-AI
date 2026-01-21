from qdrant.search import search_memories, build_filter
from memory.schema import MemoryItem, QueryFilters

class MemoryManager:
    def __init__(self, collection_name="memories"):
        self.collection_name = collection_name

    def retrieve_memories(self, query: str, filters: QueryFilters = None, limit=5):
        qdrant_filter = None
        if filters:
            qdrant_filter = build_filter(
                department=filters.department,
                outcome=filters.outcome,
                type_filter=filters.type,
                location=filters.location,
                date_from=filters.date_from,
                date_to=filters.date_to,
                tags=filters.tags
            )

        results = search_memories(query, self.collection_name, limit, qdrant_filter)

        memories = []
        for result in results:
            payload = result.payload
            memory = MemoryItem(
                id=str(result.id),
                text=payload.get('text'),
                image_url=payload.get('image_url'),
                department=payload.get('department', ''),
                date=payload.get('date', ''),
                outcome=payload.get('outcome', ''),
                type=payload.get('type', ''),
                location=payload.get('location'),
                tags=payload.get('tags')
            )
            memories.append(memory)

        return memories