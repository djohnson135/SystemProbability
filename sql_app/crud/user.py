from ..dependencies import Session, models, schemas, _hash


async def create_user(user: schemas.UserCreate, db: Session):
    user_obj = models.User(email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj




