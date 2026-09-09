from typing import Any, Dict

from api.core.db.services import user_service
from api.core.db.services.item_service import ItemService
from api.core.score.score_manager import ScoreManager
from api.dependencies import get_authenticated_username, get_item_service, get_user_service
from fastapi import APIRouter, Depends, HTTPException
from api.routes.response_models import ItemCheckModel, ItemResponseModel

item_router = APIRouter()


@item_router.get("/get", response_model=ItemResponseModel, tags=["Item"])
async def get_item(
    user_name: str = Depends(get_authenticated_username),
    service: ItemService = Depends(get_item_service),
    user_service: user_service.UserService = Depends(get_user_service),
) -> ItemResponseModel:
    """
    Get an item for a user.

    :param user_id: The ID of the user.
    :return: The item data.
    :raises HTTPException: If the user_id is not provided or item is not found.
    """
    user, error = user_service.get_user_by_username(user_name)

    item, error = service.get_item_for_user(user)
    if error:
        raise HTTPException(status_code=404, detail=error)

    response = ItemResponseModel.model_validate(item)

    return response


@item_router.post("/check", response_model=Dict[str, Any], tags=["Item"])
async def check_item(
    data: ItemCheckModel,
    user_name: str = Depends(get_authenticated_username),
    item_service: ItemService = Depends(get_item_service),
    user_service: user_service.UserService = Depends(get_user_service),
) -> Dict[str, bool | None]:
    """
    Check if the solution to an item is correct.

    :param data: The data containing item_id, user_id, and solution.
    :param service: The item service.
    :return: A dictionary indicating if the solution is correct.
    :raises HTTPException: If the required fields are not provided or if there is an error checking the solution.
    """
    item_id = data.item_id
    solution = data.user_solution

    if item_id is None or solution is None:
        raise HTTPException(status_code=400, detail="item_id and solution are required")

    user, error = user_service.get_user_by_username(user_name)
    is_correct, error_codes, error = item_service.check_item_solution(item_id, user, solution)
    item_solutions = item_service.get_item_sample_solutions(item_id)
    score = ScoreManager.get_score(is_correct, error_codes)
    user_service.add_user_score(user, score)
    user_service.update_rank(user)
    user_service.check_new_user_achievements_by_user_name(user_name)
    if error:
        raise HTTPException(status_code=404, detail=error)

    return {"correct": is_correct, "solutions": item_solutions, "error_codes": error_codes}
