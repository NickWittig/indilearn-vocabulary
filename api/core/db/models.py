from datetime import datetime

from api.core.db.session import Base
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Rank(Base):
    __tablename__ = "ranks"

    id = Column(Integer, primary_key=True)
    name_de = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    min_score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)

    users = relationship("User", back_populates="rank")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True)
    name_de = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    description_de = Column(String)
    description_en = Column(String)
    color = Column(String)
    icon_url = Column(String)
    class_name = Column(String, nullable=False)

    user_achievements = relationship("UserAchievement", back_populates="achievement")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)
    score = Column(Integer, nullable=False)
    rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=False)
    ability = Column(Float, nullable=False)
    in_control_group = Column(Boolean, nullable=False)

    rank = relationship("Rank", back_populates="users")
    user_items = relationship("UserItem", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    solutions = Column(String, nullable=False)
    difficulty = Column(Float, nullable=False)
    discrimination = Column(Float, nullable=False)
    grade = Column(Integer, nullable=False)

    user_items = relationship("UserItem", back_populates="item")


class UserItem(Base):
    __tablename__ = "user_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    correctness = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="user_items")
    item = relationship("Item", back_populates="user_items")


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
