from pydantic import BaseModel
from typing import Optional

class StockMagasinOut(BaseModel):
    produit_id: int
    nom: str
    quantite: int

class StockLogistiqueOut(BaseModel):
    produit_id: int
    nom: Optional[str]
    quantite: int

    class Config:
        orm_mode = True
