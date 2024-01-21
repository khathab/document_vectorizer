import os
from dotenv import load_dotenv
import cohere
from documentizer.types import Chunk, Document
from typing import Union, List

# vectorizer class should abstract customizability on the embedding model
# cloud or local
# what type of model
class Vectorizer:

    def __init__(self) -> None:
        load_dotenv()
        COHERE_API_KEY = os.environ.get('COHERE_API_KEY')
        self.client = cohere.Client(api_key=COHERE_API_KEY)

    def generate_vector(self, search_text):
        return self.client.embed([search_text], 'embed-english-v3.0', input_type='search_query').embeddings[0]

    def generate_embedding(self, chunks: List[Union[Chunk, Document]]):
        embeddings = self.client.embed([chunk.text for chunk in chunks],'embed-english-v3.0', input_type='search_document')
        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding
        return chunks