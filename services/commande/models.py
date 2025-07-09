from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from database import Base
from pydantic import BaseModel


class Commande(Base):
    __tablename__ = "commandes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, index=True)
    statut = Column(String, default="validee")


class EtatCommande(str, Enum):
    CREEE = "cree"
    STOCK_VERIFIE = "stock_verifie"
    STOCK_RESERVE = "stock_reserve"
    PAYEE = "payee"
    CONFIRMEE = "confirmee"
    ANNULEE = "annulee"
    
    
class Produit(BaseModel):
    id: str
    qte: int

class CommandeCreate(BaseModel):
    id: int
    client_id: int
    produits: list[Produit]