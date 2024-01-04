from pydantic import BaseModel
from typing import List

class Embedding(BaseModel):
    vector: List[float]

class Image(BaseModel):
    document: str
    page: int
    path: str
    text_description: str
    embedding_image: Embedding
    embedding_text: Embedding

# represents a small group of text. ie few sentences
class Chunk(BaseModel):
    document: str
    page: int
    text: str
    embedding_text: Embedding

# represents a set of texts. ie a paragraph or few paragraphs
class TextGroup(BaseModel):
    document: str
    page: int
    texts: List[Chunk]
    embedding_texts: Embedding
