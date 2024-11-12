from pydantic import BaseModel


class VkUser(BaseModel):
    id: str
    name: str
    parent_friend_id: str | None
    friend_ids: list[str] | None = None
