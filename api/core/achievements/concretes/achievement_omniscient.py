from api.core.achievements.achievement import Achievement
from api.core.db.models import Item, UserItem


class AchievementOmniscient(Achievement):
    def __init__(self, session):
        """
        Initialize the Omniscient achievement.
        """
        super().__init__("Omniscient", session)

    def unlock_condition(self, user_id: int) -> bool:
        """
        Check if the user has correctly answered all items in the database.

        :param user_id: The ID of the user.
        :param db: The database session.
        :return: True if the user has correctly answered all items, False otherwise.
        """
        user_items = self.session.query(UserItem).filter_by(user_id=user_id, correctness=True).all()
        all_items = self.session.query(Item).all()
        return len(user_items) == len(all_items)
