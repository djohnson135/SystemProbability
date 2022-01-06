from typing import List

from fastapi import Depends, FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware
import fastapi.security as _security
from pydantic.schema import model_schema

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update

from . import crud, models, schemas



# from .database import SessionLocal, engine


# models.Base.metadata.create_all(bind=engine)

crud.create_database()

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
async def create_user(user: schemas.UserCreate, db: Session = Depends(crud.get_db)):
    db_user = await crud.get_user_by_email(email = user.email, db = db)
    if db_user:
        raise HTTPException(status_code=400, detail= "Email already in use")
    users = await crud.create_user(user = user, db = db)
    return await crud.create_token(users)
    
    
@app.post("/token/")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(crud.get_db)):
    user = await crud.authenticate_user(email = form_data.username, password = form_data.password, db = db)  #form_data.username refers to email
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return await crud.create_token(user)

@app.get("/users/me", response_model= schemas.User)
async def get_user(user: schemas.User = Depends(crud.get_current_user)):
    return user

@app.post("/users/me/SystemProbability/", response_model=schemas.SystemProbability)
async def create_system_of_probability(system: schemas.SystemProbabilityCreate, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    return await crud.create_system(user=user, db=db, system=system)

@app.get("/users/me/SystemProbability/", response_model=List[schemas.SystemProbability])
async def get_systems(user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    return await crud.get_systems(user=user, db = db)

@app.get("/users/me/SystemProbability/{system_id}", status_code=200)
async def get_system(system_id: int, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    return await crud.get_system(system_id=system_id, user=user, db=db)

@app.delete("/users/me/SystemProbability/{system_id}", status_code=204)
async def delete_system(system_id: int, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    
    await crud.delete_system(system_id=system_id, user=user, db=db)
    return {"Message", "Successfully Deleted"}


@app.put("/users/me/SystemProbability/{system_id}", status_code=200)
async def update_system(system_id: int, system: schemas.SystemProbabilityCreate, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    await crud.update_system(system_id=system_id, system=system, db=db, user=user)
    return {"Message", "Successfully Updated"}


#need to add endpoints for graph and node
@app.get("/users/me/SystemProbability/{system_id}/Nodes/{node_id}", response_model= schemas.Node)
async def get_node(system_id: int, node_id: int, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    return await crud.get_node(system_id=system_id, node_id=node_id,user=user, db=db)

@app.get("/users/me/SystemProbability/{system_id}/Nodes/", response_model= List[schemas.Node])
async def get_nodes(system_id:int, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    return await crud.get_nodes(system_id = system_id, user = user, db=db)

@app.post("/users/me/SystemProbability/{system_id}/Nodes/",response_model= schemas.Node)
async def create_node(system_id: int, node: schemas.NodeCreate, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    return await crud.create_node(db=db, node=node,system_id=system_id, user=user)
    
@app.delete("/users/me/SystemProbability/{system_id}/Nodes/{node_id}", status_code=204)
async def delete_node(system_id: int,  node_id: int, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    await crud.delete_node(system_id=system_id, user=user, node_id = node_id, db=db)
    return {"Message", "Successfully Deleted"}
    
@app.put("/users/me/SystemProbability/{system_id}/Nodes/{node_id}", status_code=200)
async def update_node(system_id: int, node_id: int, node: schemas.NodeCreate, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    await crud.update_node(node_id = node_id, system_id=system_id, db=db, node=node, user=user)
    return {"Message", "Successfully Updated"}   

@app.post("/users/me/SystemProbability/{system_id}/Graphs/",response_model= schemas.Graph)
async def create_graph(system_id: int, graph: schemas.GraphCreate, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    return await crud.create_graph(db=db, graph=graph, system_id=system_id, user=user)

@app.get("/users/me/SystemProbability/{system_id}/Graphs/", response_model= List[schemas.Graph])
async def get_graphs(system_id:int, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    return await crud.get_graphs(system_id = system_id, user = user, db=db)

@app.delete("/users/me/SystemProbability/{system_id}/Graphs/{graph_id}", status_code=204)
async def delete_graph(system_id: int,  graph_id: int, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    await crud.delete_graph(system_id=system_id, user=user, graph_id = graph_id, db=db)
    return {"Message", "Successfully Deleted"}

@app.put("/users/me/SystemProbability/{system_id}/Graphs/{graph_id}", status_code=200)
async def update_graph(system_id: int, graph_id: int, graph: schemas.GraphCreate, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    await crud.update_graph(graph_id = graph_id, system_id=system_id, db=db, graph=graph, user=user)
    return {"Message", "Successfully Updated"}   

@app.get("/users/me/SystemProbability/{system_id}/Graphs/{graph_id}", response_model= schemas.Graph)
async def get_graph(system_id: int, graph_id: int, user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(crud.get_db)):
    return await crud.get_graph(system_id=system_id, graph_id=graph_id,user=user, db=db)
