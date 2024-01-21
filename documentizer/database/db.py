import os
import re
import pymongo
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

    def setup_atlas_vector_search(self):
        url = f'https://cloud.mongodb.com/api/atlas/v2/groups/{self.project_id}/clusters/{self.cluster_name}/fts/indexes'
        index_config = {
            "collectionName": 'documents',
            "database": self.database_name,
            "name": "documentSearch",
            "type": "vectorSearch",
            "fields": [
                {
                    "numDimensions": 1024,
                    "path": "embedding",
                    "similarity": "cosine",
                    "type": "vector"
                },
                {
                    "path": "type",
                    "type": "filter"
                },
            ]
        }
        headers = {'Content-Type': 'application/json'}
        # Add authentication if required
        response = requests.post(url=url, json=index_config, headers=headers)
        if response.status_code == 200:
            print("Vector search index created successfully.")
        else:
            print(f"Error creating index: {response.json()}")

    def add_documents(self, documents: List[Union[Chunk, Document, Image]]):
        # Ensure that documents have a method named 'model_dump'
        self.documents.insert_many(documents=[doc.model_dump() for doc in documents])

    def search_document(self, vector, type):
        try:
            pipeline = self.generate_pipeline(vector, type)
            results = self.documents.aggregate(pipeline)
            return next(results, None)
        except Exception as e:
            print(f"Error in search: {e}")
            return None
    
    def generate_pipeline(self,vector, type):
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