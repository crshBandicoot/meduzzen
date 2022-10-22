from typing import Literal
from pydantic import BaseModel, Field


class CompanyCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=32)
    description: str | None = Field(min_length=1, max_length=4096)
    visible: bool | None

class CompanyAlterSchema(BaseModel):
    name: str | None = Field(min_length=1, max_length=32)
    description: str | None = Field(min_length=1, max_length=4096)
    visible: bool | None


class CompanySchema(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=32)
    owner: str = Field(min_length=1, max_length=32)
    description: str | None = Field(min_length=1, max_length=4096)
    visible: bool


class MemberCreateSchema(BaseModel):
    company_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    admin: bool | None


class MemberSchema(BaseModel):
    id: int = Field(gt=0)
    company: str = Field(min_length=1, max_length=32)
    user: str = Field(min_length=1, max_length=32)
    admin: bool | None


class RequestSchema(BaseModel):
    user: str = Field(min_length=1, max_length=32)
    company: str = Field(min_length=1, max_length=32)
    side: Literal['Company invites user', 'User requests access to company']
