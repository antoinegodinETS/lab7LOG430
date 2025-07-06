# stress_test.py
import asyncio
import httpx
import time

API_URL = "http://localhost:8088/produits"
 # interface web (FastAPI)

CONCURRENT_USERS = 100
REQUESTS_PER_USER = 10

async def send_requests(client):
    for _ in range(REQUESTS_PER_USER):
        try:
            await client.get(API_URL)
        except Exception as e:
            print("Erreur:", e)

async def main():
    start = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [send_requests(client) for _ in range(CONCURRENT_USERS)]
        await asyncio.gather(*tasks)
    duration = time.time() - start
    print(f"Test terminé en {duration:.2f} secondes.")

if __name__ == "__main__":
    asyncio.run(main())
