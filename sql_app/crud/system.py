from ..dependencies import schemas, Session, HTTPException, models, _dt
from .helper import system_selector


async def get_systems(user: schemas.User, db: Session):
    systems = db.query(models.SystemProbability).filter_by(owner_id = user.id)
    return list(map(schemas.SystemProbability.from_orm, systems)) #does from orm through each system and adds it to a list


async def get_system(user: schemas.User, db: Session, system_id: int):
    system = await system_selector(system_id=system_id, user=user, db=db) #query returns model
    return schemas.SystemProbability.from_orm(system)


async def delete_system(system_id: int, user: schemas.User, db: Session):
    system = await system_selector(system_id=system_id, user=user, db = db)
    nodes = db.query(models.Node).filter(models.Node.owner_id == system_id).all()
    # graphs = db.query(models.Graph).filter(models.Graph.owner_id == system_id).all()
    
    if nodes is not None:
        try:
            #db.query(models.Node).filter(models.Node.owner_id == system_id).delete()
            for o in nodes:
                delgraph = db.query(models.Graph).filter(models.Graph.owner_id == o.id).all()
                if delgraph is not None:
                    try:
                        for i in delgraph:
                            db.delete(i)
                        db.commit()
                    except Exception as e:
                        raise HTTPException(status_code = 400, detail= f"Unable to delete Graphs: {e}")
                db.delete(o)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code = 400, detail= f"Unable to delete Nodes: {e}")
        
    if system is not None:
        try:
            db.delete(system)
        except Exception as e:
            raise HTTPException(status_code = 400, detail= f"Unable to delete System: {e}")
    db.commit()
    
    
    
   
async def update_system(system_id: int, system: schemas.SystemProbabilityCreate, user: schemas.User, db: Session):
    system_db = await system_selector(system_id=system_id, user=user, db=db)
    system_db.name = system.name 
    system_db.date_last_updated = _dt.datetime.utcnow()
    # system_db.system_probability = system.system_probability #might change it to a function
    db.commit()
    db.refresh(system_db)
    return schemas.SystemProbability.from_orm(system_db)



async def create_system(user: schemas.User, db: Session, system: schemas.SystemProbabilityCreate):
    system = models.SystemProbability(**system.dict(), owner_id = user.id) #shorthand for copying the data from one model to the other
    db.add(system)
    db.commit()
    db.refresh(system)
    return schemas.SystemProbability.from_orm(system) #converts our model to a schema

