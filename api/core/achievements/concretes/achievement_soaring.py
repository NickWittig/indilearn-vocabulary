from datetime import datetime
from api.core.achievements.achievement import Achievement
from sqlalchemy.orm import Session
from api.core.db.models import User  # Assuming User model contains score attributes


class AchievementSoaring(Achievement):
    START_DATE = datetime(2024, 11, 9)  # Hardcoded start date for awarding the achievement
    top_number = 3

    def __init__(self, session: Session):
        """
        Initialize the Soaring achievement.

        :param session: The SQLAlchemy session to use for database queries.
        :param get_top_users: A function to retrieve the top users based on score.
        """
        super().__init__("Soaring", session)

    def unlock_condition(self, user_id: int) -> bool:
        """
        Check if the user is in the top 3 on the leaderboard and if the date is after the hardcoded
        start date for awarding this achievement.

        :param user_id: The ID of the user.
        :return: True if the condition is met, False otherwise.
        """
        # Check if today is on or after the specified start date
        if datetime.now() < self.START_DATE:
            return False

        # Get the top 3 (top_number) users on the leaderboard
        top_users = self.session.query(User).order_by(User.score.desc()).limit(self.top_number).all()
        top_3_user_ids = [user.id for user in top_users]

        # Check if the user is in the top 3
        return user_id in top_3_user_ids
