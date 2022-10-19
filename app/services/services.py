from os import getenv
from jwt import encode
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from models.users import User


def create_token(data: dict) -> str:
    try:
        return encode(data, getenv('SECRET_KEY'), algorithm='HS256')
    except:
        raise HTTPException(404, 'token creation error')
