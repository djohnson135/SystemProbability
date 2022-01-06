from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} #needed for SQLlite because sqllite by default allows only one thread
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #create sessionlocal class using sessionmaker function

Base = declarative_base() #create a base class that will later be inherited from
