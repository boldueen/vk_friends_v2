import vk_api
from vk_api.exceptions import ApiError

from schemas import VkUser

from loguru import logger


class VkHTTPClient:
    _access_token: str
    _api_version: str = "5.81"

    def __init__(self, access_token: str) -> None:
        self.token = access_token
        self.session = vk_api.VkApi(token=self.token)
        self.api = self.session.get_api()

    def get_user_info(self, user_id: str) -> VkUser:
        try:
            response = self.api.users.get(
                user_ids=[user_id],
            )
        except ApiError as e:
            logger.info(f"Невозможно спарсить пользователя {user_id}: {e}")
            return
        user = response[0]

        return VkUser(
            id=str(user["id"]),
            name=user["first_name"] + " " + user["last_name"],
            friend_ids=[],
            parent_friend_id=None,
        )

    def get_friends(self, user_id: str) -> list[VkUser]:
        try:
            response = self.api.friends.get(
                user_id=user_id,
                fields=["nickname"],
                limit=100,
            )
        except ApiError as e:
            logger.info(f"Невозможно спарсить друзей для {user_id}: {e}")
            return []

        friends_list = response.get("items", [])[:100]  # FIXME выставить лимит в 100

        return [
            VkUser(
                id=str(friend["id"]),
                name=friend["first_name"] + " " + friend["last_name"],
                friend_ids=[],
                parent_friend_id=user_id,
            )
            for friend in friends_list
        ]
