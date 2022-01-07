from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
import datetime as _dt
import passlib.hash as _hash
from sqlalchemy.orm.relationships import foreign
#might use date time

from .database import Base



# #creating tables

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, index= True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    systemProbabilitys = relationship("SystemProbability", back_populates= "owner")
    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)




class SystemProbability(Base):

    __tablename__ = "systemProbability"

    #create columns
    id = Column(Integer, primary_key=True, index=True) #primary key. Add auto increment = true. 
    #maybe implement is_active
    #create relationship
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index = True)
    date_created = Column(DateTime, default = _dt.datetime.utcnow)
    date_last_updated = Column(DateTime, default = _dt.datetime.utcnow)
    
    system_probability = Column(Float,  default=0 )
    
    # Graphs = relationship("Graph", back_populates="owner")
    nodes = relationship("Node", back_populates="owner")

    owner = relationship("User",back_populates="systemProbabilitys")



class Node(Base):

    __tablename__ = "node"

    #create columns
    id = Column(Integer, primary_key=True, index=True) #unique = True
    name = Column(String, index=True)
    probability = Column(Float, index = True)
    owner_id = Column(Integer, ForeignKey("systemProbability.id"))
    #create relationship
    owner = relationship("SystemProbability", back_populates="nodes")
    graphs = relationship("Graph", back_populates="owner")
    
    
    
    
#creating tables
class Graph(Base):

    __tablename__ = "graph"

    #create columns
    id = Column(Integer, primary_key=True, index=True)
    edge_node_id = Column(Integer,  nullable=False) #ForeignKey("node.id"),
    owner_id = Column(Integer, ForeignKey("node.id"), nullable = False) #id of systemProb
    #create relationship
    owner = relationship("Node", back_populates="graphs", foreign_keys= "Graph.owner_id") #, foreign_keys= "Graph.owner_id"
    # edge_node = relationship("Node", foreign_keys= "Node.id") #foreign_keys= "Graph.edge_node_id"


