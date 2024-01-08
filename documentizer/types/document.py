from datetime import datetime
from bson import ObjectId
from pydantic import Base64Bytes, BaseModel, Field
from typing import List, Optional


class Image(BaseModel):
    type: str = 'image'
    image_id: str = Field(default_factory=lambda: str(ObjectId()))
    document_id: str
    page_number: int
    image_base64: Base64Bytes
    image_description: str
    embedding_image: Optional[List[float]] = Field(default_factory=list)
    embedding_text: Optional[List[float]] = Field(default_factory=list)

# represents a chunk of text
class Chunk(BaseModel):
    type: str = 'chunk'
    chunk_id: str = Field(default_factory=lambda: str(ObjectId()))
    document_id: str
    page_number: int
    text: str
    embedding: Optional[List[float]] =  Field(default_factory=list)
    previous_chunk_id: Optional[str] = None
    next_chunk_id: Optional[str] = None

# represents a set document with chunks
class Document(BaseModel):
    type: str = 'document'
    document_id: str = Field(default_factory=lambda: str(ObjectId()))
    date_created: datetime
    date_added: datetime = datetime.utcnow()
    embedding: Optional[List[float]] = Field(default_factory=list)
    chunk_ids: Optional[str] = Field(default_factory=list)
