from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RankSchema(BaseModel):
    id: int
    name_de: str
    name_en: str
    min_score: int
    max_score: int

    class Config:
        from_attributes = True


class AchievementSchema(BaseModel):
    id: int
    name_de: str
    name_en: str
    description_de: Optional[str] = None
    description_en: Optional[str] = None
    color: Optional[str] = None
    icon_url: Optional[str] = None
    class_name: str

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: int
    user_name: str
    score: int
    ability: float
    rank_id: int
    in_control_group: bool

    class Config:
        from_attributes = True


class ItemSchema(BaseModel):
    id: int
    question: str
    solutions: str
    difficulty: float
    discrimination: float
    grade: int

    class Config:
        from_attributes = True


class UserItemSchema(BaseModel):
    id: Optional[int] = None
    timestamp: Optional[datetime] = None
    user_id: int
    item_id: int
    correctness: bool
    user: Optional[UserSchema] = None
    item: Optional[ItemSchema] = None

    class Config:
        from_attributes = True


class UserAchievementSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    achievement_id: int
    timestamp: Optional[datetime] = None
    user: Optional[UserSchema] = None
    achievement: Optional[AchievementSchema] = None

    class Config:
        from_attributes = True
