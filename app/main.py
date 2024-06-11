from time import time
from fastapi import FastAPI, Request
from redis import asyncio as aioredis

from app.houses.router_house import router as router_houses
from app.rent_payment.router_rent_payment import router as router_rent
from config.config import HOST_REDIS
from app.logger import logger

app = FastAPI()
app.include_router(router_houses)
app.include_router(router_rent)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response


@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url(f"redis://{HOST_REDIS}", encoding="utf8", decode_responses=True)
