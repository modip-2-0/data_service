from fastapi import APIRouter

from api.dependencies import AsyncMongoDB

from download_engine.download import download

router = APIRouter(prefix="/download", tags=['Download Engine'])

@router.post("/{query}")
async def download_query(db: AsyncMongoDB, query: str):
    await download(db,query)