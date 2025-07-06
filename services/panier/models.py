from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class PanierItem(Base):
    __tablename__ = "panier_items"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, index=True)
    produit_id = Column(Integer)
    quantite = Column(Integer)
