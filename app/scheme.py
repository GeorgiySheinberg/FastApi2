from typing import Literal

from pydantic import BaseModel


class OkResponse(BaseModel):
    status: Literal['ok']


class GetAdResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str


class CreateAdRequest(BaseModel):
    title: str
    description: str
    price: float
    author: str


class CreateAdResponse(BaseModel):
    id: int


class UpdateAdRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None


class UpdateAdResponse(CreateAdResponse):
    pass

