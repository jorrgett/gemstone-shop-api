import datetime
from typing import Optional
from pydantic import validator, EmailStr
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    username: str = Field(index=True)
    password: str = Field(max_length=256, min_length=6)
    email: str
    created_at: datetime.datetime = datetime.datetime.now()
    is_seller: bool = False

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
    username: str = Field(default='desarrollo_inver')
    password: str = Field(default='desarrolloinver1234*')