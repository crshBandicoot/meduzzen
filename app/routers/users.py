import email
from schemas.users import *
from models.users import User
from services.users import UserCRUD
from db import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer

user_router = APIRouter()
token_auth_scheme = HTTPBearer()


# @user_router.get('/users/login_auth0')
# async def login_auth0(token: str = Depends(token_auth_scheme)) -> str:


@user_router.get('/users')
async def users(session: Session = Depends(get_session), page: int = 1) -> list[User]:
    result = await UserCRUD(session).get_users(page)
    return result


@user_router.get('/users/{id}')
async def user(id: int, session: Session = Depends(get_session)) -> User:
    user = await UserCRUD(session).get_user(id)
    return user


@user_router.post('/users')
async def new_user(user: UserCreateSchema, session: Session = Depends(get_session)) -> User:
    user = await UserCRUD(session).create_user(user)
    return user


@user_router.post('/users/login')
async def log_in_user(user: UserLoginSchema, session: Session = Depends(get_session)) -> User:
    user = await UserCRUD(session).login_user(user)
    return user


@user_router.patch('/users/{id}')
async def patch_users(id: int, user: UserCreateSchema, session: Session = Depends(get_session)) -> User:
    user = await UserCRUD(session).patch_user(user, id)
    return user


@user_router.delete('/users/{id}')
async def delete_users(id: int, session: Session = Depends(get_session)) -> User:
    user = await UserCRUD(session).delete_user(id)
    return user
