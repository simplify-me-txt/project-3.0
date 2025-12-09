import json
import pymongo
import os
from tqdm import tqdm

DATA_FILE = "data/reviews_100k.json"
DB_NAME = "ecommerce_db"
COLLECTION_NAME = "reviews"
MONGO_URI = "mongodb://localhost:27017/"

def ingest_data():
    if not os.path.exists(DATA_FILE):
        print(f"Data file {DATA_FILE} not found!")
        return

    print("Connecting to MongoDB...")
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info() # Check connection
        
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Check if already populated
        # count = collection.count_documents({})
        # if count > 0:
        #     print(f"Collection already has {count} documents. Skipping ingestion to avoid duplicates.")
        #     return

        print("Loading JSON data...")
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
            
        print(f"Ingesting {len(reviews)} reviews into MongoDB...")
        
        # Insert in chunks to be safe
        chunk_size = 1000
        for i in tqdm(range(0, len(reviews), chunk_size)):
            chunk = reviews[i:i+chunk_size]
            collection.insert_many(chunk)
            
        print("Ingestion complete!")
        print(f"Total documents in {COLLECTION_NAME}: {collection.count_documents({})}")
        
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Could not connect to MongoDB. Is it running on localhost:27017?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ingest_data()
