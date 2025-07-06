from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common.database import get_db
from maison_mere import services as mm_services
from schemas.rapport_schemas import RapportVentes, ChiffreAffaires, Tendance

router = APIRouter(prefix="/api/v1/maison-mere", tags=["Maison Mère"])

@router.get("/rapport-ventes", response_model=RapportVentes)
def rapport_ventes(db: Session = Depends(get_db)):
    return mm_services.generer_rapport_ventes()

@router.get("/performance")
def performances(db: Session = Depends(get_db)):
    return mm_services.generer_performances()

@router.put("/produits/{produit_id}")
def update_produit(produit_id: int, payload: dict, db: Session = Depends(get_db)):
    success = mm_services.mettre_a_jour_produit(produit_id, payload)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return {"message": "Produit mis à jour avec succès"}
