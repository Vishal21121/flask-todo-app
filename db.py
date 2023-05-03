import pymongo

def connect():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['flask_todo']
    return db