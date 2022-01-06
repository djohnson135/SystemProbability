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
    SystemProbabilitys = relationship("SystemProbability", back_populates= "owner")
    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)




class SystemProbability(Base):

    __tablename__ = "SystemProbability"

    #create columns
    id = Column(Integer, primary_key=True, index=True) #primary key. Add auto increment = true. 
    #maybe implement is_active
    #create relationship
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index = True)
    date_created = Column(DateTime, default = _dt.datetime.utcnow)
    date_last_updated = Column(DateTime, default = _dt.datetime.utcnow)
    
    system_probability = Column(Float,  default=0 )
    
    Graphs = relationship("Graph", back_populates="owner")
    Nodes = relationship("Node", back_populates="owner")

    owner = relationship("User",back_populates="SystemProbabilitys")


#creating tables
class Graph(Base):

    __tablename__ = "Graph"

    #create columns
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(Integer, index = True)
    edge_id = Column(Integer, index = True)
    owner_id = Column(Integer, ForeignKey("SystemProbability.id")) #id of systemProb
    #create relationship
    owner = relationship("SystemProbability", back_populates="Graphs")




class Node(Base):

    __tablename__ = "Node"

    #create columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    probability = Column(Float, index = True)
    owner_id = Column(Integer, ForeignKey("SystemProbability.id"))
    #create relationship
    owner = relationship("SystemProbability", back_populates="Nodes")
