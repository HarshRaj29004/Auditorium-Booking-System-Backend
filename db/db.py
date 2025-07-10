from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.utils import MONGO_URL, DB

client = MongoClient(MONGO_URL, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    db = client[DB]
    print("You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    db = None
    
