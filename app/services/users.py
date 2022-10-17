from models.users import *
from sqlalchemy.future import select
from sqlalchemy import or_
from fastapi import HTTPException
from models.users import *
from schemas.users import *
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import Session
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Params


class UserCRUD:
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, user: UserCreateSchema) -> User:
        db_user = await self.session.execute(select(User).filter(or_(User.email == user.email, User.user == user.username)))
        db_user = db_user.scalars().first()
        if db_user:
            raise HTTPException(404, 'username or email already in use')
        else:
            new_user = User(user=user.username, email=user.email, password=sha256.hash(user.password1), description=user.description)
            self.session.add(new_user)
            await self.session.commit()
            return new_user

    async def login_user(self, user: UserLoginSchema) -> User:
        db_user = await self.session.execute(select(User).filter_by(email=user.email))
        db_user = db_user.scalars().first()
        sha256.verify(user.password, db_user.password)
        if sha256.verify(user.password, db_user.password):
            return db_user
        raise HTTPException(404, 'user not found')

    async def patch_user(self, user: UserCreateSchema, id: int) -> User:
        upd_user = await self.session.get(User, id)
        db_user = await self.session.execute(select(User).filter(or_(User.email == user.email, User.user == user.username), User.id != id))
        db_user = db_user.scalars().first()
        if db_user:
            raise HTTPException(404, 'username or email already in use')
        if upd_user:
            upd_user.user = user.username
            upd_user.email = user.email
            upd_user.password = sha256.hash(user.password1)
            await self.session.commit()
            return upd_user
        raise HTTPException(404, 'user not found')

    async def get_users(self, page: int) -> list[User]:
        params = Params(page=page, size=10)
        users = await paginate(self.session, select(User), params=params)
        return users.items

    async def get_user(self, id: int) -> User:
        user = await self.session.get(User, id)
        if user:
            return user
        raise HTTPException(404, 'user not found')

    async def delete_user(self, id: int) -> User:
        user = await self.session.get(User, id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return user
        raise HTTPException(404, 'user not found')
