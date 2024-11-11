from db_connector import MongoCustomClient
from schemas import VkUser
from vk_client import VkHTTPClient


class VkParser:
    def __init__(self, vk_client: VkHTTPClient, mongo_client: MongoCustomClient):
        self.vk_client = vk_client
        self.mongo_client = mongo_client

    def parse(self, user_id: str):
        friends = self.vk_client.get_friends(user_id)
        self.mongo_client.insert_many([f.model_dump() for f in friends])
        return friends

    def parse_friends_in_depth(self, user: VkUser, depth: int | None = 3):
        # TODO
        pass
