from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base

class StockLogistique(Base):
    __tablename__ = "stock_logistique"

    id = Column(Integer, primary_key=True, index=True)
    produit_id = Column(Integer)
    quantite = Column(Integer)

    def __repr__(self):
        return f"<StockLogistique(produit_id={self.produit_id}, quantite={self.quantite})>"

class DemandeApprovisionnement(Base):
    __tablename__ = "demandes_approvisionnement"

    id = Column(Integer, primary_key=True, index=True)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    magasin_id = Column(Integer, ForeignKey("magasins.id"))
    quantite = Column(Integer)
    statut = Column(String, default="en_attente")

    produit = relationship("Produit")
    magasin = relationship("Magasin")
