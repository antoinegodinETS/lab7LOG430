from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import itertools

app = FastAPI()

# === CONFIGURATION CORS ===
origins = [
    "http://localhost:3000",  # Exemple : frontend local
    "http://localhost:8080",  # Si accès à la gateway via navigateur
    "*"  # ⚠️ À restreindre en production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Autoriser ces origines
    allow_credentials=True,
    allow_methods=["*"],              # Autoriser toutes les méthodes HTTP
    allow_headers=["*"],              # Autoriser tous les headers
)

# === ROUTAGE ===

CLIENTS_URL = "http://clients:8000"
COMMANDE_URL = "http://commande:8000"
PANIER_URLS = itertools.cycle([
    "http://panier1:8000",
    "http://panier2:8000"
])

# --- CLIENTS ---
@app.get("/clients")
async def get_clients():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLIENTS_URL}/clients")
        return Response(content=response.content, status_code=response.status_code, media_type="application/json")

@app.post("/clients")
async def create_client(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CLIENTS_URL}/clients", json=data)
        return Response(content=response.content, status_code=response.status_code, media_type="application/json")

# --- PANIER ---
@app.post("/panier")
async def ajouter_item_panier(request: Request):
    data = await request.json()
    url = next(PANIER_URLS)
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{url}/panier/", json=data)
        return Response(content=response.content, status_code=response.status_code, media_type="application/json")

@app.delete("/panier/{item_id}")
async def supprimer_item_panier(item_id: int):
    url = next(PANIER_URLS)
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{url}/panier/{item_id}")
        return Response(content=response.content, status_code=response.status_code, media_type="application/json")

@app.get("/panier/{client_id}")
async def lire_panier_client(client_id: int):
    url = next(PANIER_URLS)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{url}/panier/{client_id}")
        return Response(content=response.content, status_code=response.status_code, media_type="application/json")

# --- COMMANDE ---
@app.post("/commande")
async def creer_commande(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{COMMANDE_URL}/commande/", json=data)
        return Response(content=response.content, status_code=response.status_code, media_type="application/json")

@app.get("/commande/{commande_id}")
async def lire_commande(commande_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{COMMANDE_URL}/commande/{commande_id}")
        return Response(content=response.content, status_code=response.status_code, media_type="application/json")
