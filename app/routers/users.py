from schemas.users import *
from models.users import User
from services.users import UserCRUD, get_user
from db import get_session
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

user_router = APIRouter()


@user_router.get('/users/validate', response_model=UserFullSchema)
async def validate(Token: str = Header(), TokenType: str = Header(), session: Session = Depends(get_session)) -> UserFullSchema:
    user = await UserCRUD(session).get_or_create_user(Token, TokenType)
    return user


@user_router.get('/users', response_model=list[UserSchema])
async def users(session: Session = Depends(get_session), page: int = 1) -> list[UserSchema]:
    result = await UserCRUD(session).get_users(page)
    return result


@user_router.get('/users/{id}', response_model=UserSchema)
async def user(id: int, session: Session = Depends(get_session)) -> UserSchema:
    user = await UserCRUD(session).get_user(id)
    return user


@user_router.post('/users', response_model=UserSchema)
async def add_user(user: UserCreateSchema, session: Session = Depends(get_session)) -> UserSchema:
    user = await UserCRUD(session).create_user(user)
    return user


@user_router.post('/users/login', response_model=str)
async def log_user(user: UserLoginSchema, session: Session = Depends(get_session)) -> str:
    token = await UserCRUD(session).login_user(user)
    return token


@user_router.patch('/users', response_model=UserFullSchema)
async def patch_users(user: UserAlterSchema, session: Session = Depends(get_session), Token: str = Header(), TokenType: str = Header()) -> UserFullSchema:
    user_instance = await get_user(session, Token, TokenType)
    user = await UserCRUD(session, user_instance).patch_user(user)
    return user


@user_router.delete('/users', response_model=UserFullSchema)
async def delete_users(Token: str = Header(), TokenType: str = Header(), session: Session = Depends(get_session)) -> UserFullSchema:
    user_instance = await get_user(session, Token, TokenType)
    user = await UserCRUD(session, user_instance).delete_user()
    return user
