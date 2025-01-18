from fastapi import APIRouter

from models.bioassay import BioassayCreate, Bioassay
from crud.bioassay import create_bioassay
from api.dependencies import AsyncMongoDB

router = APIRouter(prefix="/bioassay", tags=['Bioassays'])

@router.get("/")
async def list_bioassays(db: AsyncMongoDB) -> list[Bioassay]:
    # response = list(db.bioassay.find({}))
    # for item in response:
    #     item["_id"] = str(item["_id"])
    # return response
    response = []
    async for doc in db.bioassay.find({}): # Itera asíncronamente
        #doc["_id"] = str(doc["_id"]) # Convertir ObjectId a string
        response.append(doc) # Conversión explícita a Pydantic Model
    return response

@router.post("/insert", response_model=Bioassay)
async def insert_bioassay(db: AsyncMongoDB, bioassay: BioassayCreate) -> Bioassay:
    return await create_bioassay(db,bioassay)    
    