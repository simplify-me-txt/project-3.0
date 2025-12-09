from pymongo import MongoClient
import os

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ecommerce_db"

class Database:
    client: MongoClient = None
    db = None

db = Database()

def get_database():
    return db.db

def connect_to_mongo():
    db.client = MongoClient(MONGO_URI)
    db.db = db.client[DB_NAME]
    print("Connected to MongoDB")

def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection")
