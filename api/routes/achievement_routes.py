from typing import List

from api.core.db.services.achievement_service import AchievementService
from api.dependencies import get_achievement_service
from fastapi import APIRouter, Depends, HTTPException
from api.routes.response_models import AchievementResponseModel

achievement_router = APIRouter()


@achievement_router.get("/get/{achievement_id}", response_model=AchievementResponseModel, tags=["Achievement"])
async def get_achievement(
    achievement_id: int, service: AchievementService = Depends(get_achievement_service)
) -> AchievementResponseModel:
    """
    Get an achievement by ID.

    :param achievement_id: The ID of the achievement to retrieve.
    :param db: The database session.
    :return: The achievement data.
    :raises HTTPException: If the achievement is not found.
    """
    achievement = service.get_achievement(achievement_id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return AchievementResponseModel.model_validate(achievement)


@achievement_router.get("/get_all", response_model=List[AchievementResponseModel], tags=["Achievement"])
async def get_all_achievements(
    serivce: AchievementService = Depends(get_achievement_service),
) -> List[AchievementResponseModel]:
    """
    Get all achievements.

    :param db: The database session.
    :return: A list of all achievements.
    """
    achievements = serivce.get_all_achievements()
    if not achievements:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return [AchievementResponseModel.model_validate(achievement) for achievement in achievements]
