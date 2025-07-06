from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from common.database import get_db
from logistique import services as log_services
from schemas.stock_schemas import StockLogistiqueOut

router = APIRouter(prefix="/api/v1/logistique", tags=["Logistique"])

@router.get("/stock", response_model=list[StockLogistiqueOut])
def get_stock_logistique(db: Session = Depends(get_db)):
    return log_services.consulter_stock_logistique()

@router.get("/demandes")
def get_demandes_en_attente(db: Session = Depends(get_db)):
    return log_services.recuperer_demandes_en_attente()

@router.post("/approvisionner")
def approvisionner(produit_id: int, quantite: int, magasin_id: int, db: Session = Depends(get_db)):
    return log_services.approvisionner_magasin(produit_id, quantite, magasin_id)

@router.post("/verifier_reapprovisionnement")
def verifier(magasin_id: int, produit_id: int, quantite: int, db: Session = Depends(get_db)):
    return log_services.verifier_et_reapprovisionner(magasin_id, produit_id, quantite)

@router.post("/demande")
def creer_demande(magasin_id: int, produit_id: int, quantite: int, db: Session = Depends(get_db)):
    return log_services.creer_demande_approvisionnement(magasin_id, produit_id, quantite)

@router.post("/demandes/{demande_id}/valider")
def valider_demande(demande_id: int, db: Session = Depends(get_db)):
    return log_services.valider_demande(db, demande_id)
