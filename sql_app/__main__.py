import uvicorn
from .dependencies import create_database
from sql_app.routers.app import app

create_database()


@app.get("/api/")
async def root():
    return {"Message": "System Proabbility Calculator"}



# uvicorn.run(app,host="0.0.0.0", port=8000)




