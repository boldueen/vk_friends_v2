from config import Config
from db_connector import MongoCustomClient
from schemas import VkUser
from vk_client import VkHTTPClient
from parser import VkParser


first_level_user_ids = [
    "396854328",
    "151413977",
    "144399122",
    "270780454",
]

first_level_user_ids_tmp = [
    "396854328",
]


def main():
    config = Config()
    mongo_client = MongoCustomClient(config.mongo_url)
    vk_client = VkHTTPClient(config.access_token)
    vk_parser = VkParser(vk_client, mongo_client)

    for user_id in first_level_user_ids_tmp:
        user = vk_parser.get_user_info(user_id)
        if user is None:
            continue
        vk_parser.parse_friends_in_depth(user, depth=3)


if __name__ == "__main__":
    main()
