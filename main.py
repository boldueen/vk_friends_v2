from loguru import logger
from config import Config
from db_connector import MongoCustomClient
from vk_client import VkHTTPClient
from parser import VkParser
from graph import build_graph

first_level_user_ids = [
    "164679738",
    "419376445",
    "472133870",
    "386272361",
    "172350665",
    "229180632",
    "145195585",
    "193887357",
    "386272361",
    "204720239",
    "162225997",
    "860446539",
    "472133870",
    "195614586",
    "825545292",
    "750743366",
    "637593527",
    "299106540",
    "164679738",
    "101098087",
    "239666833",
    "342040017",
    "205762499",
    "165171730",
    "270780454",
    "155290829",
    "151413977",
    "62269831",
    "253407490",
    "192574298",
    "144399122",
    "419376445",
    "508644412",
    "396854328",
]


def main():
    config = Config()
    mongo_client = MongoCustomClient(
        mongo_url=config.mongo_url,
        database_name=config.mongo_db_name,
        collection_name=config.mongo_collection_name,
    )
    vk_client = VkHTTPClient(config.access_token)
    vk_parser = VkParser(vk_client, mongo_client)

    for user_id in first_level_user_ids:
        user = vk_parser.get_user_info(user_id)
        if user is None:
            continue
        vk_parser.parse_friends_in_depth(user, depth=4)

    data = mongo_client.select_all()
    logger.info(f"got {len(data)} users")
    build_graph(data)


if __name__ == "__main__":
    main()
