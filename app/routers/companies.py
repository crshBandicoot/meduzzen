from fastapi import APIRouter, Depends, Header
from db import get_session
from schemas.companies import CompanyCreateSchema, MemberCreateSchema, RequestCreateSchema, CompanySchema, MemberSchema, RequestSchema, CompanyAlterSchema
from services.users import get_user
from models.users import User
from services.companies import CompanyCRUD, get_company
from models.companies import Company
from sqlalchemy.ext.asyncio import async_object_session, AsyncSession
from sqlalchemy.future import select
company_router = APIRouter()


@company_router.post('/companies', response_model=CompanySchema)
async def add_company(company: CompanyCreateSchema, session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> CompanySchema:
    company = await CompanyCRUD(session=session).create_company(company=company, user=user)
    return company


@company_router.get('/companies/{id}', response_model=CompanySchema)
async def company(id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> CompanySchema:
    company = await CompanyCRUD(session=session).get_company(id=id, user=user)
    return company


@company_router.patch('/companies/{id}')
async def patch_company(company: CompanyAlterSchema, id: int, db_company: Company = Depends(get_company), user: User = Depends(get_user)) -> CompanySchema:
    company = await CompanyCRUD(company=db_company).patch_company(company=company, user=user)
    return company


@company_router.delete('/companies/{id}')
async def delete_company(id: int, db_company: Company = Depends(get_company), user: User = Depends(get_user)) -> CompanySchema:
    company = await CompanyCRUD(company=db_company).delete_company(user=user)
    return company
