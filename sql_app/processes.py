from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
# import passlib.hash as _hash
# from sqlalchemy.sql.expression import false
# import jwt as _jwt
from fastapi import Depends
from .dependencies import get_db
from . import models, schemas
import numpy as np
from .crud import graph



class system_probability:
    adj_list: np.matrix 
  
        
    async def calculated_system_probability(adj_list: np.matrix):
        """[summary]
        Takes an adjacency list of dictionary pairs and returns the total system probability
        Args:
            adj_list (np.matrix): [description]
        """
        rows = adj_list.shape[0]
        cols = adj_list.shape[1]
        for x in range(0, rows):
            #
            for y in range(0, cols):
                print (adj_list[x,y])
        
        

# async def set_adj_list(graph_id: int, db: Session = Depends(get_db)): #
    
#     return await graph.get_by_id( graph_id=graph_id, db=db)

def set_adj_list(graph_id: int, db: Session = get_db): #
    db_graph = db.query(models.Graph).filter_by(id = graph_id).first()
    if db_graph is None:
        raise HTTPException(status_code=404, detail = "Graph does not exist")
    return schemas.Graph.from_orm(db_graph)