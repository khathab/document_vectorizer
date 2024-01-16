import pymongo
import os
from typing import List, Union
from ..types import Document, Chunk, Image
from dotenv import load_dotenv
import requests
class Database:
    def __init__(self, database_name='app') -> None:
        self.database_name = database_name
        try:
            load_dotenv()
            MONGODB_URI = os.environ.get('MONGODB_URI')
            # self.project_id = os.environ.get('PROJECT_ID')
            # cluster_name_regex = re.compile(r'mongodb\+srv://[a-zA-Z0-9]+:[^@]+@([a-zA-Z0-9]+)\.')
            # match = cluster_name_regex.search(cluster_name_regex)
            # self.cluster_name = match.group(1)
            print(f'Mongodb uri: {MONGODB_URI}')
            self.client = pymongo.MongoClient(MONGODB_URI)
            self.client.admin.command('ping')
            self.documents = self.client[database_name].documents
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def setup_atlas_vector_search(self):
        url = f'https://cloud.mongodb.com/api/atlas/v2/groups/{self.project_id}/clusters/{self.cluster_name}/fts/indexes'

        index_config = {
        "collectionName": 'documents',
        "database": self.database_name,
        "name": "documentSearch",
        "type": "vectorSearch",
        "fields": [
            {
            "numDimensions": 1536,
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
        requests.post(url=url, data=index_config)

    def add_documents(self, documents: List[Union[Chunk, Document, Image]]):
        self.documents.insert_many(documents=[doc.model_dump() for doc in documents])

    def search_document(self, vector):
        pipeline = self.generate_pipeline(vector)
        results = self.documents.aggregate(pipeline)
        return results
    
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