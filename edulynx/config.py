import os

from dotenv import load_dotenv

load_dotenv()


class MongoDBEnv:
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
