import fastapi
import auth
from typing import Annotated

from sqlalchemy import select

import crud
from lifespan import lifespan
from models import Advertisement, User, Token
import scheme

from dependencies import SessionDependency, TokenDependency

from crud import add_item, get_item, search_item

app = fastapi.FastAPI(
    title="purchase API",
    version='1.0',
    description="API for purchase and sell",
    lifespan=lifespan
)

TokenHeader = Annotated[str, fastapi.Header()]


@app.get("/v1/advertisement/{advertisement_id}/", response_model=scheme.GetAdResponse)
async def get_add(session: SessionDependency, advertisement_id: int, raise_exception=True):
    advertisement = await get_item(session, Advertisement, advertisement_id)

    return advertisement.dict


@app.post("/v1/advertisement/", response_model=scheme.CreateAdResponse, summary="Create new add")
async def create_add(advertisement_json: scheme.CreateAdRequest, session: SessionDependency, token: TokenDependency):
    advertisement = Advertisement(**advertisement_json.dict(), user_id=token.user_id)
    await auth.check_access_rights(session, token, advertisement, write=False, read=True)
    advertisement = await add_item(session, advertisement)
    return {"id": advertisement.id}


@app.patch("/v1/advertisement/{advertisement_id}/", response_model=scheme.UpdateAdResponse)
async def update_add(advertisement_json: scheme.UpdateAdRequest,
                     session: SessionDependency,
                     advertisement_id: int,
                     token: TokenDependency
                     ):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    await auth.check_access_rights(session, token, advertisement, write=True, read=False)

    advertisement_dict = advertisement_json.dict(exclude_unset=True)
    for field, value in advertisement_dict.items():
        setattr(advertisement, field, value)

    advertisement = await add_item(session, advertisement)
    return advertisement.dict


@app.delete("/v1/advertisement/{advertisement_id}/", response_model=scheme.OkResponse)
async def delete_add(session: SessionDependency, advertisement_id: int,
                     token: TokenDependency):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    await auth.check_access_rights(session, token, advertisement, write=True, read=False)
    await session.delete(advertisement)
    await session.commit()
    return {"status": "ok"}


@app.get("/v1/advertisement/")
async def search(session: SessionDependency, title: str):
    advertisement = await search_item(session, title)

    return {f'Search result for "{title}"': advertisement}


@app.post("/v1/login/", response_model=scheme.LoginResponse)
async def login(session: SessionDependency, login_data: scheme.LoginRequest):

    user_query = select(User).where(User.login == login_data.login)
    user_model = await session.scalar(user_query)

    if user_model is None:
        raise fastapi.HTTPException(status_code=401, detail="User or password is incorrect")

    if not auth.check_password(login_data.password, user_model.password):
        raise fastapi.HTTPException(status_code=401, detail="User or password is incorrect")

    token = Token(user_id=user_model.user_id)
    await add_item(session, token)

    return token.dict


@app.post("/v1/user/", response_model=scheme.CreateUserResponse)
async def create_user(user_data: scheme.CreateUserRequest, session: SessionDependency):
    user = User(**user_data.dict())
    user.password = auth.hash_password(user_data.password)
    user.roles = [await auth.get_default_role(session)]
    user = await add_item(session, user)
    return user.dict


@app.get("/v1/user/{user_id}/", response_model=scheme.GetUserResponse)
async def get_user(session: SessionDependency, user_id: int):
    user = await crud.get_user(session, user_id)
    return user


@app.patch("/v1/user/{user_id}/", response_model=scheme.UpgradeUserResponse)
async def update_user(user_data: scheme.UpgradeUserRequest,
                      session: SessionDependency,
                      user_id: int,
                      token: TokenDependency):
    user = await crud.get_user(session, user_id)
    await auth.check_access_rights(session, token, user, write=True, read=False)
    user_dict = user_data.dict()
    for field, value in user_dict.items():
        setattr(user, field, value)

    user = await add_item(session, user)
    return user.dict


@app.delete("/v1/user/{user_id}/", response_model=scheme.OkResponse)
async def delete_user(session: SessionDependency,
                      user_id: int,
                      token: TokenDependency):

    user = await crud.get_user(session, user_id)
    await auth.check_access_rights(session, token, user, write=True, read=False)
    await session.delete(user)
    await session.commit()
    return {"status": "ok"}
