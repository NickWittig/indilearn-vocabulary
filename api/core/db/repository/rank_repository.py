from api.core.db.models import Rank
from api.core.db.repository.abstract_repository import AbstractRepository
from sqlalchemy.orm import Session


class RankRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, rank_id: int) -> Rank:
        return self.session.get(Rank, rank_id)

    def get_all(self):
        return self.session.query(Rank).all()

    def add(self, rank: Rank):
        self.session.add(rank)
        self.session.commit()

    def update(self, rank: Rank):
        self.session.commit()

    def delete(self, rank_id: int):
        rank = self.get_by_id(rank_id)
        if rank:
            self.session.delete(rank)
            self.session.commit()
