from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class QueryRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    limit: Optional[int] = 5
    data_type: Optional[str] = "both"  # "text", "image", or "both"
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
    type: str  # "text" or "image"
    location: Optional[str] = None
    tags: Optional[List[str]] = None


class QueryResponse(BaseModel):
    query: str
    memories: List[MemoryResponse]
    reasoning: str
    summary: str


# -------------------------------
# Ingestion Models
# -------------------------------

class IngestRequest(BaseModel):
    # One of these must be provided depending on type
    text: Optional[str] = None
    image_path: Optional[str] = None
    description: Optional[str] = None

    # Required fields
    department: str = Field(..., description="Responsible department")
    date: str = Field(..., description="Date of the event/document")
    outcome: str = Field(..., description="Outcome e.g., success/failure/mixed")
    type: str = Field(..., description="Memory type: 'text' or 'image'")

    # Optional metadata
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    document_type: Optional[str] = None
    confidence: Optional[str] = None
    source: Optional[str] = None
    notes: Optional[str] = None
    image_category: Optional[str] = None
    related_event: Optional[str] = None


# -------------------------------
# Memory Update Models
# -------------------------------

class UpdateMemoryRequest(BaseModel):
    memory_id: str

    # Optional fields for updating memory
    text: Optional[str] = None
    image_path: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None
    date: Optional[str] = None
    outcome: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    confidence: Optional[str] = None
    notes: Optional[str] = None
    type: Optional[str] = None
    document_type: Optional[str] = None
    image_category: Optional[str] = None
    related_event: Optional[str] = None
