from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_current_user
from ..schemas import User

router = APIRouter(
    prefix="/users/me",
    # tags=["users"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model= User)
async def get_user(user: User = Depends(get_current_user)):
    return user
