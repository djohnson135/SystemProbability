from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
import passlib.hash as _hash
from sqlalchemy.sql.expression import false
import jwt as _jwt
from fastapi import Depends
import fastapi.security as _security
from .database import SessionLocal, engine
import datetime as _dt

from . import models, schemas

JWT_SECRET = "myjwtsecret"
oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/token/")
# from .database import SessionLocal, engine

#pass in skip and limit values into function
#return db.query(models.User).offset(skip).limit(limit).all()

#use filter to get by id

#create the database


def create_database():
    return models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#HELPER FUNCTIONS
async def system_selector(system_id: int, user: schemas.User, db: Session):
    system = db.query(models.SystemProbability).filter_by(owner_id = user.id).filter(models.SystemProbability.id == system_id).first()

    if system is None:
        raise HTTPException(status_code=404, detail = "System does not exist")
    
    return system

async def node_selector(node_id: int, system: schemas.SystemProbability, db: Session):
    node = db.query(models.Node).filter_by(owner_id = system.id).filter(models.Node.id == node_id).first()
    if node is None:
        raise HTTPException(status_code=404, detail = "Node does not exist")
    return node
    
async def graph_selector(graph_id: int, node: schemas.Node, db: Session):
    graph = db.query(models.Graph).filter_by(owner_id = node.id).filter(models.Graph.id == graph_id).first()
    if graph is None:
        raise HTTPException(status_code=404, detail = "Graph does not exist")
    return graph


#END OF HELPER FUNCTIONS

async def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()

async def create_user(user: schemas.UserCreate, db: Session):
    user_obj = models.User(email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: Session):
    user = await get_user_by_email(db = db, email = email)
    if not user or not user.verify_password(password):
        return False
    return user

async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)   #from orm takes a model and maps it to the schema. Makes it a schema object
    token = _jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type= "bearer")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2schema)):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise HTTPException(status_code=401, detail= "Invalid Email or Password")
    return schemas.User.from_orm(user)
        
        


async def create_system(user: schemas.User, db: Session, system: schemas.SystemProbabilityCreate):
    system = models.SystemProbability(**system.dict(), owner_id = user.id) #shorthand for copying the data from one model to the other
    db.add(system)
    db.commit()
    db.refresh(system)
    return schemas.SystemProbability.from_orm(system) #converts our model to a schema

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


async def get_systems(user: schemas.User, db: Session):
    systems = db.query(models.SystemProbability).filter_by(owner_id = user.id)
    return list(map(schemas.SystemProbability.from_orm, systems)) #does from orm through each system and adds it to a list

async def get_system(user: schemas.User, db: Session, system_id: int):
    system = await system_selector(system_id=system_id, user=user, db=db) #query returns model
    return schemas.SystemProbability.from_orm(system)

async def get_nodes(db: Session, system_id: int): 
    nodes = db.query(models.Node).filter_by(owner_id = system_id)
    if nodes is None:
        raise HTTPException(status_code=404, detail = "Node does not exist") 
    return list(map(schemas.Node.from_orm, nodes))


async def delete_system(system_id: int, user: schemas.User, db: Session):
    system = await system_selector(system_id=system_id, user=user, db = db)
    nodes = db.query(models.Node).filter(models.Node.owner_id == system_id).all()
    # graphs = db.query(models.Graph).filter(models.Graph.owner_id == system_id).all()
    
    if nodes is not None:
        try:
            #db.query(models.Node).filter(models.Node.owner_id == system_id).delete()
            for o in nodes:
                delgraph = db.query(models.Graph).filter(models.Graph.owner_id == o.id).all()
                if delgraph is not None:
                    try:
                        for i in delgraph:
                            db.delete(i)
                        db.commit()
                    except Exception as e:
                        raise HTTPException(status_code = 400, detail= f"Unable to delete Graphs: {e}")
                db.delete(o)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code = 400, detail= f"Unable to delete Nodes: {e}")
        
    if system is not None:
        try:
            db.delete(system)
        except Exception as e:
            raise HTTPException(status_code = 400, detail= f"Unable to delete System: {e}")
    db.commit()
    
async def update_system(system_id: int, system: schemas.SystemProbabilityCreate, user: schemas.User, db: Session):
    system_db = await system_selector(system_id=system_id, user=user, db=db)
    system_db.name = system.name 
    system_db.date_last_updated = _dt.datetime.utcnow()
    # system_db.system_probability = system.system_probability #might change it to a function
    db.commit()
    db.refresh(system_db)
    return schemas.SystemProbability.from_orm(system_db)

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

async def update_graph(system_id: int,  graph_id: int, graph: schemas.GraphCreate , db: Session, user: schemas.User, node_id: int):
    system = await system_selector(system_id=system_id, user=user, db=db)
    node_db = await node_selector(node_id=node_id, system=system, db=db)
    graph_db = await graph_selector(graph_id=graph_id, db=db, node = node_db)
    graph_db.edge_node_id = graph.edge_node_id
    db.commit()
    db.refresh(graph_db)
    return schemas.Graph.from_orm(graph_db)

async def delete_graph(system_id: int,  graph_id: int, node_id: int, user: schemas.User , db: Session ):
    # system = await system_selector(system_id=system_id, user=user, db=db)
    system = await system_selector(system_id=system_id, user=user, db=db)
    node_db = await node_selector(node_id=node_id, system=system, db=db)
    graph_db = await graph_selector(graph_id=graph_id, db=db, node = node_db)
    db.delete(graph_db)
    db.commit()

async def get_graphs( db: Session, node_id: int): 
    # system = await system_selector(user=user, db=db, system_id = system_id)
    # node = await node_selector(system=system, db=db, node_id=node_id)
    graphs = db.query(models.Graph).filter_by(owner_id = node_id) 
    if graphs is None:
        raise HTTPException(status_code=404, detail = "Graph does not exist")
    return list(map(schemas.Graph.from_orm, graphs))  

        
async def get_graph(db: Session, graph_id: int):
    # system = await system_selector(system_id=system_id, user=user, db=db)
    graph = db.query(models.Graph).filter_by(id = graph_id).first()
    if graph is None:
        raise HTTPException(status_code=404, detail = "Graph does not exist")
    return schemas.Graph.from_orm(graph)

async def create_graph(db: Session, graph: schemas.GraphCreate, node_id: int, user: schemas.User, system_id: int):
    #just exception/error cheking
    db_system = await system_selector(user=user, db=db, system_id=system_id)
    await node_selector(node_id = node_id, system = db_system , db = db)      
    #done error checking
    graph = models.Graph(**graph.dict(), owner_id = node_id)
    db.add(graph)
    db.commit()
    db.refresh(graph)
    return schemas.Graph.from_orm(graph)

