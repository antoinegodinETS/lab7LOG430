from pydantic import BaseModel
from typing import List

class VentesParMagasin(BaseModel):
    nom: str
    total_ventes: float

class ProduitVendu(BaseModel):
    nom: str
    quantite_totale: int

class StockRestant(BaseModel):
    magasin: str
    produit: str
    quantite: int

class RapportVentes(BaseModel):
    ventes_par_magasin: List[VentesParMagasin]
    produits_vendus: List[ProduitVendu]
    stock_restants: List[StockRestant]

class ChiffreAffaires(BaseModel):
    magasin_id: int
    total: float

class Tendance(BaseModel):
    magasin_id: int
    nombre_ventes: int
