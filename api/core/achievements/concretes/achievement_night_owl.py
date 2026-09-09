from datetime import time

from api.core.achievements.achievement import Achievement
from api.core.db.models import UserItem
from sqlalchemy import func, or_
from sqlalchemy.orm import Session


class AchievementNightOwl(Achievement):
    def __init__(self, session: Session):
        """
        Initialize the NightOwl achievement.

        :param session: The SQLAlchemy session to use for database queries.
        """
        super().__init__("NightOwl", session)

    def unlock_condition(self, user_id: int) -> bool:
        """
        Check if the user has correctly answered at least 500 items between 7:30 PM and 6:00 AM.

        :param user_id: The ID of the user.
        :return: True if the condition is met, False otherwise.
        """
        start_time = time(19, 30)  # 7:30 PM
        end_time = time(6, 0)  # 6:00 AM
        items_to_solve = 300

        # Define the time ranges
        evening_time_range = func.extract("hour", UserItem.timestamp) >= start_time.hour
        night_time_range = func.extract("hour", UserItem.timestamp) < end_time.hour

        # Query to count the number of correctly answered items by the user during the specified time range
        correct_items_count = (
            self.session.query(UserItem)
            .filter(
                UserItem.user_id == user_id, UserItem.correctness == True, or_(evening_time_range, night_time_range)
            )
            .count()
        )

        return correct_items_count >= items_to_solve
