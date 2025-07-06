# init_data.py
from sqlalchemy.orm import Session
from common.database import SessionLocal
from magasin.models import Magasin, Produit

from logistique.models import StockLogistique

magasins = [
    {"nom": "Magasin Plateau", "quartier": "Plateau"},
    {"nom": "Magasin Rosemont", "quartier": "Rosemont"},
    {"nom": "Magasin Vieux-Port", "quartier": "Vieux-Port"},
    {"nom": "Magasin Verdun", "quartier": "Verdun"},
    {"nom": "Magasin Saint-Laurent", "quartier": "Saint-Laurent"},
]
produits_data = [
    {"nom": "Lait 1L", "description": "Lait entier 1L", "prix": 2.49},
    {"nom": "Pain tranché", "description": "Pain blanc tranché", "prix": 3.29},
    {"nom": "Oeufs 12", "description": "Boîte de 12 œufs", "prix": 4.99},
    {"nom": "Pâtes 500g", "description": "Pâtes alimentaires 500g", "prix": 1.79},
    {"nom": "Riz 1kg", "description": "Riz basmati 1kg", "prix": 5.49},
]

def init_produits_et_stock():
    db: Session = SessionLocal()
    
    for prod in produits_data:
        produit = Produit(**prod)
        db.add(produit)
        db.flush()  # pour obtenir l'ID généré
        stock = StockLogistique(produit_id=produit.id, quantite=100)
        db.add(stock)
    
    db.commit()
    db.close()
    print("Produits et stock logistique ajoutés avec succès.")

def init_magasins():
    db: Session = SessionLocal()
    for data in magasins:
        magasin = Magasin(**data)
        db.add(magasin)
    db.commit()
    db.close()
    print("5 magasins insérés avec succès.")

if __name__ == "__main__":
    init_magasins(), init_produits_et_stock()
