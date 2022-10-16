from schemas.users import *
from services.users import *
from db import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

user_router = APIRouter()


@user_router.get('/users')
async def users(session: Session = Depends(get_session), page: int = 1):
    result = await get_users(session, page)
    return result


@user_router.get('/users/{id}')
async def user(id: int, session: Session = Depends(get_session)):
    result = await get_user(session, id)
    return result


@user_router.post('/users')
async def post_users(user: UserCreateSchema, session: Session = Depends(get_session)):
    user = await create_user(session, user)
    return user


@user_router.post('/users/login')
async def post_users(user: UserLoginSchema, session: Session = Depends(get_session)):
    user = await login_user(session, user)
    return user


@user_router.patch('/users/{id}')
async def patch_users(id: int, user: UserCreateSchema, session: Session = Depends(get_session)):
    user = await patch_user(session, user, id)
    return user


@user_router.delete('/users/{id}')
async def delete_users(id: int, session: Session = Depends(get_session)):
    user = await delete_user(session, id)
    return user
