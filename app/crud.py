from sqlalchemy import select
from sqlalchemy.engine import Result
from models import Session, Advertisement, MODEL, MODEL_CLS, User
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException
import typing


async def add_item(session: Session, item: MODEL):
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as err:
        if err.orig.pgcode == "23505":
            raise HTTPException(status_code=409, detail='item already exists')
        raise err
    return item


async def get_item(session: Session, orm_class: typing.Type[Advertisement], ad_id: int):
    orm_object = await session.get(orm_class, ad_id)
    if orm_object is None:
        raise HTTPException(status_code=404, detail=f"{orm_class.title} is not found")
    return orm_object


async def search_item(session: Session, title: str = None) -> list[Advertisement]:
    query = select(Advertisement).where(Advertisement.title == title)
    orm_object: Result = await session.execute(query)

    ads = orm_object.all()
    if ads is None:
        raise HTTPException(status_code=404, detail=f"{Advertisement.__name__} is not found")
    ads = [ad.dict for ad in ads]
    return ads


async def get_user(session: Session, user_id: int):
    query = select(User).where(User.user_id == user_id)
    orm_object: Result = await session.execute(query)
    user = orm_object.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail=f"{User.__name__} is not found")
    return user
