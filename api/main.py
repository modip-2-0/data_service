from fastapi import APIRouter

from api.routes import bioassay
from api.routes import compound
from api.routes import download

api_router = APIRouter()
api_router.include_router(bioassay.router)
api_router.include_router(compound.router)
api_router.include_router(download.router)