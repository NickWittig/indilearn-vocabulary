from api.core.achievements.achievement import Achievement
from api.core.db.models import Item, UserItem
from sqlalchemy.orm import Session


class AchievementBeyondTheHorizon(Achievement):
    def __init__(self, session: Session):
        """
        Initialize the BeyondTheHorizon achievement.

        :param session: The SQLAlchemy session to use for database queries.
        """
        super().__init__("BeyondTheHorizon", session)

    def unlock_condition(self, user_id: int) -> bool:
        """
        Check if the user has correctly answered at least 100 items of grade 6.

        :param user_id: The ID of the user.
        :return: True if the condition is met, False otherwise.
        """
        grade_to_check = 6
        required_correct_items = 100

        # Query to count the number of correctly answered items of the specified grade
        correct_items_count = (
            self.session.query(UserItem)
            .join(Item, UserItem.item_id == Item.id)
            .filter(UserItem.user_id == user_id, UserItem.correctness == True, Item.grade == grade_to_check)
            .count()
        )

        return correct_items_count >= required_correct_items
