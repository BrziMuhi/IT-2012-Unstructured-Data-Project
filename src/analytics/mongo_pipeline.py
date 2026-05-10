import pandas as pd
from pymongo import MongoClient


def get_mongo_collection(
    uri="mongodb://localhost:27017",
    db_name="tourism_pipeline",
    collection_name="raw_places"
):
    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]


def category_pipeline(collection):
    pipeline = [
        {
            "$match": {
                "data.properties.categories": {"$exists": True}
            }
        },
        {
            "$addFields": {
                "primary_category": {
                    "$arrayElemAt": ["$data.properties.categories", 0]
                }
            }
        },
        {
            "$group": {
                "_id": "$primary_category",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$project": {
                "_id": 0,
                "category": "$_id",
                "count": 1
            }
        }
    ]

    result = list(collection.aggregate(pipeline))
    return pd.DataFrame(result)