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
        
    def read_demo_data(self):
        self.collection = self.db['demo_collection']
        
        try:
            data = list(self.collection.find({}, {'_id': 0}))
            return data
        except Exception as e:
            print(f"An error occurred while reading data: {e}")
            return None
        
    def load_demo_data(self, demo_data):
        if demo_data is None:
            raise ValueError("demo_data must be provided")
        
        self.collection = self.db['demo_collection']
        # Drop existing collection before inserting new data
        self.collection.drop()
        # Insert new data
        self.collection.insert_many(demo_data)
    
    def load_data(self, transformed_data):
        if transformed_data is None:
            raise ValueError("transformed_data must be provided")
        
        self.collection = self.db['oil_mill_collection']
        # Drop existing collection before inserting new data
        self.collection.drop()
        # Insert new data
        self.collection.insert_many(transformed_data)

if __name__ == "__main__":
    datawarehouse_handler = DataWarehouseHadler()
    datawarehouse_handler.read_data()