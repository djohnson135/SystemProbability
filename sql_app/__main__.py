import uvicorn
from .dependencies import create_database
# from fastapi import Depends
import asyncio

from .routers.app import app
from . import processes
create_database()

# if __name__ == "__main__":
#     uvicorn.run("sql_app.__main__:app", host="0.0.0.0", port=8000, reload=True)



@app.get("/api/")
async def root():
    return {"Message": "System Proabbility Calculator"}




# processes.initgraphexample()

# try:
#     loop = asyncio.get_running_loop()
# except RuntimeError:  # 'RuntimeError: There is no current event loop...'
#     loop = None

# if loop and loop.is_running():
#     print('Async event loop already running. Adding coroutine to the event loop.')
#     tsk = loop.create_task(processes.set_adj_list(graph_id=1))
#     # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
#     # Optionally, a callback function can be executed when the coroutine completes
#     tsk.add_done_callback(
#         lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
# else:
#     print('Starting new event loop')
#     asyncio.run(processes.set_adj_list(graph_id=1))

# asyncio.run(processes.set_adj_list(graph_id=1))

# processes.set_adj_list(graph_id=1)
