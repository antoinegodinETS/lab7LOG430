from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import schemas
import crud
import database
from prometheus_fastapi_instrumentator import Instrumentator



app = FastAPI()
Instrumentator().instrument(app).expose(app)

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/panier/", response_model=schemas.PanierItemOut)
def ajouter_item(item: schemas.PanierItemCreate, db: Session = Depends(get_db)):
    return crud.add_item(db, item)

@app.delete("/panier/{item_id}")
def supprimer_item(item_id: int, db: Session = Depends(get_db)):
    crud.remove_item(db, item_id)
    return {"message": "Item supprimé"}

@app.get("/panier/{client_id}", response_model=list[schemas.PanierItemOut])
def lire_panier(client_id: int, db: Session = Depends(get_db)):
    return crud.get_panier_by_client(db, client_id)
