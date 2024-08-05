import uuid
from typing import Literal

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    login: str


class OkResponse(BaseModel):
    status: Literal['ok']


class GetAdResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    user: User


class CreateAdRequest(BaseModel):
    title: str
    description: str
    price: float


class CreateAdResponse(BaseModel):
    id: int


class UpdateAdRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    user: str | None = None


class UpdateAdResponse(CreateAdResponse):
    pass


class LoginRequest(BaseModel):
    login: str
    password: str


class LoginResponse(BaseModel):
    token: uuid.UUID


class IdResponse(BaseModel):
    user_id: int


class CreateUserResponse(IdResponse):
    pass


class CreateUserRequest(BaseModel):
    login: str
    password: str


class GetUserRequest(BaseModel):
    user_id: int


class GetUserResponse(BaseModel):
    user_id: int
    login: str


class UpgradeUserRequest(BaseModel):
    login: str | None = None
    password: str | None = None


class UpgradeUserResponse(BaseModel):
    user_id: int
    login: str


class DeleteUserRequest(BaseModel):
    user_id: int
