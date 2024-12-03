import os
from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, collection_name="Unsorted"):
        uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(uri)
        self.db = self.client['palmoildatabase']

        if collection_name is None:
            raise ValueError("collection_name must be provided when initializing MongoDBHandler")

        self.collection_name = collection_name
        self.collection = self.db[self.collection_name]

    def read_data(self):
        try:
            data = list(self.collection.find())
            return data
        except Exception as e:
            print(f"An error occurred while reading data: {e}")
            return None

    def set_collection(self, collection_name):
        self.collection_name = collection_name
        self.collection = self.db[self.collection_name]

