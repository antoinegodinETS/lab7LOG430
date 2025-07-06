FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary prometheus_fastapi_instrumentator

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
