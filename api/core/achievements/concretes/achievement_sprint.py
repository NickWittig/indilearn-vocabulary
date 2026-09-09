from datetime import datetime, timedelta

from api.core.achievements.achievement import Achievement
from api.core.db.models import UserItem
from sqlalchemy.orm import Session


class AchievementSprint(Achievement):
    def __init__(self, session: Session):
        """
        Initialize the Sprint achievement.

        :param session: The SQLAlchemy session to use for database queries.
        """
        super().__init__("Sprint", session)

    def unlock_condition(self, user_id: int) -> bool:
        """
        Check if the user has correctly answered at least n items within t minutes.

        :param user_id: The ID of the user.
        :return: True if the condition is met, False otherwise.
        """
        now = datetime.now()
        forty_five_minutes_ago = now - timedelta(minutes=10)
        items_to_solve = 25

        correct_items_count = (
            self.session.query(UserItem)
            .filter(
                UserItem.user_id == user_id, UserItem.correctness == True, UserItem.timestamp >= forty_five_minutes_ago
            )
            .count()
        )

        return correct_items_count >= items_to_solve
