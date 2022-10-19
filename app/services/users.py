from services.services import create_token
from models.users import *
from sqlalchemy.future import select
from sqlalchemy import or_
from fastapi import HTTPException
from schemas.users import *
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import Session
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Params
from jwt import PyJWKClient, decode
from os import getenv


class UserCRUD:
    def __init__(self, session: Session, user: User | None = None):
        self.session = session
        self.user = user

    async def create_user(self, user: UserCreateSchema) -> UserSchema:
        db_user = await self.session.execute(select(User).filter(or_(User.email == user.email, User.username == user.username)))
        db_user = db_user.scalars().first()
        if db_user:
            raise HTTPException(404, 'username or email already in use')
        else:
            new_user = User(username=user.username, email=user.email, password=sha256.hash(user.password1), description=user.description)
            self.session.add(new_user)
            await self.session.commit()
            return UserSchema(id=new_user.id, username=new_user.username, description=new_user.description)

    async def login_user(self, user: UserLoginSchema) -> str:
        db_user = await self.session.execute(select(User).filter_by(email=user.email))
        db_user = db_user.scalars().first()
        if sha256.verify(user.password, db_user.password):
            return create_token({'email': user.email, 'password': user.password})
        raise HTTPException(404, 'user not found')

    async def patch_user(self, user: UserAlterSchema) -> UserFullSchema:
        if user.username:
            self.user.username = user.username
        if user.description:
            self.user.description = user.description
        if user.password:
            self.user.password = sha256.hash(user.password)
        await self.session.commit()
        return UserFullSchema(id=self.user.id, username=self.user.username, email=self.user.email, description=self.user.description, password=self.user.password)

    async def get_users(self, page: int) -> list[UserSchema]:
        params = Params(page=page, size=10)
        users = await paginate(self.session, select(User), params=params)
        return [UserSchema(id=user.id, username=user.username, description=user.description) for user in users.items]

    async def get_user(self, id: int) -> UserSchema:
        user = await self.session.get(User, id)
        if user:
            return UserSchema(id=user.id, username=user.username, description=user.description)
        raise HTTPException(404, 'user not found')

    async def delete_user(self) -> UserSchema:
        return_user = UserFullSchema(id=self.user.id, username=self.user.username, email=self.user.email, description=self.user.description, password=self.user.password)
        await self.session.delete(self.user)
        await self.session.commit()
        return return_user

    async def get_or_create_user(self, Token: str, TokenType: str) -> User:
        if TokenType == 'app':
            try:
                data = decode(Token, getenv('SECRET_KEY'), ['HS256'])
                email = data['email']
                password = data['password']
                user = await self.session.execute(select(User).filter(User.email == email))
                user = user.scalars().first()
                if user:
                    if sha256.verify(password, user.password):
                        return UserFullSchema(id=user.id, username=user.username, email=user.email, description=user.description, password=user.password)
                else:
                    raise Exception
            except:
                raise HTTPException(404, 'token validation error')
        elif TokenType == 'auth0':
            try:
                jwks_client = PyJWKClient(getenv('AUTH0_PUBLIC_URL'))
                signing_key = jwks_client.get_signing_key_from_jwt(Token)
                data = decode(
                    Token,
                    signing_key.key,
                    algorithms=["RS256"],
                    audience=getenv('AUTH0_AUDIENCE')
                )
                email = data['user_email']
                user = await self.session.execute(select(User).filter(User.email == email))
                user = user.scalars().first()
                if user:
                    return UserFullSchema(id=user.id, username=user.username, email=user.email, description=user.description, password=user.password)
                else:
                    new_user = User(username=email, email=email, password=sha256.hash(getenv('SECRET_KEY')))
                    self.session.add(new_user)
                    await self.session.commit()
                    return UserFullSchema(id=new_user.id, username=new_user.username, email=new_user.email, description=new_user.description, password=new_user.password)
            except:
                raise HTTPException(404, 'token validation error')


async def get_user(session: Session, Token: str, TokenType: str) -> User:
    if TokenType == 'app':
        try:
            data = decode(Token, getenv('SECRET_KEY'), ['HS256'])
            email = data['email']
            password = data['password']
            user = await session.execute(select(User).filter(User.email == email))
            user = user.scalars().first()
            if user:
                if sha256.verify(password, user.password):
                    return user
                raise Exception
        except:
            raise HTTPException(404, 'token validation error')
    elif TokenType == 'auth0':
        try:
            jwks_client = PyJWKClient(getenv('AUTH0_PUBLIC_URL'))
            signing_key = jwks_client.get_signing_key_from_jwt(Token)
            data = decode(
                Token,
                signing_key.key,
                algorithms=["RS256"],
                audience=getenv('AUTH0_AUDIENCE')
            )
            email = data['user_email']
            user = await session.execute(select(User).filter(User.email == email))
            user = user.scalars().first()
            if user:
                return user
            else:
                raise Exception
        except:
            raise HTTPException(404, 'token validation error')
