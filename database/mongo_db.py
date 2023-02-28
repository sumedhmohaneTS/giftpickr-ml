from pymongo import MongoClient

def get_mongo_client(uri: str='mongodb+srv://giftpickr-user:olGrScebMhNj6gnQ@giftpickr-cluster.nisokxj.mongodb.net/test'):
    return MongoClient(uri)

class MongoDB:
    def __init__(self, uri: str, database: str):
        self.client = get_mongo_client(uri)
        self.db = self.client[database]

    def get_collection(self, collection: str):
        return self.db[collection]
