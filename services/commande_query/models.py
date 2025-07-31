from sqlalchemy import Column, Integer, String, JSON
from database import Base

class CommandeRead(Base):
    __tablename__ = "commandes_read"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, index=True)
    statut = Column(String)
    produits = Column(JSON)  # Projection simple
