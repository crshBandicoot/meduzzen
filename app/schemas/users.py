from pydantic import BaseModel, ValidationError, validator, Field, EmailStr


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=1, max_length=32)
    email: EmailStr
    description: str | None = Field(min_length=1, max_length=4096)
    password1: str = Field(min_length=8, max_length=32)
    password2: str = Field(min_length=8, max_length=32)

    @validator('password2')
    def passwords_match(cls, password2, values):
        if 'password1' in values and password2 != values['password1']:
            raise ValueError('passwords do not match')
        return password2

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)

    class Config:
        orm_mode = True
