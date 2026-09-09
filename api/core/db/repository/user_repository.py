from api.core.db.models import User
from api.core.db.repository.abstract_repository import AbstractRepository
from api.core.db.schemas import UserSchema
from sqlalchemy.orm import Session


class UserRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id):
        return self.session.get(User, user_id)

    def get_all(self):
        return self.session.query(User).all()

    def add(self, user):
        self.session.add(user)
        self.session.commit()

    def update(self, user):
        self.session.merge(user)
        self.session.commit()

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()

    def get_top_users(self, limit=10):
        users = self.session.query(User).order_by(User.score.desc()).limit(10).all()
        return [UserSchema.model_validate(user).model_dump() for user in users]

    def get_user_by_username(self, username: str):
        return self.session.query(User).filter(User.user_name == username).first()
