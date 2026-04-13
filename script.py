import asyncio
import aiohttp
import json
import random
import time
import os

BASE_URL = "https://jbzd.com.pl/mikroblog/user/profile/{}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

CONCURRENCY = 2

results_200 = []
results_404 = []

queue = asyncio.Queue()

# -----------------------------
# PODZIAŁ ZAKRESU (20 JOBÓW)
# -----------------------------
TOTAL = 1300000
PARTS = int(os.getenv("PARTS", "1"))
PART = int(os.getenv("PART", "0"))

chunk = TOTAL // PARTS

start = PART * chunk + 1
end = (PART + 1) * chunk

for i in range(start, end):
    queue.put_nowait(i)

# -----------------------------

async def worker(session):
    while True:
        try:
            user_id = queue.get_nowait()
        except asyncio.QueueEmpty:
            break

        try:
            async with session.get(BASE_URL.format(user_id), headers=HEADERS) as r:
                status = r.status

                print(f"ID {user_id} -> {status}")

                if status == 200:
                    results_200.append(user_id)
                elif status == 404:
                    results_404.append(user_id)

        except Exception as e:
            print("Błąd:", user_id, e)

        await asyncio.sleep(random.uniform(0.12, 0.12))
        queue.task_done()


async def main():
    start_time = time.time()

    connector = aiohttp.TCPConnector(limit=CONCURRENCY)

    async with aiohttp.ClientSession(connector=connector) as session:
        workers = [worker(session) for _ in range(CONCURRENCY)]
        await asyncio.gather(*workers)

    # zapis per job (żeby się nie nadpisywało)
    part = PART

    with open(f"200_{part}.json", "w") as f:
        json.dump(results_200, f, indent=2)

    with open(f"404_{part}.json", "w") as f:
        json.dump(results_404, f, indent=2)

    print("200:", len(results_200))
    print("404:", len(results_404))
    print("Czas:", time.time() - start_time)


asyncio.run(main())
