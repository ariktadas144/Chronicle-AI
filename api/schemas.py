from pydantic import BaseModel
from typing import Optional, Dict, Any

class QueryRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    limit: Optional[int] = 5
    data_type: Optional[str] = "both"
    reasoning_mode: Optional[str] = "summary"
    include_images: Optional[bool] = True
    evidence_strictness: Optional[int] = 7

class MemoryResponse(BaseModel):
    id: str
    text: Optional[str] = None
    image_url: Optional[str] = None
    department: str
    date: str
    outcome: str
    type: str
    location: Optional[str] = None
    tags: Optional[list[str]] = None

class QueryResponse(BaseModel):
    query: str
    memories: list[MemoryResponse]
    reasoning: str
    summary: str

class IngestRequest(BaseModel):
    text: Optional[str] = None
    image_path: Optional[str] = None
    description: Optional[str] = None
    department: str
    date: str
    outcome: str
    type: str
    location: Optional[str] = None
    tags: Optional[list[str]] = None
    document_type: Optional[str] = None
    confidence: Optional[str] = None
    source: Optional[str] = None
    notes: Optional[str] = None
    image_category: Optional[str] = None
    related_event: Optional[str] = None

class UpdateMemoryRequest(BaseModel):
    memory_id: str
    text: Optional[str] = None
    image_path: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None
    date: Optional[str] = None
    outcome: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[list[str]] = None
    confidence: Optional[str] = None
    notes: Optional[str] = None