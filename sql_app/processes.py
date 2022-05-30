from fastapi.exceptions import HTTPException
from numpy.core.multiarray import array
from sqlalchemy.orm import Session
# import passlib.hash as _hash
# from sqlalchemy.sql.expression import false
# import jwt as _jwt
from fastapi import Depends
from sqlalchemy.sql.expression import null
# from .dependencies import get_db
# from . import models, schemas
from . import adj_list
# from .crud import graph


class probability:
    def __init__(self):
        self.dict = dict()
    def add_probability(self, node_id, probability): #as a string
        self.dict[node_id] = probability 
    def return_probability(self,node_id):
        return self.dict[node_id]
#illustrated graph
#maybe use strings and define start as start node or as 0


#lets say that we pass in the following adj list
# {
#               S : 1 3
#               1 : 2
#               2 : 4 5 6
#               3 : Null
#               4 : Null
#               5 : Null
#               6 : Null
# }





# each value in the matrix is a dictionary with its key (id) and probability
# def calculated_system_probability(adj_list):
#     """[summary]
#     Takes an adjacency list of dictionary pairs and returns the total system probability
#     Args:
#         adj_list (np.matrix): [description]
#     """
#     rows = adj_list.shape[0]
#     cols = adj_list.shape[1]
#     for x in range(0, rows):
#         #
#         for y in range(0, cols):
#             print (adj_list[x,y])
    
    
# example_list = [[{'Start': null}, {'1': 0.3} , {'3': 0.3}],
#                 [{'1': 0.3},{'2': 0.3}]
#                 [{'2':0.3},{'4':0.3},{'5':0.3},{'6':0.3}],
#                 [{'3': null}],
#                 [{'4':null}],
#                 [{'5':null}],
#                 [{'6':null}]]


 
# async def set_adj_list(graph_id: int, db: Session = Depends(get_db)): #
    
#     return await graph.get_by_id( graph_id=graph_id, db=db)

# def set_adj_list(graph_id: int, db: Session = get_db): #
#     db_graph = db.query(models.Graph).filter_by(id = graph_id).first()
#     if db_graph is None:
#         raise HTTPException(status_code=404, detail = "Graph does not exist")
#     return schemas.Graph.from_orm(db_graph)





