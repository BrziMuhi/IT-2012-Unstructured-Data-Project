from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")

# Tourism DB
tourism_db = client["tourism_pipeline"]
places_collection = tourism_db["raw_places"]

# Image DB
image_db = client["image_pipeline"]
images_collection = image_db["images"]


def save_to_mongo(data, source):
    document = {
        "source": source,
        "timestamp": datetime.now(),
        "data": data
    }

    result = places_collection.insert_one(document)
    print(f"Saved document: {result.inserted_id}")


def save_image_metadata(metadata):
    metadata["processed_at"] = datetime.utcnow()
    result = images_collection.insert_one(metadata)
    print(f"Saved metadata: {result.inserted_id}")