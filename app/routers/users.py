from schemas.users import *
from models.users import User
from services.users import UserCRUD
from db import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer

user_router = APIRouter()


@user_router.post('/validate')
async def validate(token: str, session: Session = Depends(get_session)):
    validated = await UserCRUD(session).validate_user(token)
    return validated


@user_router.get('/users', response_model=list[UserSchema])
async def users(session: Session = Depends(get_session), page: int = 1) -> list[User]:
    result = await UserCRUD(session).get_users(page)
    return result


@user_router.get('/users/{id}', response_model=UserSchema)
async def user(id: int, session: Session = Depends(get_session)) -> User:
    user = await UserCRUD(session).get_user(id)
    return user


@user_router.post('/users', response_model=UserSchema)
async def add_user(user: UserCreateSchema, session: Session = Depends(get_session)) -> User:
    user = await UserCRUD(session).create_user(user)
    return user


@user_router.post('/users/login', response_model=str)
async def log_user(user: UserLoginSchema, session: Session = Depends(get_session)) -> str:
    token = await UserCRUD(session).login_user(user)
    return token


@user_router.patch('/users/{id}', response_model=UserSchema)
async def patch_users(id: int, user: UserCreateSchema, session: Session = Depends(get_session)) -> User:
    user = await UserCRUD(session).patch_user(user, id)
    return user


@user_router.delete('/users/{id}', response_model=UserSchema)
async def delete_users(id: int, session: Session = Depends(get_session)) -> User:
    user = await UserCRUD(session).delete_user(id)
    return user
