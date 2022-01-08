from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/users/me",
    # tags=["users"]
    dependencies=[Depends(get_current_user)],
    responses={404: {"description" : "Not found"}}
)

@router.get("/")
async def read_items():
    pass