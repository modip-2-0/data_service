from fastapi import APIRouter

from models.compound import CompoundCreate, Compound
from crud.compound import create_compound
from api.dependencies import AsyncMongoDB

router = APIRouter(prefix="/compound", tags=['compounds'])

@router.get("/")
async def list_compounds(db: AsyncMongoDB) -> list[Compound]:
    # response = list(db.compound.find({}))
    # for item in response:
    #     item["_id"] = str(item["_id"])
    # return response
    response = []
    async for doc in db.compound.find({}): # Itera asíncronamente
        #doc["_id"] = str(doc["_id"]) # Convertir ObjectId a string
        response.append(doc) # Conversión explícita a Pydantic Model
    return response

@router.post("/insert", response_model=Compound)
async def insert_compound(db: AsyncMongoDB, compound: CompoundCreate) -> Compound:
    return await create_compound(db,compound)    
    