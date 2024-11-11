from pydantic import BaseModel


class VkUser(BaseModel):
    id: str
    name: str
    parent_friend_id: int | None
    friend_ids: list[int] | None = None
