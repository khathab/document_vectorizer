# An agent that searches through the database
from ..vectorizer import Vectorizer
from ..database import Database
import cohere
from dotenv import load_dotenv
import os

class SearchAgent:
    def __init__(self) -> None:
        load_dotenv()
        COHERE_API_KEY = os.environ.get('COHERE_API_KEY')
        self.client = cohere.Client(COHERE_API_KEY)
        self.vectorizer = Vectorizer()
        self.database = Database()

    def iterate_over_top(self, generator, k):
        results = []
        for _ in range(k):
            try:
                results.append(next(generator))
            except StopIteration:
                break
        return results
    
    def search(self, query):
        query_embedding = self.vectorizer.generate_vector(query)
        results = self.database.search_document(query_embedding)

        results = self.iterate_over_top(results, 3)
        top_results = ''
        for i, result in enumerate(results, start=1):
            top_results += f'\nResult {i}: ' + result['text']
        message = f'''
        Given the following query, come up and the top results in a search based on the query, answer the question if its relevant or else say you dont know.

        Top results:
        {top_results}

        Answer to question:
        '''

        answer = self.client.chat(message)
        return answer.text