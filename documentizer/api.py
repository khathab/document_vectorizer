from .vectorizer import Vectorizer
from .chunking import Chunker
from .database import Database
from .types import Document, Chunk

class Documentizer:

    def __init__(self) -> None:
        self.chunker = Chunker(400)
        self.vectorizer = Vectorizer()
        self.database = Database()

    def add_document(self, path):
        document, chunks = self.chunker.chunk_evenly(path)
        chunks = self.vectorizer.generate_embedding(chunks)
        self.database.add_documents(chunks)

    def search_document(self, search_query):
        vector = self.vectorizer.generate_vector(search_query)
        result = self.database.search_document(vector, 'chunk')
        return result