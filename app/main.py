from sqlalchemy import select
from auth.models import *
from fastapi import FastAPI, Depends
from uvicorn import run as startserver
from auth.db import postgres_engine, redis_engine
from os import getcwd
from config import add_middleware
from auth.schemas import *
from auth.crud import *
from auth.db import get_session
app = FastAPI()
add_middleware(app)


@app.get('/', status_code=200)
async def root():
    return {"status": "Working!", 'postgres': postgres_engine.__str__(), 'redis': redis_engine.__str__()}


@app.get('/users')
async def get_users(session=Depends(get_session)):
    result = await session.execute(select(User))
    return result


@app.post('/users')
async def post_users(user: UserSchema, session=Depends(get_session)):
    create_user(session, user)
    return user


def health_check():
    return 200


app.add_api_route('/health', endpoint=health_check)

if __name__ == '__main__':
    startserver('main:app', host="0.0.0.0", port=8000, reload=True, reload_dirs=[getcwd()])
