from logistique.models import DemandeApprovisionnement, StockLogistique
from magasin.models import Produit, StockMagasin
from common.database import SessionLocal

SEUIL_MINIMUM = 20  # ajustable si besoin


def creer_demande_approvisionnement(magasin_id: int, produit_id: int, quantite: int):
    db = SessionLocal()
    demande = DemandeApprovisionnement(
        magasin_id=magasin_id,
        produit_id=produit_id,
        quantite=quantite,
        statut="en_attente"
    )
    db.add(demande)
    db.commit()
    db.close()
    return "Demande envoyée au centre logistique."

def approvisionner_magasin(produit_id, quantite, magasin_id):
    session = SessionLocal()

    # Retirer du stock logistique
    stock_log = session.query(StockLogistique).filter(StockLogistique.produit_id == produit_id).first()
    if not stock_log or stock_log.quantite < quantite:
        session.close()
        return f"Stock logistique insuffisant pour le produit {produit_id}."

    stock_log.quantite -= quantite

    # Ajouter au stock du magasin
    stock_mag = session.query(StockMagasin).filter_by(produit_id=produit_id, magasin_id=magasin_id).first()
    if stock_mag:
        stock_mag.quantite += quantite
    else:
        stock_mag = StockMagasin(produit_id=produit_id, magasin_id=magasin_id, quantite=quantite)
        session.add(stock_mag)

    session.commit()
    session.close()
    return f"{quantite} unités du produit {produit_id} envoyées au magasin {magasin_id}."


def verifier_et_reapprovisionner(magasin_id, produit_id, quantite_demande):
    session = SessionLocal()

    stock_mag = session.query(StockMagasin).filter_by(magasin_id=magasin_id, produit_id=produit_id).first()
    if not stock_mag or stock_mag.quantite < SEUIL_MINIMUM:
        # Vérifier stock logistique
        stock_log = session.query(StockLogistique).filter_by(produit_id=produit_id).first()
        if not stock_log or stock_log.quantite < quantite_demande:
            session.close()
            return f"Stock logistique insuffisant pour répondre à la demande du magasin {magasin_id}."
        
        # Mettre à jour les deux
        if stock_mag:
            stock_mag.quantite += quantite_demande
        else:
            stock_mag = StockMagasin(produit_id=produit_id, magasin_id=magasin_id, quantite=quantite_demande)
            session.add(stock_mag)

        stock_log.quantite -= quantite_demande
        session.commit()
        session.close()
        return f"Réapprovisionnement effectué pour le magasin {magasin_id}."

    session.close()
    return f"Pas besoin de réapprovisionnement : stock suffisant pour le magasin {magasin_id}."

def consulter_stock_logistique():
    session = SessionLocal()
    stock_info = []

    stocks = session.query(StockLogistique).all()
    for stock in stocks:
        produit = session.query(Produit).filter(Produit.id == stock.produit_id).first()
        stock_info.append({
            "produit_id": stock.produit_id,
            "nom": produit.nom if produit else "Inconnu",
            "quantite": stock.quantite
        })
    
    session.close()
    return stock_info



def recuperer_demandes_en_attente():
    db = SessionLocal()
    demandes = db.query(DemandeApprovisionnement).filter_by(statut="en_attente").all()
    for demande in demandes:
        _ = demande.produit.nom  # force lazy-loading pour le template
        _ = demande.magasin.nom
    db.close()
    return demandes
