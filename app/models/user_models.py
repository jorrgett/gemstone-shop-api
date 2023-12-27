import datetime
from typing import Optional
from pydantic import BaseModel, validator, EmailStr
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    username: str = Field(index=True)
    password: str = Field(max_length=256, min_length=6)
    email: str
    created_at: datetime.datetime = datetime.datetime.now()
    is_seller: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "Id": 150,
                "username": "JohnDoe23x",
                "password": "desarrolloinver1234",
                "email": "johndoe23x@example.com",
                "created_at": "2023-12-22T15:11:59.849342",
                "is_seller": True,
            }
        }

class UserInput(SQLModel):
    username: str = Field(default='user_example')
    password: str = Field(max_length=256, min_length=6, default='password1234*')
    password2: str = Field(default='password1234*')
    email: str = Field(default='example@example.com')
    is_seller: bool = False

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')
        return v

class UserLogin(SQLModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "maxcodex",
                "password": "inver1234*"
            }
        }

class AuthSchema(BaseModel):
    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "CI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVjE1NDE2NDE2MiIsImV4cGlyZXMiOjE2NzE1MjUxNDYuOTU2NTAyMn0",
                "token_type": "Bearer"
            }
        }

class LoginInResponse(BaseModel):
    auth_credentials: AuthSchema
    auth_info: UserLogin
    user: User