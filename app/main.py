from os import getcwd
from sqlalchemy.future import select
from auth.models import *
from fastapi import FastAPI, Depends
from uvicorn import run as startserver
from db import postgres_engine, redis_engine, get_session, init_models
from config import add_middleware
from auth.schemas import *
from auth.crud import *
app = FastAPI()
add_middleware(app)


@app.get('/', status_code=200)
async def root():
    return {"status": "Working!", 'postgres': postgres_engine.__str__(), 'redis': redis_engine.__str__()}


@app.get('/users')
async def get_users(session=Depends(get_session)):
    result = await session.execute(select(User))
    return result.scalars().all()


@app.get('/users/{id}')
async def get_user(id: int, session=Depends(get_session)):
    result = await session.get(User, id)
    return result


@app.post('/users')
async def post_users(user: UserCreateSchema, session=Depends(get_session)):
    user = await create_user(session, user)
    return user


@app.post('/users/login')
async def post_users(user: UserLoginSchema, session=Depends(get_session)):
    user = await login_user(session, user)
    return user


@app.patch('/users/{id}')
async def patch_users(id: int, user: UserCreateSchema, session=Depends(get_session)):
    user = await patch_user(session, user, id)
    return user


def health_check():
    return 200


app.add_api_route('/health', endpoint=health_check)

if __name__ == '__main__':
    startserver('main:app', host="0.0.0.0", port=8000, reload=True, reload_dirs=[getcwd()])
