from typing import List

from api.core.db.services.user_service import UserService
from api.dependencies import get_user_service
from fastapi import APIRouter, Depends
from api.routes.user_routes import UserResponseModel

leaderboard_router = APIRouter()


@leaderboard_router.get("/get", response_model=List[UserResponseModel], tags=["Leaderboard"])
async def get_leaderboard(service: UserService = Depends(get_user_service)) -> List[UserResponseModel]:
    """
    Returns the top 10 users.

    :param db: Database session dependency.
    :return: A list of the top 10 users.
    """
    users = service.get_top_users()
    response = [UserResponseModel.model_validate(user) for user in users]
    return response
