from pydantic import BaseModel
from typing import Optional

class MemoryItem(BaseModel):
    id: str
    text: Optional[str] = None
    image_url: Optional[str] = None
    department: str
    date: str
    outcome: str
    type: str
    location: Optional[str] = None
    tags: Optional[list[str]] = None

class QueryFilters(BaseModel):
    department: Optional[str] = None
    outcome: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    tags: Optional[list[str]] = None