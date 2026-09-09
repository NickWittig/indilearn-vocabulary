from api.core.db.services.achievement_service import AchievementService
from api.core.db.services.item_service import ItemService
from api.core.db.services.rank_service import RankService
from api.core.db.services.user_service import UserService
from api.core.db.session import get_db
from fastapi import Depends, Request
from sqlalchemy.orm import Session


def get_authenticated_username(request: Request):
    # Assuming the username is stored in the request state by the middleware
    return request.state.username


def get_item_service(session: Session = Depends(get_db)) -> ItemService:
    return ItemService(session)


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    return UserService(session)


def get_rank_service(session: Session = Depends(get_db)) -> RankService:
    return RankService(session)


def get_achievement_service(session: Session = Depends(get_db)) -> AchievementService:
    return AchievementService(session)
