from typing import Literal
from pydantic import BaseModel, Field, validator


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


class MemberSchema(BaseModel):
    company: str = Field(min_length=1, max_length=32)
    user: str = Field(min_length=1, max_length=32)
    admin: bool | None


class RequestSchema(BaseModel):
    id: int = Field(gt=0)
    user: str = Field(min_length=1, max_length=32)
    company: str = Field(min_length=1, max_length=32)
    side: Literal['Company invites user', 'User requests access to company']


class QuizCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=32)
    description: str | None = Field(min_length=1, max_length=4096)
    frequency: int = Field(gt=0)
    questions: list[str] = Field(min_length=1, max_length=16384)
    answer_options: list[list[str]] = Field(min_length=1, max_length=65536)
    correct_answers: list[int]

    @validator('correct_answers')
    def validate_quiz(cls, value, values):
        if len(values['questions']) < 2:
            raise ValueError('Invalid quiz!')
        for option in values['answer_options']:
            if len(option) < 2:
                raise ValueError('Invalid quiz!')
        if len(value) != len(values['questions']) != len(values['answer_options']):
            raise ValueError('Invalid quiz!')
        for options, answer in zip(values['answer_options'], value):
            if answer > len(options):
                raise ValueError('Invalid quiz!')
        return value


class QuizAlterSchema(BaseModel):
    name: str | None = Field(min_length=1, max_length=32)
    description: str | None = Field(min_length=1, max_length=4096)
    frequency: int | None = Field(gt=0)
    questions: list[str] | None = Field(min_length=1, max_length=16384)
    answer_options: list[list[str]] | None = Field(min_length=1, max_length=65536)
    correct_answers: list[int] | None

    @validator('correct_answers')
    def validate_quiz(cls, value, values):
        if not value or not values['questions'] or not values['answer_options']:
            if value != values['questions'] != values['answer_options'] != None:
                raise ValueError('Invalid quiz!')
        if len(values['questions']) < 2:
            raise ValueError('Invalid quiz!')
        for option in values['answer_options']:
            if len(option) < 2:
                raise ValueError('Invalid quiz!')
        if len(value) != len(values['questions']) != len(values['answer_options']):
            raise ValueError('Invalid quiz!')
        for options, answer in zip(values['answer_options'], value):
            if answer > len(options):
                raise ValueError('Invalid quiz!')
        return value


class QuizSchema(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=32)
    description: str | None = Field(min_length=1, max_length=4096)
    frequency: int = Field(gt=0)
    quiz: dict


class QuizAnswerSchema(BaseModel):
    answers: list[int]


class ResultSchema(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    quiz_id: int = Field(gt=0)
    overall_questions: int = Field(gt=0)
    correct_questions: int = Field(ge=0)
