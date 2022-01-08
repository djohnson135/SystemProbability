# import uvicorn
from typing import List

from fastapi import Depends, FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware
import fastapi.security as _security
from pydantic.schema import model_schema

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update

from sql_app.crud import graph as crud_graph
from sql_app.crud import system as crud_system
from sql_app.crud import node as crud_node
from sql_app.crud import user as crud_user
# from sql_app.crud import helper as crud_helper
from . import dependencies, schemas 


# from .database import SessionLocal, engine


# models.Base.metadata.create_all(bind=engine)

dependencies.create_database()

#we can only send schemas from endpoints and not models
app = FastAPI()

#uvicorn sql_app.main:app --reload

#https://towardsdatascience.com/fastapi-cloud-database-loading-with-python-1f531f1d438a

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8000"], # * means all
#     allow_methods=["*"], #Get put etc...
#     allow_headers=["*"],
#     allow_credentials=True,
# )



# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.get("/api/")
async def root():
    return {"Message": "System Proabbility Calculator"}


@app.post("/users/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = await dependencies.get_user_by_email(email = user.email, db = db)
    if db_user:
        raise HTTPException(status_code=400, detail= "Email already in use")
    users = await crud_user.create_user(user = user, db = db)
    return await dependencies.create_token(users)
    
    
@app.post("/token/")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = await dependencies.authenticate_user(email = form_data.username, password = form_data.password, db = db)  #form_data.username refers to email
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return await dependencies.create_token(user)

@app.get("/users/me", response_model= schemas.User)
async def get_user(user: schemas.User = Depends(dependencies.get_current_user)):
    return user

@app.post("/users/me/SystemProbability/", response_model=schemas.SystemProbability)
async def create_system_of_probability(system: schemas.SystemProbabilityCreate, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud_system.create_system(user=user, db=db, system=system)

@app.get("/users/me/SystemProbability/", response_model=List[schemas.SystemProbability])
async def get_systems(user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud_system.get_systems(user=user, db = db)

@app.get("/users/me/SystemProbability/{system_id}", status_code=200)
async def get_system(system_id: int, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud_system.get_system(system_id=system_id, user=user, db=db)


# need to make edits to this because changing database structure

@app.delete("/users/me/SystemProbability/{system_id}", status_code=204)
async def delete_system(system_id: int, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    await crud_system.delete_system(system_id=system_id, user=user, db=db)
    return {"Message", "Successfully Deleted"}


@app.put("/users/me/SystemProbability/{system_id}", status_code=200)
async def update_system(system_id: int, system: schemas.SystemProbabilityCreate, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    await crud_system.update_system(system_id=system_id, system=system, db=db, user=user)
    return {"Message", "Successfully Updated"}


#need to add endpoints for graph and node
@app.get("/users/me/Node/{node_id}", response_model= schemas.Node)
async def get_node( node_id: int, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud_node.get_node( node_id=node_id, db=db)

@app.get("/users/me/Nodes/{system_id}", response_model= List[schemas.Node])
async def get_nodes(system_id:int, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud_node.get_nodes(system_id = system_id,  db=db)

@app.post("/users/me/SystemProbability/{system_id}/Nodes/",response_model= schemas.Node)
async def create_node(system_id: int, node: schemas.NodeCreate, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud_node.create_node(db=db, node=node,system_id=system_id, user=user)
    
@app.delete("/users/me/SystemProbability/{system_id}/Nodes/{node_id}", status_code=204)
async def delete_node(system_id: int,  node_id: int, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    await crud_node.delete_node(system_id=system_id, user=user, node_id = node_id, db=db)
    return {"Message", "Successfully Deleted"}
    
@app.put("/users/me/SystemProbability/{system_id}/Nodes/{node_id}", status_code=200)
async def update_node(system_id: int, node_id: int, node: schemas.NodeCreate, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    await crud_node.update_node(node_id = node_id, system_id=system_id, db=db, node=node, user=user)
    return {"Message", "Successfully Updated"}   



@app.post("/users/me/SystemProbability/{system_id}/Nodes/{node_id}/Graphs/",response_model= schemas.Graph)
async def create_graph(system_id: int, node_id: int, graph: schemas.GraphCreate, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud_graph.create_graph(db=db, graph=graph, system_id=system_id,node_id=node_id, user=user)

@app.get("/users/me/Graphs/{node_id}", response_model= List[schemas.Graph])
async def get_graphs( node_id : int, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud_graph.get_graphs(node_id = node_id,  db=db)

@app.delete("/users/me/SystemProbability/{system_id}/Nodes/{node_id}/Graphs/{graph_id}", status_code=204)
async def delete_graph(system_id: int, node_id: int, graph_id: int, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    await crud_graph.delete_graph(system_id=system_id, user=user, graph_id = graph_id, db=db, node_id=node_id)
    return {"Message", "Successfully Deleted"}

@app.put("/users/me/SystemProbability/{system_id}/Nodes/{node_id}/Graphs/{graph_id}", status_code=200)
async def update_graph(system_id: int, node_id : int, graph_id: int, graph: schemas.GraphCreate, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    await crud_graph.update_graph(graph_id = graph_id, system_id=system_id, db=db, graph=graph, user=user, node_id = node_id)
    return {"Message", "Successfully Updated"}   

@app.get("/users/me/Graph/{graph_id}", response_model= schemas.Graph)
async def get_graph(graph_id: int, user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud_graph.get_graph( graph_id=graph_id, db=db)




