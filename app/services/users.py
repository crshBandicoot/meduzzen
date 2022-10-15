from models.users import *
from sqlalchemy.future import select
from sqlalchemy import or_
from fastapi import HTTPException
from models.users import *
from schemas.users import *
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import Session


async def create_user(session: Session, user: UserCreateSchema) -> User:
    db_user = await session.execute(select(User).filter(or_(User.email == user.email, User.user == user.username)))
    db_user = db_user.scalars().first()
    if db_user:
        raise HTTPException(404, 'username or email already in use')
    else:
        new_user = User(user=user.username, email=user.email, password=sha256.hash(user.password1), description=user.description)
        session.add(new_user)
        await session.commit()
        return new_user


async def login_user(session: Session, user: UserLoginSchema) -> User:
    db_user = await session.execute(select(User).filter_by(email=user.email))
    db_user = db_user.scalars().first()
    sha256.verify(user.password, db_user.password)
    if sha256.verify(user.password, db_user.password):
        return db_user
    raise HTTPException(404, 'user not found')


async def patch_user(session: Session, user: UserCreateSchema, id: int) -> User:
    upd_user = await session.get(User, id)
    db_user = await session.execute(select(User).filter(or_(User.email == user.email, User.user == user.username), User.id != id))
    db_user = db_user.scalars().first()
    if db_user:
        raise HTTPException(404, 'username or email already in use')
    if upd_user:
        upd_user.user = user.username
        upd_user.email = user.email
        upd_user.password = sha256.hash(user.password1)
        await session.commit()
        return upd_user
    raise HTTPException(404, 'user not found')


async def get_users(session: Session) -> list[User]:
    users = await session.execute(select(User))
    users = users.scalars().all()
    return users


async def get_user(session: Session, id: int) -> User:
    user = await session.get(User, id)
    if user:
        return user
    raise HTTPException(404, 'user not found')
