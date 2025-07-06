from pydantic import BaseModel

class PanierItemBase(BaseModel):
    client_id: int
    produit_id: int
    quantite: int

class PanierItemCreate(PanierItemBase):
    pass

class PanierItemOut(PanierItemBase):
    id: int

    class Config:
        orm_mode = True
