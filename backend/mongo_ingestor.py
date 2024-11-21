import pandas as pd
from core.rag.mongo_client import MongoClient

class MongoIngestor:
    def __init__(self, mongo_uri: str, db_name: str, db_collection: str):
        self.db_name = db_name
        self.db_collection = db_collection
        self.mongo_client = MongoClient().get_mongo_client(mongo_uri)

    def ingest_to_mongodb(self, df: pd.DataFrame):
        """Inserts the processed DataFrame into MongoDB."""
        db = self.mongo_client[self.db_name]
        collection = db[self.db_collection]

        # Clear the collection before inserting new data
        collection.delete_many({})

        # Convert DataFrame to dictionary and insert into MongoDB
        documents = df.to_dict("records")
        collection.insert_many(documents)
        print("Data ingestion into MongoDB completed")
