from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class Achievement(ABC):
    def __init__(self, name: str, session: Session):
        """
        Initialize the achievement with a name.

        :param name: The name of the achievement.
        """
        self.name = name
        self.session: Session = session

    @abstractmethod
    def unlock_condition(self, user_id: int) -> bool:
        """
        Check if the achievement unlock condition is met.

        :param user_id: The ID of the user.
        :return: True if the condition is met, False otherwise.
        """
