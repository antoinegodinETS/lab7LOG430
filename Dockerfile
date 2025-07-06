# Utilise une image Python officielle légère
FROM python:3.12-slim

WORKDIR /app

# Installe les dépendances système nécessaires pour psycopg[c]
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Copie les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY src/ src/
COPY .flake8 .flake8  

# Ajoute le chemin source au PYTHONPATH pour que les imports fonctionnent
ENV PYTHONPATH=/app/src

# Expose le port pour FastAPI
EXPOSE 8003  
EXPOSE 8004  

# Par défaut, lance le serveur FastAPI avec Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]
