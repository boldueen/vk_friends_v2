from config import Config
from db_connector import MongoCustomClient
from schemas import VkUser
from vk_client import VkHTTPClient
from parser import VkParser


first_level_users = [
    VkUser(
        id="396854328",
        name="Денис Яценко",
        parent_friend_id=None,
    ),
    VkUser(
        id="151413977",
        name="Владислав Утц",
        parent_friend_id=None,
    ),
    VkUser(
        id="144399122",
        name="Александр Чекунков",
        parent_friend_id=None,
    ),
    VkUser(
        id="270780454",
        name="Иван Никонов",
        parent_friend_id=None,
    ),
]


def main():
    config = Config()
    mongo_client = MongoCustomClient(config.MONGO_URL)
    vk_client = VkHTTPClient(config.VK_ACCESS_TOKEN)
    vk_parser = VkParser(vk_client, mongo_client)

    for user in first_level_users:
        vk_parser.parse_friends_in_depth(user)


if __name__ == "__main__":
    main()
