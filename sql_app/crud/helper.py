from ..dependencies import schemas, Session, HTTPException, models




#HELPER FUNCTIONS
async def system_selector(system_id: int, user: schemas.User, db: Session):
    system = db.query(models.SystemProbability).filter_by(owner_id = user.id).filter(models.SystemProbability.id == system_id).first()

    if system is None:
        raise HTTPException(status_code=404, detail = "System does not exist")
    
    return system

async def node_selector(node_id: int, system: schemas.SystemProbability, db: Session):
    node = db.query(models.Node).filter_by(owner_id = system.id).filter(models.Node.id == node_id).first()
    if node is None:
        raise HTTPException(status_code=404, detail = "Node does not exist")
    return node
    
async def graph_selector(graph_id: int, node: schemas.Node, db: Session):
    graph = db.query(models.Graph).filter_by(owner_id = node.id).filter(models.Graph.id == graph_id).first()
    if graph is None:
        raise HTTPException(status_code=404, detail = "Graph does not exist")
    return graph