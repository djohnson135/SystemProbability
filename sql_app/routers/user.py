from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_current_user, get_db, create_token, authenticate_user
from ..schemas import User, UserCreate
from sqlalchemy.orm import Session
from ..crud import user as crud_user
import fastapi.security as _security


router = APIRouter(
    # prefix="/users/me",
    tags=["user"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.get("/users/me/", response_model= User)
async def get_user(user: User = Depends(get_current_user)):
    return user



@router.post("/users/")
async def create(user: UserCreate, db: Session = Depends(get_db)):

    db_user = await crud_user.get_by_email(email = user.email, db = db)
    if db_user:
        raise HTTPException(status_code=400, detail= "Email already in use")
    users = await crud_user.create(user = user, db = db)
    return await create_token(users)
    
    
@router.post("/token/")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(email = form_data.username, password = form_data.password, db = db)  #form_data.username refers to email
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return await create_token(user)
