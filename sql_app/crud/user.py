
from .. import models, schemas
import passlib.hash as _hash
from sqlalchemy.orm import Session


async def create_user(user: schemas.UserCreate, db: Session):
    user_obj = models.User(email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()



