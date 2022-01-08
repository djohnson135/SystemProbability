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

from sql_app.routers import user as user_route
from sql_app.routers import graph as graph_route
from sql_app.routers import node as node_route
from sql_app.routers import system as system_route
# from .database import SessionLocal, engine


dependencies.create_database()


app = FastAPI()
# dependencies=[Depends(dependencies.get_current_user)]

app.include_router(user_route.router)
app.include_router(system_route.router)
app.include_router(node_route.get_router)
app.include_router(node_route.router)
app.include_router(graph_route.router)
app.include_router(graph_route.get_router)

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






