
from .. import schemas, models
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .helper import system_selector, node_selector



async def create_node(db: Session, node: schemas.NodeCreate, system_id: int, user: schemas.User):
    await system_selector(user=user, db=db, system_id=system_id)      
    node = models.Node(**node.dict(), owner_id = system_id)
    db.add(node)
    db.commit()
    db.refresh(node)
    return schemas.Node.from_orm(node)

        
async def get_node(db: Session, node_id: int):
    node = db.query(models.Node).filter_by(id = node_id).first()
    if node is None:
        raise HTTPException(status_code=404, detail = "Node does not exist")
    return schemas.Node.from_orm(node)



async def get_nodes(db: Session, system_id: int): 
    nodes = db.query(models.Node).filter_by(owner_id = system_id)
    if nodes is None:
        raise HTTPException(status_code=404, detail = "Node does not exist") 
    return list(map(schemas.Node.from_orm, nodes))


async def delete_node(system_id: int,  node_id: int, user: schemas.User , db: Session ):
    # system = await system_selector(system_id=system_id, user=user, db=db)
    system = await system_selector(system_id=system_id, user=user, db=db)
    node = await node_selector(node_id=node_id, db=db, system = system)
    db.delete(node)
    db.commit()

async def update_node(system_id: int,  node_id: int, node: schemas.NodeCreate , db: Session, user: schemas.User):
    system = await system_selector(system_id=system_id, user=user, db=db)
    node_db = await node_selector(node_id=node_id, db=db, system = system)
    node_db.name = node.name
    node_db.probability = node.probability
    db.commit()
    db.refresh(node_db)
    return schemas.Node.from_orm(node_db)