from os import getenv
from jwt import encode, decode
from fastapi import HTTPException


def create_token(data: dict) -> str:
    try:
        return encode(data, getenv('SECRET_KEY'))
    except:
        raise HTTPException(404, 'token creation error')


def get_current_user(token: str) -> dict:
    try:
        return decode(token, getenv('SECRET_KEY'))
    except:
        raise HTTPException(404, 'token validation error')


