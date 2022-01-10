from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ..dependencies import get_current_user, get_db 
from ..schemas import User, Node, NodeCreate
from ..crud import node as crud_node

router = APIRouter(
    prefix="/users/me/SystemProbability/{system_id}/Nodes",
    tags=["node"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description" : "Not found"}},
)

#router to get node
get_router = APIRouter(
    prefix = "/users/me/Node",
    tags=["get_by_id"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description" : "Not found"}},
)



#need to add endpoints for graph and node

@get_router.get("/{node_id}", response_model= Node)
async def get_by_id( node_id: int,  db: Session = Depends(get_db)):
    return await crud_node.get_by_id( node_id=node_id, db=db)



@router.get("/", response_model= List[Node], dependencies=[Depends(get_current_user)])
async def get_all(system_id:int, db: Session = Depends(get_db)):
    return await crud_node.get_all(system_id = system_id,  db=db)


@router.post("/",response_model= Node)
async def create(system_id: int, node: NodeCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud_node.create(db=db, node=node,system_id=system_id, user=user)
    
@router.delete("/{node_id}", status_code=204)
async def delete(system_id: int,  node_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    await crud_node.delete(system_id=system_id, user=user, node_id = node_id, db=db)
    return {"Message", "Successfully Deleted"}
    
@router.put("/{node_id}", status_code=200)
async def update(system_id: int, node_id: int, node: NodeCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    await crud_node.update(node_id = node_id, system_id=system_id, db=db, node=node, user=user)
    return {"Message", "Successfully Updated"}   



async def return_router():
    return router.include_router(get_router)