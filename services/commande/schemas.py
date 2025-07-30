from typing import Literal
from pydantic import BaseModel

class ProduitCommande(BaseModel):
    id: int
    quantite: int

class CommandeBase(BaseModel):
    client_id: int

class CommandeCreate(CommandeBase):
    produits: list[ProduitCommande]

class CommandeOut(CommandeBase):
    id: int
    statut: str

    class Config:
        orm_mode = True

class EtatPayload(BaseModel):
    etat: Literal["CONFIRMEE", "ANNULEE"]
