from sqlalchemy.orm import Session
from common.database import SessionLocal
from maison_mere.models import Vente
from magasin.models import Produit
import random

def generate_fake_ventes():
    db: Session = SessionLocal()

    produits = db.query(Produit).all()
    if not produits:
        print("Aucun produit trouvé. Exécute d'abord init_data.py.")
        return

    ventes_a_inserer = []

    for magasin_id in range(1, 6):  # Magasins 1 à 5
        for _ in range(10):  # 10 ventes par magasin
            produit = random.choice(produits)
            quantite = random.randint(1, 10)
            montant = quantite * produit.prix

            vente = Vente(
                magasin_id=magasin_id,
                produit_id=produit.id,
                quantite=quantite,
                montant=montant
            )
            ventes_a_inserer.append(vente)

    db.add_all(ventes_a_inserer)
    db.commit()
    db.close()
    print("Données de ventes fictives insérées avec succès.")

if __name__ == "__main__":
    generate_fake_ventes()
