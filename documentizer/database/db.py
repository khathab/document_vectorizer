import os
import re
import pymongo
import os
from typing import List, Union
from ..types import Document, Chunk, Image
from dotenv import load_dotenv
import requests
from dotenv import load_dotenv
from typing import List, Union
from ..types import Chunk, Document, Image
class Database:
    def __init__(self, database_name='app') -> None:
        self.database_name = database_name
        try:
            load_dotenv()
            MONGODB_URI = os.environ.get('MONGODB_URI')
            self.project_id = os.environ.get('PROJECT_ID')
            cluster_name_regex = re.compile(r'mongodb\+srv://[a-zA-Z0-9]+:[^@]+@([a-zA-Z0-9]+)\.')
            match = cluster_name_regex.search(MONGODB_URI)
            self.cluster_name = match.group(1) if match else 'Unknown'
            print(f'Cluster Name: {self.cluster_name}')
            print(f'Mongodb URI: {MONGODB_URI}')
            self.client = pymongo.MongoClient(MONGODB_URI)
            self.client.admin.command('ping')
            self.documents = self.client[database_name].documents
            print("Pinged your deployment. Successfully connected to MongoDB!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def add_documents(self, documents: List[Union[Chunk, Document, Image]]):
        self.documents.insert_many(documents=[doc.model_dump() for doc in documents])


    def search_document(self, vector):
        try:
            pipeline = self.generate_pipeline(vector)
            results = self.documents.aggregate(pipeline)
            return results
        except Exception as e:
            print(f"Error in search: {e}")
            return None
    
    def generate_pipeline(self,vector):
        # define pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": 'documentSearch',
                    "path": "embedding",
                    "queryVector": vector,
                    "numCandidates": 1000,
                    "limit": 40,
                }
            }, 
            {
                "$project": {
                    "embedding": 0 
                }
            }
        ]
        return pipeline