import aiohttp
import asyncio
from os import getenv
user = 'bogdan'
password = 'hashpass'

print(getenv('AUTH0_SECRET'))


async def main():
    async with aiohttp.ClientSession() as session:
        data = {'grant_type': 'client_credentials', 'audience': getenv('AUTH0_AUDIENCE'), 'scope': 'read:sample', 'client_id': getenv('AUTH0_CLIENT'), 'client_secret': getenv('AUTH0_SECRET')}

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        async with session.post(f'https://{getenv("AUTH0_DOMAIN")}/oauth/token', headers=headers, data=data) as resp:
            return await resp.text()


usr = asyncio.run(main())
print(usr)
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImgzeFduUjlNVERDbEQtUjBNTWI0bSJ9.eyJpc3MiOiJodHRwczovL2Rldi04MG9kazY5ci51cy5hdXRoMC5jb20vIiwic3ViIjoiMVBTT2FnbDNNeVo2MFpIUWJkSEZtYnM1bnozZmZWdlVAY2xpZW50cyIsImF1ZCI6InBpemh1a0FwaSIsImlhdCI6MTY2NjA0Nzg0MSwiZXhwIjoxNjY2MTM0MjQxLCJhenAiOiIxUFNPYWdsM015WjYwWkhRYmRIRm1iczVuejNmZlZ2VSIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyJ9.cJD8JZv1x1gltE8I41d_2pOG3RZIGcedPdVR5G6cRMCIDTGgCA21Yi5v3OIPbSyr2xYJnYOcO8ENeg4viTkb8UmmjD2QTC4KcUEvr8hOBEs1tceFdLgIcAjgQFh_WQxbGU0BRjey26wUCDeFgoCy4CXewbFRnPD1A0yAOwHmXavnSOXNdIG_yRIgMIvSnj1wwKBpElsnaWHvuEcnsP4Csg0huy5wNIOxzsLzeL5XpI0a1XUHqOy3WS2Rvwl4i-Vblu3pwIlpYjiactnlLTRXsy-uwz4QE_-XX5hX5sXXmXnLSgBuFz6UpMoX6jUK3WGi1WGsjtCIfYCQ6W6Xi-yXg'


async def func():
    async with aiohttp.ClientSession() as session:
        headers = {'Authorization': 'Bearer {token}'}
        async with session.get(f'https://{getenv("AUTH0_DOMAIN")}/userinfo', headers=headers,) as resp:
            return await resp.text()

usr = asyncio.run(func())
print(usr)
