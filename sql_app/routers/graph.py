from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ..dependencies import get_current_user, get_db 
from ..schemas import User, Graph, GraphCreate
from ..crud import graph as crud_graph

router = APIRouter(
    prefix="/users/me/SystemProbability/{system_id}/Nodes/{node_id}/Graphs",
    tags=["graph"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description" : "Not found"}},
)

get_router = APIRouter(
    prefix="/users/me/Graph/{graph_id}",
    tags=["get_by_id"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description" : "Not found"}},
)


@get_router.get("/", response_model= Graph)
async def get_by_id(graph_id: int,  db: Session = Depends(get_db)):
    return await crud_graph.get_by_id( graph_id=graph_id, db=db)



@router.post("/",response_model= Graph)
async def create(system_id: int, node_id: int, graph: GraphCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud_graph.create(db=db, graph=graph, system_id=system_id,node_id=node_id, user=user)

@router.get("/", response_model= List[Graph], dependencies=[Depends(get_current_user)] )
async def get_all( node_id : int,  db: Session = Depends(get_db)):
    return await crud_graph.get_all(node_id = node_id,  db=db)

@router.delete("/{graph_id}", status_code=204)
async def delete(system_id: int, node_id: int, graph_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    await crud_graph.delete(system_id=system_id, user=user, graph_id = graph_id, db=db, node_id=node_id)
    return {"Message", "Successfully Deleted"}

@router.put("/{graph_id}", status_code=200)
async def update(system_id: int, node_id : int, graph_id: int, graph: GraphCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    await crud_graph.update(graph_id = graph_id, system_id=system_id, db=db, graph=graph, user=user, node_id = node_id)
    return {"Message", "Successfully Updated"}   

