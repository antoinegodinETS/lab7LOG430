FROM python:3.12-slim

WORKDIR /app

COPY services/commande/. /app
# Copier event_store dans l'image pour permettre l'import
COPY services/event_store /app/services/event_store

# Installation des dépendances
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary prometheus_fastapi_instrumentator kafka-python

# 👇 Ajout du chemin /app au PYTHONPATH pour permettre l'import de 'services'
ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
