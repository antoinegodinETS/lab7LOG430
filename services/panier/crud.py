from sqlalchemy.orm import Session
import models
import schemas

def add_item(db: Session, item: schemas.PanierItemCreate):
    db_item = models.PanierItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_item(db: Session, item_id: int):
    item = db.query(models.PanierItem).filter(models.PanierItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()

def get_panier_by_client(db: Session, client_id: int):
    return db.query(models.PanierItem).filter(models.PanierItem.client_id == client_id).all()
