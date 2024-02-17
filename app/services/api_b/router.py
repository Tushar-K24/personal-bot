from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from .service import main_func as main_func_b

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/api_b/{num}", tags=["api_b"])
async def view_b(
    num: int,
) -> dict[str, int]:
    return main_func_b(num)
