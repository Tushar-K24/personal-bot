from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from .service import main_func as main_func_a

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/api_a/{num}", tags=["api_a"])
async def view_a(
    num: int,
) -> dict[str, int]:
    return main_func_a(num)
