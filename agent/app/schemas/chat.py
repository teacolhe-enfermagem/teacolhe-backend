from pydantic import BaseModel
from typing import List

class Metrics(BaseModel):
    documents_found: int
    sources_used: List[str]

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    metrics: Metrics