from api.core.db.schemas import RankSchema
from api.core.db.services.rank_service import RankService
from api.core.db.services.user_service import UserService
from api.dependencies import get_authenticated_username, get_rank_service, get_user_service
from fastapi import APIRouter, Depends, HTTPException

rank_router = APIRouter()


@rank_router.get("/get/{rank_id}", response_model=RankSchema, tags=["Rank"])
async def get_rank(rank_id: int, service: RankService = Depends(get_rank_service)):
    """
    Get a rank by ID.

    :param rank_id: The ID of the rank.
    :param service: The rank service.
    :return: The rank data.
    :raises HTTPException: If the rank is not found.
    """
    rank, error = service.get_rank_by_id(rank_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return rank


@rank_router.get("/get_current", response_model=RankSchema, tags=["Rank"])
async def get_rank(
    user_name: str = Depends(get_authenticated_username),
    service: RankService = Depends(get_rank_service),
    user_service: UserService = Depends(get_user_service),
):
    """
    Get a rank by ID.

    :return: The rank data.
    :raises HTTPException: If the rank is not found.
    """
    user, error = user_service.get_user_by_username(user_name)
    rank, error = service.get_rank_by_id(user.rank_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return rank
