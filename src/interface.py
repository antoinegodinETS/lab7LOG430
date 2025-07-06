from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import joinedload
import httpx
from prometheus_fastapi_instrumentator import Instrumentator


from magasin.models import Produit
from logistique.models import DemandeApprovisionnement
from common.database import SessionLocal

app = FastAPI()
instrumentator = Instrumentator().instrument(app).expose(app)
templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

API_BASE = "http://localhost:8003/api/v1"

@app.get("/produits")
def get_produits():
    db = SessionLocal()
    produits = db.query(Produit).all()
    db.close()
    return {"produits": [{"id": p.id, "nom": p.nom, "prix": p.prix} for p in produits]}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    db = SessionLocal()
    demandes = db.query(DemandeApprovisionnement).options(
        joinedload(DemandeApprovisionnement.magasin),
        joinedload(DemandeApprovisionnement.produit)
    ).filter_by(statut="en_attente").all()
    db.close()

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/logistique/stock")
        stock = resp.json()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "stock": stock,
        "demandes": demandes,
        "result": None
    })

@app.get("/rapport", response_class=HTMLResponse)
async def afficher_rapport(request: Request):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/maison-mere/rapport")
        data = resp.json()
    return templates.TemplateResponse("rapport.html", {"request": request, "data": data})

@app.get("/performances", response_class=HTMLResponse)
async def afficher_performances(request: Request):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/maison-mere/performances")
        data = resp.json()
    return templates.TemplateResponse("performances.html", {"request": request, "result": data})

@app.get("/maj_produit", response_class=HTMLResponse)
def afficher_formulaire_maj(request: Request):
    db = SessionLocal()
    produits = db.query(Produit).all()
    db.close()
    return templates.TemplateResponse("maj_produit.html", {"request": request, "produits": produits})

@app.post("/maj_produit", response_class=HTMLResponse)
def mettre_a_jour_produit(request: Request, produit_id: int = Form(...), nom: str = Form(...), prix: float = Form(...), description: str = Form(...)):
    db = SessionLocal()
    produit = db.query(Produit).filter_by(id=produit_id).first()
    if produit:
        produit.nom = nom
        produit.prix = prix
        produit.description = description
        db.commit()

    produits = db.query(Produit).all()
    db.close()
    return templates.TemplateResponse("maj_produit.html", {
        "request": request,
        "message": "Produit mis à jour avec succès.",
        "produits": produits
    })

@app.get("/demande_appro", response_class=HTMLResponse)
def afficher_demandes(request: Request):
    db = SessionLocal()
    demandes = db.query(DemandeApprovisionnement).filter_by(statut="en_attente").all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "demandes": demandes})

@app.post("/valider_demande", response_class=HTMLResponse)
async def valider_demande(request: Request, demande_id: int = Form(...)):
    db = SessionLocal()
    
    # Charger les relations pour la demande validée
    demande = db.query(DemandeApprovisionnement)\
        .options(joinedload(DemandeApprovisionnement.magasin),
                 joinedload(DemandeApprovisionnement.produit))\
        .filter(DemandeApprovisionnement.id == demande_id)\
        .first()

    if demande:
        async with httpx.AsyncClient() as client:
            await client.post(f"{API_BASE}/logistique/approvisionner", params={
                "produit_id": demande.produit_id,
                "quantite": demande.quantite,
                "magasin_id": demande.magasin_id
            })
        demande.statut = "validee"
        db.commit()

    # Charger TOUTES les demandes avec les relations (important !)
    demandes = db.query(DemandeApprovisionnement)\
        .filter_by(statut="en_attente")\
        .options(joinedload(DemandeApprovisionnement.magasin),
                 joinedload(DemandeApprovisionnement.produit))\
        .all()

    # Récupérer le stock avant de fermer la session
    async with httpx.AsyncClient() as client:
        stock = (await client.get(f"{API_BASE}/logistique/stock")).json()

    db.close()  # ✅ fermer la session après que tout est chargé

    return templates.TemplateResponse("index.html", {
        "request": request,
        "stock": stock,
        "demandes": demandes,
        "result": "Demande validée avec succès."
    })


@app.post("/execute", response_class=HTMLResponse)
async def execute_action(request: Request):
    db = SessionLocal()
    form_data = await request.form()
    action = form_data.get("action")
    section = form_data.get("section", None)
    demandes = db.query(DemandeApprovisionnement).filter_by(statut="en_attente").all()
    result = None
    stock_magasin = None

    try:
        async with httpx.AsyncClient(base_url=API_BASE) as client:
            if action == "rapport":
                return RedirectResponse(url="/rapport", status_code=303)

            elif action == "performances":
                resp = await client.get("/maison-mere/performances")
                result = resp.json()

            elif action == "reapprovisionnement":
                await client.post("/logistique/demande", params={
                    "magasin_id": int(form_data.get("magasin_id")),
                    "produit_id": int(form_data.get("produit_id")),
                    "quantite": int(form_data.get("quantite"))
                })
                return RedirectResponse(url="/", status_code=303)

            elif action == "approvisionner":
                resp = await client.post("/logistique/approvisionner", params={
                    "produit_id": int(form_data.get("produit_id")),
                    "quantite": int(form_data.get("quantite")),
                    "magasin_id": int(form_data.get("magasin_id"))
                })
                result = resp.text

            elif action == "consulter_stock_magasin":
                magasin_id = int(form_data.get("magasin_id"))
                resp = await client.get(f"/magasins/{magasin_id}/stock")
                stock_magasin = resp.json()

            elif action == "vendre_produit":
                await client.post("/magasins/vente", params={
                    "magasin_id": int(form_data.get("magasin_id")),
                    "produit_id": int(form_data.get("produit_id")),
                    "quantite": int(form_data.get("quantite"))
                })
                result = "Produit vendu avec succès"

            else:
                result = "Action non reconnue."

    except Exception as e:
        result = f"Erreur : {str(e)}"

    async with httpx.AsyncClient() as client:
        stock = (await client.get(f"{API_BASE}/logistique/stock")).json()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "stock": stock,
        "stock_magasin": stock_magasin,
        "active_section": section,
        "demandes": demandes
    })
