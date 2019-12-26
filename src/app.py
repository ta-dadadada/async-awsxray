import asyncio
from fastapi import FastAPI
from starlette.responses import JSONResponse


app = FastAPI()


async def async_sleep(t: float, name: str):
    await asyncio.sleep(t)
    print(f'{name} sleep {t}s')
    return t


async def _random_sleepers(n: int):
    from random import random
    works = [async_sleep(random(), str(i)) for i in range(n)]
    return await asyncio.gather(*works)


async def random_sleepers(n: int = 10):
    sleeps = await _random_sleepers(n)
    return JSONResponse({'sleepers': n, 'sleeps': sleeps})


@app.get('/')
async def sleepy():
    await random_sleepers()
