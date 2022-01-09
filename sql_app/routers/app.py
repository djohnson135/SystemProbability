from fastapi import FastAPI
from sql_app.routers.user import router as user_route
from sql_app.routers.graph import router as graph_route
from sql_app.routers.graph import get_router as get_graph_route
from sql_app.routers.node import router as node_route
from sql_app.routers.node import get_router as get_node_route
from sql_app.routers.system import router as system_route

app = FastAPI()
# dependencies=[Depends(dependencies.get_current_user)]

app.include_router(user_route)
app.include_router(system_route)
app.include_router(get_node_route)
app.include_router(node_route)
app.include_router(graph_route)
app.include_router(get_graph_route)

@app.get("/api/")
async def root():
    return {"Message": "System Proabbility Calculator"}
