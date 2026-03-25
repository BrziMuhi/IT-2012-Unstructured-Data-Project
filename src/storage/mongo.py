from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["tourism_pipeline"]
collection = db["raw_places"]


def save_to_mongo(data, source):
    document = {
        "source": source,
        "timestamp": datetime.now(),
        "data": data
    }

    result = collection.insert_one(document)
    print(f"Saved document: {result.inserted_id}")