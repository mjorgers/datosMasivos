import os
from pymongo import MongoClient

class DataWarehouseHadler:
    def __init__(self):
        uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(uri)
        self.db = self.client['palmoildatabase']

    def read_data(self):
        
        self.collection = self.db['oil_mill_collection']
        
        try:
            data = list(self.collection.find({}, {'_id': 0}))
            return data
        except Exception as e:
            print(f"An error occurred while reading data: {e}")
            return None

    def load_data(self, transformed_data):

        if transformed_data is None:
            raise ValueError("transformed_data must be provided")
        
        # if not isinstance(transformed_data, str):
        #     raise TypeError("transformed_data must be an instance of str")

        self.collection = self.db['oil_mill_collection']
        self.collection.insert_many(transformed_data)


