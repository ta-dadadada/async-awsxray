import asyncio
import requests_async
from fastapi import FastAPI
from starlette.responses import JSONResponse
from src.tracing import recorder, TracingMiddleware

app = FastAPI()
app.add_middleware(TracingMiddleware)


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
        works = [_ok_google() for _ in range(4)]
        return await asyncio.gather(*works)


async def random_sleepers(n: int = 10):
    async with recorder.in_subsegment_async('random_sleep'):
        sleeps = await _random_sleepers(n)
        await asyncio.sleep(0.2)
        return JSONResponse({'sleepers': n, 'sleeps': sleeps})


@app.get('/')
async def sleepy():
    results = await asyncio.gather(random_sleepers(), ok_google())
    return results[0]
