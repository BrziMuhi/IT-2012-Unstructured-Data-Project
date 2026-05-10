import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analytics.mongo_pipeline import get_mongo_collection, category_pipeline

collection = get_mongo_collection()

df = category_pipeline(collection)

print("MONGO CATEGORY AGGREGATION:")
print(df.head())