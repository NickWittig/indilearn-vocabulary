from api.core.db.repository.rank_repository import RankRepository
from sqlalchemy.orm import Session


class RankService:
    def __init__(self, session: Session):
        self.repository = RankRepository(session)

    def get_rank_by_id(self, rank_id: int):
        rank = self.repository.get_by_id(rank_id)
        if not rank:
            return None, "Rank not found"
        return rank, None

    def get_all_ranks(self):
        return self.repository.get_all()
