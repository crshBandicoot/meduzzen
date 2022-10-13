import json
from .models import *
from sqlalchemy.future import select


async def create_user(session, user):
    new_user = User(user=user.username, email=user.email, password=user.password)
    session.add(new_user)
    try:
        await session.commit()
    except:
        return json.dumps({'error': 'already in db'})
    return new_user


async def login_user(session, user):
    user = await session.execute(select(User).filter_by(email=user.email, password=user.password))
    user = user.scalars().first()
    if user:
        return True
    return False


async def patch_user(session, user, id):
    db_user = await session.get(User, id)
    db_user.user = user.username
    db_user.email = user.email
    db_user.password = user.password
    await session.commit()
    return db_user
