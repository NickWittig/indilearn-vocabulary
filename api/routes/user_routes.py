from typing import Any, Dict, List

from api.core.db.services.user_service import UserService
from api.dependencies import get_authenticated_username, get_user_service
from fastapi import APIRouter, Depends, HTTPException
from api.routes.response_models import UserResponseModel

user_router = APIRouter()


@user_router.get("/get", response_model=UserResponseModel, tags=["User"])
async def get_user(
    user_name: str = Depends(get_authenticated_username), service: UserService = Depends(get_user_service)
) -> UserResponseModel:
    """
    Get the user by username. Only return the user object for the calling user.
    """
    user, error = service.get_user_by_username(user_name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    response = UserResponseModel.model_validate(user)
    return response


@user_router.get("/achievements/check", response_model=Dict[str, Any], tags=["User"])
async def check_user_achievements(
    user_name: str = Depends(get_authenticated_username), service: UserService = Depends(get_user_service)
) -> Dict[str, Any]:
    """
    Check and award newly unlocked achievements for the authenticated user based on their username.
    """
    achievement_ids, error = service.check_new_user_achievements_by_user_name(user_name)
    if error:
        raise HTTPException(status_code=404, detail=error)

    return {"unlocked_achievement_ids": achievement_ids}


@user_router.get("/achievements/get", response_model=Dict[str, List[int]], tags=["User"])
async def get_user_achievements(
    user_name: str = Depends(get_authenticated_username), service: UserService = Depends(get_user_service)
) -> Dict[str, Any]:
    """
    Get achievements for the authenticated user based on their username.
    """
    achievement_ids, error = service.get_user_achievements_ids(user_name)
    if error:
        raise HTTPException(status_code=404, detail=error)

    return {"unlocked_achievement_ids": achievement_ids}
