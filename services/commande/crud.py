from sqlalchemy.orm import Session
import models
import schemas

def valider_commande(db: Session, commande: schemas.CommandeCreate):
    db_commande = models.Commande(client_id=commande.client_id, statut="validee")
    db.add(db_commande)
    db.commit()
    db.refresh(db_commande)
    return db_commande

def get_commande(db: Session, commande_id: int):
    return db.query(models.Commande).filter(models.Commande.id == commande_id).first()
