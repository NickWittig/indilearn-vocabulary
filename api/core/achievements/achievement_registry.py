from api.core.achievements.concretes.achievement_beyond_the_horizon import AchievementBeyondTheHorizon
from api.core.achievements.concretes.achievement_marching_through import AchievementMarchingThrough
from api.core.achievements.concretes.achievement_night_owl import AchievementNightOwl
from api.core.achievements.concretes.achievement_omniscient import AchievementOmniscient
from api.core.achievements.concretes.achievement_soaring import AchievementSoaring
from api.core.achievements.concretes.achievement_sprint import AchievementSprint
from api.core.achievements.concretes.achievement_unshakable import AchievementUnshakable
from sqlalchemy.orm import Session


class AchievementRegistry:
    _registry = {
        "AchievementOmniscient": AchievementOmniscient,
        "AchievementUnshakable": AchievementUnshakable,
        "AchievementBeyondTheHorizon": AchievementBeyondTheHorizon,
        "AchievementSoaring": AchievementSoaring,
        "AchievementSprint": AchievementSprint,
        "AchievementMarchingThrough": AchievementMarchingThrough,
        "AchievementNightOwl": AchievementNightOwl,
    }

    @classmethod
    def get_achievement(cls, class_name, session: Session):
        achievement_class = cls._registry.get(class_name)
        if achievement_class is None:
            raise ValueError(f"Achievement class '{class_name}' not found in registry.")
        return achievement_class(session)
