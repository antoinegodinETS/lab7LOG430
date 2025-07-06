from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from common.database import Base

class Vente(Base):
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True, index=True)
    magasin_id = Column(Integer)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    quantite = Column(Integer)
    montant = Column(Float)

    produit = relationship("Produit", back_populates="ventes")
