import os
from dotenv import load_dotenv
from openai import OpenAI
from torch import mode
from documentizer.types import Chunk, Document
from typing import Union, List

# vectorizer class should abstract customizability on the embedding model
# cloud or local
# what type of model
class Vectorizer:

    def __init__(self) -> None:
        load_dotenv()
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_vector(self, search_text):
        embedding = self.client.embeddings.create(input=search_text, model='text-embedding-ada-002')
        return embedding.data[0].embedding
    
    # could improve in parallel
    def generate_embedding(self, chunks: List[Union[Chunk, Document]]):
        embedding = self.client.embeddings.create(input=[chunk.text for chunk in chunks], model='text-embedding-ada-002')
        for chunk, embedding in zip(chunks, embedding.data):
            chunk.embedding = embedding.embedding
        return chunks