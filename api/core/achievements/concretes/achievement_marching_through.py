from datetime import datetime

from api.core.achievements.achievement import Achievement
from api.core.db.models import UserItem
from sqlalchemy import func
from sqlalchemy.orm import Session


class AchievementMarchingThrough(Achievement):
    def __init__(self, session: Session):
        """
        Initialize the MarchingThrough achievement.

        :param session: The SQLAlchemy session to use for database queries.
        """
        super().__init__("MarchingThrough", session)

    def unlock_condition(self, user_id: int) -> bool:
        """
        Check if the user has correctly answered at least 100 items in one day.

        :param user_id: The ID of the user.
        :return: True if the condition is met, False otherwise.
        """
        required_correct_items = 100
        today = datetime.now().date()

        # Query to count the number of correctly answered items by the user for today
        correct_items_count = (
            self.session.query(UserItem)
            .filter(UserItem.user_id == user_id, UserItem.correctness == True, func.date(UserItem.timestamp) == today)
            .count()
        )

        return correct_items_count >= required_correct_items
