from .service import UserDataBuilderService
from fastapi import APIRouter, Depends

from app.core.exception_handler import success_response_builder
from app.core.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])
user_data_builder_service = UserDataBuilderService()


@router.post("/user-history/add", tags=["Database Population"])
async def add_user_data() -> None:
    await user_data_builder_service.add_user_data_to_db()
    return success_response_builder(data=None)
