from pydantic import BaseModel


class VkUser(BaseModel):
    id: str
    name: str | None = None
    parent_friend_id: str | None = None
    friend_ids: list[str] | None = None
