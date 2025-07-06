# from common.database import init_db


# if __name__ == "__main__":
#     init_db()
#     print("✅ Base de données initialisée avec succès.")

# src/main.py

import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from api import magasin_api, maison_mere_api, logistique_api
from interface import app as interface_app  # 👈 si interface.py contient app = FastAPI()

app = FastAPI(title="API Multi-Magasins - LOG430")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(magasin_api.router)
app.include_router(logistique_api.router)
app.include_router(maison_mere_api.router)

# ✅ Route racine qui affiche toutes les routes
@app.get("/123")
def list_routes():
    return {
        "routes": [
            {"path": route.path, "methods": list(route.methods), "name": route.name}
            for route in app.routes if isinstance(route, APIRoute)
        ]
    }

@app.on_event("startup")
def startup_event():
    # Exécute les scripts Python une fois au démarrage
    try:
        subprocess.run(["python", "init_data.py"], check=True)
        subprocess.run(["python", "populate_vente.py"], check=True)
        print("✅ Scripts exécutés avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur dans l'exécution d'un script : {e}")


