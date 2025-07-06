from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Commande(Base):
    __tablename__ = "commandes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, index=True)
    statut = Column(String, default="validee")
