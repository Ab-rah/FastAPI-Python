from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

# MongoDB client instance
client = AsyncIOMotorClient(MONGO_URI)
database = client["test"]

def get_database():
    return database
