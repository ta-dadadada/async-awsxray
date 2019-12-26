import asyncio
import requests_async
from fastapi import FastAPI
from starlette.responses import JSONResponse
from databases import Database
from src.tracing import recorder, TracingMiddleware

app = FastAPI()
app.add_middleware(TracingMiddleware)

db = Database('mysql://test:test@db:3306/test?charset=utf8mb4')


async def startup_event():
    await db.connect()

async def shutdown_event():
    await db.disconnect()


app.add_event_handler('startup', startup_event)
app.add_event_handler('shutdown', shutdown_event)


async def async_sleep(t: float):
    async with recorder.in_subsegment_async('async_sleep'):
        await asyncio.sleep(t)
    return t


async def _random_sleepers(n: int):
    from random import random
    works = [async_sleep(random()) for _ in range(n)]
    return await asyncio.gather(*works)


async def ok_google():
    async def _ok_google():
        async with recorder.in_subsegment_async('_ok_google'):
            return requests_async.get('https://www.google.com/')
    async with recorder.in_subsegment_async('ok_google'):
        works = [_ok_google() for _ in range(10)]
        return await asyncio.gather(*works)


async def async_query():
    statement = """SELECT * FROM test;"""

    async def _async_query():
        with recorder.in_subsegment_async('_async_query'):
            await db.fetch_all(statement)

    async with recorder.in_subsegment_async('async_query'):
        works = [_async_query() for _ in range(10)]
        return await asyncio.gather(*works)


async def random_sleepers(n: int = 10):
    async with recorder.in_subsegment_async('random_sleep'):
        sleeps = await _random_sleepers(n)
        await asyncio.sleep(0.2)
        return JSONResponse({'sleepers': n, 'sleeps': sleeps})


@app.get('/')
async def sleepy():
    results = await asyncio.gather(random_sleepers(), ok_google(), async_query())
    return results[0]
