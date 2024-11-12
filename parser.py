from collections import deque
from db_connector import MongoCustomClient
from schemas import VkUser
from vk_client import VkHTTPClient

from loguru import logger


class VkParser:
    def __init__(self, vk_client: VkHTTPClient, mongo_client: MongoCustomClient):
        self.vk_client: VkHTTPClient = vk_client
        self.mongo_client: MongoCustomClient = mongo_client

    def parse_friends(self, user_id: str, parse_all: bool):
        friends = self.vk_client.get_friends(user_id, limit=100)
        return friends

    def get_user_info(self, user_id: str) -> VkUser | None:
        return self.vk_client.get_user_info(user_id)

    def _save_user(self, user: VkUser, depth: int | None = None):
        self.mongo_client.upsert(
            query={k: v for k, v in user.model_dump().items() if v},
            data={"depth": depth, **user.model_dump()},
        )

    def parse_friends_in_depth(self, user: VkUser, depth: int | None = 3):
        users_to_parse_q = deque([user])
        for i in range(depth):
            tmp_users_storage = []
            while len(users_to_parse_q) > 0:
                user = users_to_parse_q.popleft()

                friends = self.parse_friends(user.id, parse_all=i == 2)

                if len(friends) == 0:
                    logger.error(f"no friends for {user.id}")
                    continue

                user.friend_ids = [friend.id for friend in friends]
                self._save_user(user, depth=i)

                tmp_users_storage.extend(self._exclude_parent_friend(user.id, friends))

                logger.success(f"got {len(friends)} friends for {user.id}")

            users_to_parse_q += tmp_users_storage

    def parse_leaf_friends(self):
        leaf_friends_ids = self.mongo_client.get_leaf_friends()

        for _id in leaf_friends_ids:
            logger.info(f"parsing {_id=}")
            user = VkUser(id=_id)
            friends = self.parse_friends(user.id)
            if len(friends) == 0:
                logger.error(f"no friends for {user.id}")
                continue
            user.friend_ids = [friend.id for friend in friends]
            self._save_user(user, depth=3)

    def _exclude_parent_friend(
        self, parent_friend_id: str, friends: list[VkUser]
    ) -> list[VkUser]:
        return [friend for friend in friends if friend.id != parent_friend_id]
