import fastapi

from typing import Annotated

from lifespan import lifespan
from models import Advertisement
import scheme

from dependencies import SessionDependency

from crud import add_item, get_item, search_item

app = fastapi.FastAPI(
    title="purchase API",
    version='1.0',
    description="API for purchase and sell",
    lifespan=lifespan
)

TokenHeader = Annotated[str, fastapi.Header()]


@app.get("/v1/advertisement/{advertisement_id}/", response_model=scheme.GetAdResponse)
async def get_add(session: SessionDependency, advertisement_id: int):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    return advertisement.dict


@app.post("/v1/advertisement/", response_model=scheme.CreateAdResponse, summary="Create new add")
async def create_add(advertisement_json: scheme.CreateAdRequest, session: SessionDependency):

    advertisement = Advertisement(**advertisement_json.dict())
    advertisement = await add_item(session, advertisement)
    return {"id": advertisement.id}


@app.patch("/v1/advertisement/{advertisement_id}/", response_model=scheme.UpdateAdResponse)
async def update_add(advertisement_json: scheme.UpdateAdRequest, session: SessionDependency, advertisement_id: int):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    advertisement_dict = advertisement_json.dict(exclude_unset=True)
    for field, value in advertisement_dict.items():
        setattr(advertisement, field, value)

    advertisement = await add_item(session, advertisement)
    return advertisement.dict


@app.delete("/v1/advertisement/{advertisement_id}/", response_model=scheme.OkResponse)
async def delete_add(session: SessionDependency, advertisement_id: int):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    await session.delete(advertisement)
    await session.commit()
    return {"status": "ok"}


@app.get("/v1/advertisement/")
async def search(session: SessionDependency, title: str):
    advertisement = await search_item(session, title)

    return {f'Search result for "{title}"': advertisement}
