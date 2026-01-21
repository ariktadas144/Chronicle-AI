from fastapi import FastAPI, HTTPException
from api.schemas import QueryRequest, QueryResponse, MemoryResponse, IngestRequest, UpdateMemoryRequest
from memory.schema import QueryFilters
import traceback

app = FastAPI(title="Chronicle AI - Institutional Memory Agent API")

_memory_manager = None
_recommendation_engine = None

def get_memory_manager():
    global _memory_manager
    if _memory_manager is None:
        from memory.memory_manager import MemoryManager
        _memory_manager = MemoryManager()
    return _memory_manager

def get_recommendation_engine():
    global _recommendation_engine
    if _recommendation_engine is None:
        from reasoning.recommendation import RecommendationEngine
        _recommendation_engine = RecommendationEngine()
    return _recommendation_engine

@app.get("/")
async def root():
    return {
        "message": "Chronicle AI - Institutional Memory Agent API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "POST /query": "Query institutional memory",
            "POST /ingest": "Ingest new document or image",
            "PUT /update/{memory_id}": "Update existing memory",
            "GET /docs": "Interactive API documentation"
        }
    }

@app.post("/query", response_model=QueryResponse)
async def query_memories(request: QueryRequest):
    try:
        memory_manager = get_memory_manager()
        recommendation_engine = get_recommendation_engine()

        filters = QueryFilters(**request.filters) if request.filters else QueryFilters()

        if request.data_type and request.data_type != "both":
            filters.type = request.data_type

        memories = memory_manager.retrieve_memories(
            request.query,
            filters,
            request.limit
        )

        if request.reasoning_mode == "recommendation":
            reasoning = recommendation_engine.generate_recommendation(request.query, memories)
        elif request.reasoning_mode == "comparison":
            reasoning = f"Comparing retrieved memories: {len(memories)} items found."
        else:
            reasoning = f"Summary of {len(memories)} relevant memories."

        summary = recommendation_engine.get_summary(request.query, memories)

        memory_responses = [
            MemoryResponse(
                id=m.id,
                text=getattr(m, 'text', None),
                image_url=getattr(m, 'image_url', None),
                department=m.department,
                date=m.date,
                outcome=m.outcome,
                type=m.type,
                location=m.location,
                tags=getattr(m, 'tags', None)
            ) for m in memories
        ]

        return QueryResponse(
            query=request.query,
            memories=memory_responses,
            reasoning=reasoning,
            summary=summary
        )

    except Exception as e:
        import traceback
        print(f"Error in query: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest_document(request: IngestRequest):
    try:
        from qdrant.ingest import ingest_single_document

        metadata = {
            "department": request.department,
            "date": request.date,
            "outcome": request.outcome,
            "type": request.type,
            "location": request.location,
            "tags": request.tags,
            "document_type": request.document_type,
            "confidence": request.confidence,
            "source": request.source,
            "notes": request.notes,
            "image_category": request.image_category,
            "related_event": request.related_event
        }
        metadata = {k: v for k, v in metadata.items() if v is not None}

        ingest_single_document(text=request.text or request.description, image_path=request.image_path, metadata=metadata)
        return {"message": f"{request.type.capitalize()} ingested successfully"}
    except Exception as e:
        import traceback
        print(f"Error in ingest: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/update/{memory_id}")
async def update_memory(memory_id: str, request: UpdateMemoryRequest):
    try:
        from qdrant.ingest import update_memory_document

        update_data = {
            "text": request.text,
            "image_path": request.image_path,
            "description": request.description,
            "department": request.department,
            "date": request.date,
            "outcome": request.outcome,
            "location": request.location,
            "tags": request.tags,
            "confidence": request.confidence,
            "notes": request.notes
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}

        update_memory_document(memory_id, update_data)
        return {"message": f"Memory {memory_id} updated successfully"}
    except Exception as e:
        import traceback
        print(f"Error in update: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}