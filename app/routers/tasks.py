from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from db import get_session
from schemas.users import UserSchema
from models.users import User
from models.companies import Result
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

task_router = APIRouter()


@task_router.get('/tasks/revise', response_model=list[UserSchema])
async def revise(session: AsyncSession = Depends(get_session)) -> list[UserSchema]:
    week_ago = datetime.today() - timedelta(days=7)
    results = await session.execute(select(Result).filter(Result.created_at <= week_ago).distinct(Result.user_id))
    users = []
    for result in results:
        #  await send_sms(result.user_id, 'Retake tests!')
        user = await session.get(User, result.user_id)
        user_schema = UserSchema(id=user.id, username=user.username, email=user.email, description=user.description)
        users.append(user_schema)
    return users
