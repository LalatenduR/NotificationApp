from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from dotenv import load_dotenv
load_dotenv() 
import os

MONGODB_URL=os.getenv('MONGODB_URL')
client=AsyncIOMotorClient(MONGODB_URL)
db: Database=client.notifications_db
notifications_collection=db.get_collection(os.getenv('COLLECTION_NAME'))
