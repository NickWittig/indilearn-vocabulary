from api.core.db.models import UserAchievement
from api.core.db.repository.abstract_repository import AbstractRepository
from sqlalchemy.orm import Session


class UserAchievementRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, entity_id):
        return self.session.get(UserAchievement, entity_id)

    def get_all(self):
        return self.session.query(UserAchievement).all()

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def update(self, entity):
        self.session.commit()

    def delete(self, entity_id):
        entity = self.get_by_id(entity_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()

    def get_user_achievements(self, user_id):
        return self.session.query(UserAchievement).filter_by(user_id=user_id).all()

    def exists(self, user_id: int, achievement_id: int) -> bool:
        return (
            self.session.query(UserAchievement).filter_by(user_id=user_id, achievement_id=achievement_id).first()
            is not None
        )
