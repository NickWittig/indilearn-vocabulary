from typing import List

from api.core.achievements.achievement_registry import AchievementRegistry
from api.core.db.models import Achievement, User, UserAchievement
from api.core.db.repository.achievement_repository import AchievementRepository
from api.core.db.repository.user_achievement_repository import UserAchievementRepository


class AchievementService:
    def __init__(self, session):
        self.session = session
        self.achievement_repository = AchievementRepository(session)
        self.user_achievement_repository = UserAchievementRepository(session)

    def check_user_achievements(self, user_id) -> List[UserAchievement]:
        unlocked_achievements = []
        all_achievements = self.achievement_repository.get_all()

        for achievement in all_achievements:
            if not self.user_achievement_repository.exists(user_id, achievement.id):
                achievement_class = AchievementRegistry.get_achievement(achievement.class_name, self.session)
                if achievement_class.unlock_condition(user_id):
                    user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement.id)
                    unlocked_achievements.append(user_achievement)

        return unlocked_achievements

    def award_user_achievements(self, user_achievements: List[UserAchievement]):
        for user_achievement in user_achievements:
            if not self.user_achievement_repository.exists(user_achievement.user_id, user_achievement.achievement_id):
                self.user_achievement_repository.add(user_achievement)

    def get_achievement(self, achievement_id: int) -> Achievement:
        return self.achievement_repository.get_by_id(achievement_id)

    def get_all_achievements(self) -> List[Achievement]:
        return self.achievement_repository.get_all()

    def get_user_achievements(self, user: User):
        return self.achievement_repository.get_user_achievements(user.id)
