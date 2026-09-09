from typing import List, Tuple

from api.core.db.models import User
from api.core.db.repository.user_repository import UserRepository
from api.core.db.services.achievement_service import AchievementService
from api.core.db.services.rank_service import RankService
from sqlalchemy import Column
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = UserRepository(session)
        self.achievement_service = AchievementService(session)
        self.rank_service = RankService(session)

    def get_user(self, user_id):
        user = self.repository.get_by_id(user_id)
        if not user:
            return None, "User not found"
        return user, None

    def create_user(self, user_id: int, user_name: str, in_control_group: bool):
        existing_user = self.repository.get_by_id(user_id)
        if existing_user:
            return None, "User already exists"

        user = User(id=user_id, username=user_name, ability=0.0, score=0, rank_id=0, in_control_group=in_control_group)
        self.repository.add(user)
        return user, None

    def check_achievements(self, user_id):
        user = self.repository.get_by_id(user_id)
        if not user:
            return None, "User not found"

        unlocked_achievements = self.achievement_service.check_user_achievements(user_id)
        self.award_achievements(user_id)
        return [achievement.achievement_id for achievement in unlocked_achievements], None

    def check_new_user_achievements_by_user_name(self, user_name):
        user = self.repository.get_user_by_username(user_name)
        if not user:
            return None, "User not found"
        return self.check_achievements(user.id)

    def award_achievements(self, user_id) -> Tuple[List[Column[int]] | None, str | None]:
        user: User | None = self.repository.get_by_id(user_id)
        if not user:
            return None, "User not found"

        unlocked_achievements = self.achievement_service.check_user_achievements(user_id)
        self.achievement_service.award_user_achievements(unlocked_achievements)

        return [achievement.achievement_id for achievement in unlocked_achievements], None

    def get_top_users(self, limit=10):
        return self.repository.get_top_users(limit)

    def get_user_by_username(self, username: str):
        """
        Retrieve a user by their username.

        :param username: The username of the user to retrieve.
        :return: (User | None, str | None) Tuple containing the user object if found, otherwise None,
        and an error message if applicable.
        """
        user = self.repository.get_user_by_username(username)
        if not user:
            return None, "User not found"
        return user, None

    def get_user_achievements_ids(self, user_name):
        user, error = self.get_user_by_username(user_name)
        if not user:
            return None, "User not found"

        user_achievements = self.achievement_service.get_user_achievements(user)
        return [user_achievement.achievement_id for user_achievement in user_achievements], None

    def add_user_score(self, user: User, value):
        if not user:
            return None, "User not found"

        user.score += value
        self.repository.update(user)

    def update_rank(self, user):
        if not user:
            return "User not found"
        ranks = self.rank_service.get_all_ranks()
        for rank in ranks:
            if user.score > rank.min_score and user.score < rank.max_score:
                if rank.id != user.rank_id:
                    user.rank_id = rank.id
                    self.repository.update(user)
                    return
