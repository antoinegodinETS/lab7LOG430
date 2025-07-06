from pydantic import BaseModel
from typing import Optional

class ProduitBase(BaseModel):
    nom: str
    prix: float
    description: Optional[str]

class ProduitUpdate(BaseModel):
    nom: Optional[str]
    prix: Optional[float]
    description: Optional[str]

class ProduitOut(ProduitBase):
    id: int

    class Config:
        orm_mode = True
