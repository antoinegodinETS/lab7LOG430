from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from common.database import Base
from maison_mere.models import Vente

class Magasin(Base):
    __tablename__ = "magasins"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    quartier = Column(String, nullable=True)

    def __repr__(self):
        return f"<Magasin(nom={self.nom}, quartier={self.quartier})>"
    
class StockMagasin(Base):
    __tablename__ = "stock_magasin"

    id = Column(Integer, primary_key=True, index=True)
    magasin_id = Column(Integer, ForeignKey("magasins.id"))
    produit_id = Column(Integer)
    quantite = Column(Integer)
    
    
class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prix = Column(Float)
    description = Column(String)

    ventes = relationship(Vente, back_populates="produit")
