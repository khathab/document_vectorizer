from .vectorizer import Vectorizer
from .chunking import Chunker
from .database import Database
from .search import SearchAgent

class Documentizer:
    def __init__(self) -> None:
        self.chunker = Chunker(400)
        self.vectorizer = Vectorizer()
        self.database = Database()
        self.search_agent = SearchAgent()

    def add_document(self, path):
        document, chunks = self.chunker.chunk_evenly(path)
        chunks = self.vectorizer.generate_embedding(chunks)
        self.database.add_documents(chunks)

    def search_documents(self, search_query):
        result = self.search_agent.search(search_query)
        return result