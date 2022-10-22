from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from models.companies import Company, Member, Request
from schemas.companies import CompanyCreateSchema, CompanySchema, CompanyAlterSchema, RequestSchema
from sqlalchemy.future import select
from fastapi import HTTPException, Depends
from models.users import User
from services.users import get_user
from db import get_session
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.orm import selectinload


class CompanyCRUD:
    def __init__(self, session: AsyncSession | None = None, company: Company | None = None):
        if not session:
            self.session = async_object_session(company)
        else:
            self.session = session
        self.company = company

    async def create_company(self, company: CompanyCreateSchema, user: User) -> CompanySchema:
        db_company = await self.session.execute(select(Company).filter(Company.name == company.name))
        db_company = db_company.scalars().first()
        if db_company:
            raise HTTPException(404, 'name already in use')
        else:
            new_company = Company(name=company.name, owner_id=user.id, description=company.description, visible=company.visible)
            self.session.add(new_company)
            await self.session.commit()
            return CompanySchema(id=new_company.id, name=new_company.name, owner=user.username, description=new_company.description, visible=new_company.visible)

    async def patch_company(self, company: CompanyAlterSchema, user: User) -> CompanySchema:
        if self.company.owner_id == user.id:
            if company.name:
                self.company.name = company.name
            if company.description:
                self.company.description = company.description
            if company.visible:
                self.company.visible = company.visible
            await self.session.commit()
            return CompanySchema(id=self.company.id, name=self.company.name, owner=user.username, description=self.company.description, visible=self.company.visible)
        else:
            raise HTTPException(404, 'no access')

    async def delete_company(self, user: User) -> CompanySchema:
        if self.company.owner_id == user.id:
            await self.session.delete(self.company)
            await self.session.commit()
            return CompanySchema(id=self.company.id, name=self.company.name, owner=user.username, description=self.company.description, visible=self.company.visible)
        else:
            raise HTTPException(404, 'no access')

    async def get_companies(self, page: int) -> list[CompanySchema]:
        params = Params(page=page, size=10)
        companies = await paginate(self.session, select(Company).options(selectinload(Company.owner)).filter(Company.visible == True), params=params)
        return [CompanySchema(id=company.id, name=company.name, owner=company.owner.username, description=company.description, visible=company.visible) for company in companies.items]

    async def get_company(self, id: int, user: User) -> CompanySchema:
        company = await self.session.get(Company, id)
        if company:
            if company.visible:
                return CompanySchema(id=company.id, name=company.name, owner=user.username, description=company.description, visible=company.visible)
            else:
                if company.owner_id == user.id:
                    return CompanySchema(id=company.id, name=company.name, owner=user.username, description=company.description, visible=company.visible)
                else:
                    raise HTTPException(404, 'company hidden')
        else:
            raise HTTPException(404, 'company not found')


async def get_company(id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> Company:
    company = await session.get(Company, id)
    if company:
        if company.visible:
            return company
        else:
            if company.owner_id == user.id:
                return company
            else:
                raise HTTPException(404, 'company hidden')
    else:
        raise HTTPException(404, 'company not found')


class RequestCRUD:
    def __init__(self, session: AsyncSession | None = None, user: User | None = None, company: Company | None = None) -> None:
        self.user = user
        self.company = company
        if user:
            self.session = async_object_session(user)
        elif company:
            self.session = async_object_session(company)
        else:
            self.session = session

    async def create_request(self, user_id: int, company_id: int, side: bool):
        db_member = await self.session.get(Member, (company_id, user_id))
        if db_member:
            raise HTTPException(404, 'already member of company')
        db_request = await self.session.execute(select(Request).filter(Request.company_id == company_id, Request.user_id == user_id))
        db_request = db_request.scalars().first()
        if db_request:
            raise HTTPException(404, 'request already submitted')

        user = await self.session.get(User, user_id)
        if not user:
            raise HTTPException(404, 'user not found')

        company = await self.session.get(Company, company_id)
        if not company:
            raise HTTPException(404, 'company not found')

        request = Request(user_id=user_id, company_id=company_id, side=side)
        self.session.add(request)
        await self.session.commit()
        if request.side:
            side = 'User requests access to company'
        else:
            side = 'Company invites user'
        return RequestSchema(user=user.username, company=company.name, side=side)
