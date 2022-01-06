from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
import passlib.hash as _hash
from sqlalchemy.sql.expression import false
import jwt as _jwt
from fastapi import Depends
from . import models, schemas
import numpy as np

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
    

