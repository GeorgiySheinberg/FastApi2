import uuid

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select

from config import TOKEN_TTL
from models import Session, Token

from typing import Annotated

import datetime


async def get_db_session():
    async with Session() as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_db_session, use_cache=True)]


async def get_token(x_token: Annotated[uuid.UUID, Header()], session: SessionDependency):
    token_query = select(Token).where(Token.token == x_token,
                                      Token.creation_time >= datetime.datetime.now() - datetime.timedelta(
                                          seconds=TOKEN_TTL)
                                      )
    token = await session.scalar(token_query)
    if token:
        return token
    raise HTTPException(status_code=403, detail="Invalid token")


TokenDependency = Annotated[Token, Depends(get_token)]
