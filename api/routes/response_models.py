from typing import Annotated

from pydantic import BaseModel, StringConstraints


class AchievementResponseModel(BaseModel):
    id: int
    name_de: str
    name_en: str
    description_de: str
    description_en: str
    color: str
    icon_url: str

    class Config:
        from_attributes = True


class ItemCheckModel(BaseModel):
    item_id: int
    user_solution: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, min_length=1, max_length=200, pattern=r"^[a-zA-Z0-9äöüßÄÖÜ.\'()\/?!\-\s]+$"
        ),
    ]


class ItemResponseModel(BaseModel):
    id: int
    question: str

    class Config:
        from_attributes = True


class UserResponseModel(BaseModel):
    id: int
    user_name: str
    score: int
    rank_id: int

    class Config:
        from_attributes = True
