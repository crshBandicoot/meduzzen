from fastapi import APIRouter, Depends, Header, Query
from db import get_session
from schemas.users import UserSchema
from schemas.companies import CompanyCreateSchema, MemberCreateSchema,  CompanySchema, MemberSchema, RequestSchema, CompanyAlterSchema
from services.users import get_user
from models.users import User
from services.companies import CompanyCRUD, get_company, RequestCRUD
from models.companies import Company, Request
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


@company_router.get('/companies', response_model=list[CompanySchema])
async def companies(session: AsyncSession = Depends(get_session), page: int = Query(default=1)) -> list[CompanySchema]:
    company = await CompanyCRUD(session=session).get_companies(page)
    return company


@company_router.patch('/companies/{id}')
async def patch_company(company: CompanyAlterSchema, id: int, db_company: Company = Depends(get_company), user: User = Depends(get_user)) -> CompanySchema:
    company = await CompanyCRUD(company=db_company).patch_company(company=company, user=user)
    return company


@company_router.delete('/companies/{id}')
async def delete_company(id: int, db_company: Company = Depends(get_company), user: User = Depends(get_user)) -> CompanySchema:
    company = await CompanyCRUD(company=db_company).delete_company(user=user)
    return company


@company_router.get('/companies/{id}/invite', response_model=RequestSchema)
async def invite_user(id: int, user_id: int = Query(), company: Company = Depends(get_company)) -> RequestSchema:
    request = await RequestCRUD(company=company).create_request(user_id=user_id, company_id=company.id, side=False)
    return request


# @company_router.get('/companies/{id}/requests', response_model=MemberSchema)
# async def review_request(id: int, request: int = Query(), response: str = Query(), company: Company = Depends(get_company)) -> MemberSchema:
#     member = await MemberCRUD(company=company).create_member(request_id=request, response=response)
#     return member


# @company_router.get('/users/{id}/requests', response_model=MemberSchema)
# async def review_request(id: int, request: int = Query(), response: str = Query(), user: User = Depends(get_user)) -> MemberSchema:
#     member = await MemberCRUD(user=user).create_member(request_id=request, response=response)
#     return member


# @company_router.get('/companies/{id}/remove', response_model=UserSchema)
# async def remove_user(id: int, user_id: int = Query(), company: Company = Depends(get_company)) -> RequestSchema:
#     request = await RequestCRUD(company=company).remove_request(user_id=user_id, company_id=company.id)
#     return request


@company_router.get('/companies/{id}/join', response_model=RequestSchema)
async def invite_user(id: int, user: User = Depends(get_user)) -> RequestSchema:
    request = await RequestCRUD(user=user).create_request(user_id=user.id, company_id=id, side=True)
    return request
