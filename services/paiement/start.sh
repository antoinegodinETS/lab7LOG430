#!/bin/sh

# Lance le consumer Kafka en arrière-plan
python consumer.py &

# Lance le serveur FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000
