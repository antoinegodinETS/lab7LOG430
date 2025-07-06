from pydantic import BaseModel

class ClientCreate(BaseModel):
    nom: str
    email: str

class ClientOut(ClientCreate):
    id: int

    class Config:
        orm_mode = True
