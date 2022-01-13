from fastapi import FastAPI

from . import graph, node, system, user


app = FastAPI()
# dependencies=[Depends(dependencies.get_current_user)]

app.include_router(user.router)
app.include_router(system.router)
app.include_router(node.get_router)
app.include_router(node.router)
app.include_router(graph.router)
app.include_router(graph.get_router)

# @app.get("/api/")
# async def root():
#     return {"Message": "System Proabbility Calculator"}
