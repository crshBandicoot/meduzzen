from fastapi import APIRouter, Depends, Header, Query
from db import get_session
from schemas.companies import CompanyCreateSchema,  CompanySchema, MemberSchema, RequestSchema, CompanyAlterSchema, QuizCreateSchema, QuizSchema, QuizAlterSchema, QuizAnswerSchema, ResultSchema
from services.users import get_user
from models.users import User
from services.companies import CompanyCRUD, get_company, RequestCRUD, MemberCRUD, QuizCRUD
from models.companies import Company, Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
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


@company_router.get('/companies/invite/{id}', response_model=RequestSchema)
async def invite_user(id: int, user_id: int = Query(), company: Company = Depends(get_company)) -> RequestSchema:
    request = await RequestCRUD(company=company).create_request(user_id=user_id, company_id=company.id, side=False)
    return request


@company_router.get('/request/review/{id}', response_model=MemberSchema)
async def review_request(id: int, response: str = Query(), user: User = Depends(get_user)) -> MemberSchema:
    member = await MemberCRUD(user=user).review_request(request_id=id, response=response)
    return member


@company_router.get('/companies/remove/{id}', response_model=MemberSchema)
async def remove_user(id: int, user_id: int = Query(), company: Company = Depends(get_company), user: User = Depends(get_user)) -> MemberSchema:
    member = await MemberCRUD(company=company).remove_user(user_id=user_id, cur_user=user)
    return member


@company_router.get('/companies/admin/{id}', response_model=MemberSchema)
async def change_admin(id: int, user_id: int = Query(), admin: bool = Query(), company: Company = Depends(get_company), user: User = Depends(get_user)) -> MemberSchema:
    member = await MemberCRUD(company=company).change_admin(user_id=user_id, cur_user=user, admin=admin)
    return member


@company_router.get('/companies/members/{id}')
async def get_members(company: Company = Depends(get_company), user: User = Depends(get_user), page: int = Query(default=1)) -> list[MemberSchema]:
    members = await MemberCRUD(company=company).get_members(cur_user=user, page=page)
    return members


@company_router.get('/companies/join/{id}', response_model=RequestSchema)
async def invite_user(id: int, user: User = Depends(get_user)) -> RequestSchema:
    request = await RequestCRUD(user=user).create_request(user_id=user.id, company_id=id, side=True)
    return request


@company_router.get('/companies/request_list/{id}', response_model=list[RequestSchema])
async def company_requests(company: Company = Depends(get_company), page: int = Query(default=1), user: User = Depends(get_user)) -> list[RequestSchema]:
    requests = await RequestCRUD(company=company).get_requests(company_id=company.id, page=page, cur_user=user)
    return requests


@company_router.get('/request_list', response_model=list[RequestSchema])
async def user_requests(user: User = Depends(get_user), page: int = Query(default=1)) -> list[RequestSchema]:
    requests = await RequestCRUD(user=user).get_requests(user_id=user.id, page=page)
    return requests


@company_router.post('/companies/quiz/{id}', response_model=QuizSchema)
async def add_quiz(quiz: QuizCreateSchema, company: Company = Depends(get_company), user: User = Depends(get_user), session: AsyncSession = Depends(get_session)) -> QuizSchema:
    quiz = await QuizCRUD(session=session).create_quiz(company=company, user=user, quiz=quiz)
    return quiz


@company_router.patch('/companies/quiz/{id}', response_model=QuizSchema)
async def patch_quiz(quiz: QuizAlterSchema, quiz_id: int = Query(), company: Company = Depends(get_company), user: User = Depends(get_user), session: AsyncSession = Depends(get_session)) -> QuizSchema:
    quiz = await QuizCRUD(session=session).patch_quiz(company=company, user=user, quiz=quiz, quiz_id=quiz_id)
    return quiz


@company_router.delete('/companies/quiz/{id}', response_model=QuizSchema)
async def delete_quiz(quiz_id: int = Query(), company: Company = Depends(get_company), user: User = Depends(get_user), session: AsyncSession = Depends(get_session)) -> QuizSchema:
    quiz = await QuizCRUD(session=session).delete_quiz(company=company, user=user, quiz_id=quiz_id)
    return quiz


@company_router.get('/companies/quiz_list/{id}', response_model=list[QuizSchema])
async def guizzes(session: AsyncSession = Depends(get_session), company: Company = Depends(get_company), user: User = Depends(get_user), page: int = Query(default=1)) -> list[QuizSchema]:
    quizzes = await QuizCRUD(session=session).quizzes(company=company, user=user, page=page)
    return quizzes


@company_router.post('/companies/take_quiz/{id}', response_model=ResultSchema)
async def guizzes(answers: QuizAnswerSchema, quiz_id: int = Query(), session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> ResultSchema:
    result = await QuizCRUD(session=session).take_quiz(answers=answers, user=user, quiz_id=quiz_id)
    return result


@company_router.get('/users/dump_results/', response_class=StreamingResponse)
async def dump_results_user(session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> StreamingResponse:
    results = await QuizCRUD(session=session).dump_results_user(user_id=user.id)
    return StreamingResponse(results, media_type='text/csv')


@company_router.get('/get')
async def get(session: AsyncSession = Depends(get_session)):
    results = await session.execute(select(Result))
    return results.scalars().all()
