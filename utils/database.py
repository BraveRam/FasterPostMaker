from pymongo import MongoClient
from utils.config import MONGODB_URI, DB_NAME, COLLECTION_NAME


class Database:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]
    
    def get_user(self, user_id):
        return self.collection.find_one({"user_id": user_id})
    
    def create_user(self, user_id):
        return self.collection.insert_one({
            "user_id": user_id,
            "is_admin": False,
            "is_banned": False,
            "is_premium": False
        })
    
    def update_user(self, user_id, updates):
        return self.collection.update_one(
            {"user_id": user_id},
            {"$set": updates}
        )
    
    def get_all_users(self):
        return list(self.collection.find({}))
    
    def user_exists(self, user_id):
        return self.get_user(user_id) is not None


# Create global database instance
db = Database()
