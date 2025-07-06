from pydantic import BaseModel

class CommandeBase(BaseModel):
    client_id: int

class CommandeCreate(CommandeBase):
    pass

class CommandeOut(CommandeBase):
    id: int
    statut: str

    class Config:
        orm_mode = True
