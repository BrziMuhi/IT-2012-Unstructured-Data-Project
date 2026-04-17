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

def save_transcript_to_mongo(transcript, source_path, model_name="base"):
    transcripts_collection = tourism_db["transcripts"]   

    document = {
        "source_path": source_path,
        "language": transcript.get("language"),
        "duration": transcript.get("duration"),
        "model_name": model_name,
        "full_text": transcript.get("full_text"),
        "segments": transcript.get("segments", []),
        "created_at": datetime.utcnow()
    }

    result = transcripts_collection.insert_one(document)
    print(f"Saved transcript: {result.inserted_id}")    