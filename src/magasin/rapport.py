from common.database import SessionLocal
from maison_mere.models import Vente

def rapport_ventes():
    session = SessionLocal()
    result = session.query(Vente.produit_id, Vente.quantite).all()
    session.close()
    return result
