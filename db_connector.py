from loguru import logger
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoCustomClient:
    def __init__(
        self,
        mongo_url: str,
        database_name: str | None = "mydatabase",
        collection_name: str | None = "vk_users",
    ):
        self.client: MongoClient = MongoClient(mongo_url)
        self.db = self.client[database_name]
        self.collection: Collection = self.db[collection_name]

    def insert_one(self, data: dict):
        self.collection.insert_one(data)

    def insert_many(self, data: list[dict]):
        self.collection.insert_many(data)

    def find_one(self, query: dict) -> dict | None:
        return self.collection.find_one(query)

    def upsert(self, query: dict, data: dict):
        self.collection.update_one(query, {"$set": data}, upsert=True)

    def select_all(self) -> list[dict]:
        return list(self.collection.find())

    def get_leaf_friends(self) -> list[int]:
        leaf_friends = list(self.collection.find({"depth": 2}))
        res: list = []
        for friend in leaf_friends:
            logger.info(f"{friend=}")
            res.extend(friend["friend_ids"])
        logger.info(f"{res[:2]=} ")
        return res
