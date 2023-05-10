from pymongo import MongoClient

from edulynx.config import MongoDBEnv

mongo_env = MongoDBEnv()

# Connect to the MongoDB instance
client = MongoClient(f"mongodb://{mongo_env.db_host}:{mongo_env.db_port}/")

# Select the database and collection you want to insert the data into
db = client[mongo_env.db_name]


def get_collection(collection_name: str):
    return db[collection_name]
