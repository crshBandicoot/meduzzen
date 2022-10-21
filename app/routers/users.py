from schemas.users import *
from models.users import User
from services.users import UserCRUD, get_user, get_or_create_user
from db import get_session
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

user_router = APIRouter()


@user_router.get('/users/validate', response_model=UserSchema)
async def validate(user: UserSchema = Depends(get_or_create_user)) -> UserSchema:
    return user


@user_router.get('/users', response_model=list[UserSchema])
async def users(session: Session = Depends(get_session), page: int = 1) -> list[UserSchema]:
    result = await UserCRUD(session=session).get_users(page)
    return result


@user_router.get('/users/{id}', response_model=UserSchema)
async def user(id: int, session: Session = Depends(get_session)) -> UserSchema:
    user = await UserCRUD(session=session).get_user(id)
    return user


@user_router.post('/users', response_model=UserSchema)
async def add_user(user: UserCreateSchema, session: Session = Depends(get_session)) -> UserSchema:
    user = await UserCRUD(session=session).create_user(user)
    return user


@user_router.post('/users/login', response_model=str)
async def log_user(user: UserLoginSchema, session: Session = Depends(get_session)) -> str:
    token = await UserCRUD(session=session).login_user(user)
    return token


@user_router.patch('/users', response_model=UserSchema)
async def patch_users(user: UserAlterSchema, db_user: User = Depends(get_user), session: Session = Depends(get_session)) -> UserSchema:
    user = await UserCRUD(session=session, user=db_user).patch_user(user)
    return user


@user_router.delete('/users', response_model=UserSchema)
async def delete_users(user: User = Depends(get_user), session: Session = Depends(get_session)) -> UserSchema:
    user = await UserCRUD(session=session, user=user).delete_user()
    return user
