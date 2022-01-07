
from typing import List, Optional
import datetime as _dt

from pydantic import BaseModel

#creating the pedantic model
#schema
# : declares typ 
# = sets value




class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    hashed_password: str
    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


class GraphBase(BaseModel):

    edge_node_id: int




class Graph(GraphBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True




class NodeBase(BaseModel):

    name: str
    probability: float




class Node(NodeBase):
    id: int
    owner_id: int
    Graphs: List[Graph] = []
    class Config:
        orm_mode = True




class SystemProbabilityBase(BaseModel):

    name: str
    

    # description: Optional[str] = None


class SystemProbability(SystemProbabilityBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime
    system_probability: float
    # Graphs: List[Graph] = []
    Nodes: List[Node] = []

    
    class Config:
        orm_mode = True


class ProbabilityUpdate(SystemProbabilityBase): 
    system_probability: float


class GraphCreate(GraphBase):
    pass


class SystemProbabilityCreate(SystemProbabilityBase):
    pass
    

class NodeCreate(NodeBase):
    pass

#need to create my response models