from pydantic import BaseModel, Field


class CompanyCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=32)
    owner_id: int = Field(gt=0)
    description: str | None = Field(min_length=1, max_length=4096)
    visible: bool | None


class MemberCreateSchema(BaseModel):
    company: int = Field(gt=0)
    user: int = Field(gt=0)
    admin: bool | None


class RequestCreateSchema(BaseModel):
    user_id: int = Field(gt=0)
    company_id: int = Field(gt=0)
    side: bool
