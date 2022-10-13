from .models import *


async def create_user(session, user):
    new_user = User(user=user.username, email=user.email, password=user.password)
    await session.add(new_user)
    return new_user
