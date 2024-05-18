import datetime
from pydantic import BaseModel
from uuid import UUID

class CreateTodoItem(BaseModel):
    title: str
    description: str
    is_done: bool = False
    is_important: bool = False


class Login(BaseModel):
    username: str
    password: str


class TokenHeader(BaseModel):
    token: UUID

class Token(BaseModel):
    token: UUID
    user_id: int
    creation_time: datetime.datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    registration_time: datetime.datetime