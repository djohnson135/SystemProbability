from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ..dependencies import get_current_user, get_db 
from ..schemas import User, SystemProbability, SystemProbabilityCreate
from ..crud import system as crud_system

router = APIRouter(
    prefix="/users/me/SystemProbability",
    tags=["system"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description" : "Not found"}},
)


@router.post("/", response_model=SystemProbability)
async def create(system: SystemProbabilityCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud_system.create(user=user, db=db, system=system)

@router.get("/", response_model=List[SystemProbability])
async def get_all(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud_system.get_all(user=user, db = db)

@router.get("/{system_id}", status_code=200)
async def get_by_id(system_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud_system.get_by_id(system_id=system_id, user=user, db=db)


# need to make edits to this because changing database structure

@router.delete("/{system_id}", status_code=204)
async def delete(system_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    await crud_system.delete(system_id=system_id, user=user, db=db)
    return {"Message", "Successfully Deleted"}


@router.put("/{system_id}", status_code=200)
async def update(system_id: int, system: SystemProbabilityCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    await crud_system.update(system_id=system_id, system=system, db=db, user=user)
    return {"Message", "Successfully Updated"}