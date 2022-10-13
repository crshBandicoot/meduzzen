from pydantic import BaseModel, Field, EmailStr


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=1, max_length=32)
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)

    class Config:
        orm_mode = True
