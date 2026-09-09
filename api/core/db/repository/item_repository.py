from api.core.db.models import Item, User, UserItem
from api.core.db.repository.abstract_repository import AbstractRepository
from sqlalchemy import desc, func
from sqlalchemy.orm import Session


class ItemRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, item_id):
        return self.session.get(Item, item_id)

    def get_all(self):
        return self.session.query(Item).all()

    def get_all_ui(self):
        return self.session.query(UserItem).all()

    def get_n_ui_for(self, n, user_id):
        return (
            self.session.query(UserItem)
            .filter(UserItem.user_id == user_id)
            .order_by(desc(UserItem.timestamp))
            .limit(n)
            .all()
        )

    def add(self, item):
        self.session.add(item)
        self.session.commit()

    def update(self, item):
        self.session.merge(item)
        self.session.commit()

    def delete(self, item_id):
        item = self.get_by_id(item_id)
        if item:
            self.session.delete(item)
            self.session.commit()

    def get_first_item(self):
        return self.session.query(Item).first()

    def get_user_by_id(self, user_id):
        return self.session.get(User, user_id)

    def add_user_item(self, user_item):
        self.session.add(user_item)
        self.session.commit()

    def get_random_item(self):
        return self.session.query(Item).order_by(func.random()).first()
