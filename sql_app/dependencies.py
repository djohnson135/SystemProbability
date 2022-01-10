# from fastapi import Header
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
# from sqlalchemy.sql.expression import false
import jwt as _jwt
from fastapi import Depends
import fastapi.security as _security
from .database import SessionLocal, engine
from .crud.user import get_by_email

from . import models, schemas



JWT_SECRET = "myjwtsecret"
oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/token/")


def create_database():
    return models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def authenticate_user(email: str, password: str, db: Session):
    user = await get_by_email(db = db, email = email)
    if not user or not user.verify_password(password):
        return False
    return user

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2schema)):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise HTTPException(status_code=401, detail= "Invalid Email or Password")
    return schemas.User.from_orm(user)

async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)   #from orm takes a model and maps it to the schema. Makes it a schema object
    token = _jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type= "bearer")




