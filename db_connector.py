from pymongo import MongoClient
from pymongo.collection import Collection


class MongoCustomClient:
    def __init__(self):
        self.client: MongoClient = MongoClient("mongodb://localhost:27017")
        self.db = self.client["mydatabase"]
        self.collection: Collection = self.db["vk_users"]

    def insert_one(self, data: dict):
        self.collection.insert_one(data)

    def insert_many(self, data: list[dict]):
        self.collection.insert_many(data)

    def find_one(self, query: dict) -> dict | None:
        return self.collection.find_one(query)
