
from .. import schemas, models
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from .helper import system_selector, node_selector, graph_selector


async def update(system_id: int,  graph_id: int, graph: schemas.GraphCreate , db: Session, user: schemas.User, node_id: int):
    system = await system_selector(system_id=system_id, user=user, db=db)
    node_db = await node_selector(node_id=node_id, system=system, db=db)
    graph_db = await graph_selector(graph_id=graph_id, db=db, node = node_db)
    graph_db.edge_node_id = graph.edge_node_id
    db.commit()
    db.refresh(graph_db)
    return schemas.Graph.from_orm(graph_db)



async def delete(system_id: int,  graph_id: int, node_id: int, user: schemas.User , db: Session ):
    # system = await system_selector(system_id=system_id, user=user, db=db)
    system = await system_selector(system_id=system_id, user=user, db=db)
    node_db = await node_selector(node_id=node_id, system=system, db=db)
    graph_db = await graph_selector(graph_id=graph_id, db=db, node = node_db)
    db.delete(graph_db)
    db.commit()

async def get_all( db: Session, node_id: int): 
    # system = await system_selector(user=user, db=db, system_id = system_id)
    # node = await node_selector(system=system, db=db, node_id=node_id)
    graphs = db.query(models.Graph).filter_by(owner_id = node_id) 
    if graphs is None:
        raise HTTPException(status_code=404, detail = "Graph does not exist")
    return list(map(schemas.Graph.from_orm, graphs))  

        
async def get_by_id(db: Session, graph_id: int):
    # system = await system_selector(system_id=system_id, user=user, db=db)
    graph = db.query(models.Graph).filter_by(id = graph_id).first()
    if graph is None:
        raise HTTPException(status_code=404, detail = "Graph does not exist")
    return schemas.Graph.from_orm(graph)

async def create(db: Session, graph: schemas.GraphCreate, node_id: int, user: schemas.User, system_id: int):
    #just exception/error cheking
    db_system = await system_selector(user=user, db=db, system_id=system_id)
    await node_selector(node_id = node_id, system = db_system , db = db)      
    #done error checking
    graph = models.Graph(**graph.dict(), owner_id = node_id)
    db.add(graph)
    db.commit()
    db.refresh(graph)
    return schemas.Graph.from_orm(graph)