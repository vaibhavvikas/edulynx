import json
import os

from dotenv import load_dotenv
from pymongo import ASCENDING, DESCENDING, MongoClient

# Load .env file
load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
courses = os.getenv("COURSES_COLLECTION")

# Connect to the MongoDB instance
client = MongoClient(f"mongodb://{db_host}:{db_port}/")

# Select the database and collection you want to insert the data into
db = client[db_name]
courses_collection = db[courses]

# Open the JSON file and load its contents
with open("migration/courses.json") as f:
    courses = json.load(f)

# Insert the data into the collection
for course in courses:
    course["ratings"] = 0.0
    course["ratings_count"] = 0
    for index, chapter in enumerate(course["chapters"]):
        chapter["chapter_no"] = index + 1
        chapter["ratings_total"] = 0
        chapter["ratings_count"] = 0
    courses_collection.insert_one(course)

# Creating indices on name, date and average ratings
courses_collection.create_index([("name", ASCENDING)])
courses_collection.create_index([("date", ASCENDING)])
courses_collection.create_index([("ratings.average", DESCENDING)])

# Close the MongoDB connection
client.close()
