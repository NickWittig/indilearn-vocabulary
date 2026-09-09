from datetime import datetime, timedelta

from api.core.achievements.achievement import Achievement
from api.core.db.models import UserItem
from sqlalchemy import func


class AchievementUnshakable(Achievement):
    correctly_answered = 15
    days = 14

    def __init__(self, session):
        """
        Initialize the Unshakable achievement.
        """
        super().__init__("Unshakable", session)

    def unlock_condition(self, user_id: int) -> bool:
        """
        Check if the user has correctly answered at least correctly_answered items every day for t days consecutive days.

        :param user_id: The ID of the user.
        :param db: The database session.
        :return: True if the condition is met, False otherwise.
        """
        now = datetime.now()
        daily_counts = (
            self.session.query(func.date(UserItem.timestamp).label("date"), func.count(UserItem.id).label("count"))
            .filter(
                UserItem.user_id == user_id,
                UserItem.correctness == True,
                UserItem.timestamp >= now - timedelta(days=self.days),
            )
            .group_by(func.date(UserItem.timestamp))
            .all()
        )

        consecutive_days = 0
        for day in daily_counts:
            if day.count >= self.correctly_answered:
                consecutive_days += 1
                if consecutive_days >= self.days:
                    return True
            else:
                consecutive_days = 0

        return False
