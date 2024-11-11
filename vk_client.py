import vk_api
from vk_api.exceptions import ApiError

from schemas import VkUser


class VkHTTPClient:
    _access_token: str
    _api_version: str = "5.81"

    def __init__(self, access_token: str) -> None:
        self.token = access_token
        self.session = vk_api.VkApi(token=self.token)
        self.api = self.session.get_api()

    def get_friends(self, user_id: str) -> list[VkUser]:
        try:
            response = self.api.friends.get(
                user_id=user_id,
                fields=["nickname"],
                limit=5,
            )
        except ApiError as e:
            return []

        friends_list = response.get("items", [])[:100]

        return [
            VkUser(
                id=str(friend["id"]),
                name=friend["first_name"] + " " + friend["last_name"],
                friend_ids=[],
                parent_friend_id=user_id,
            )
            for friend in friends_list
        ]
