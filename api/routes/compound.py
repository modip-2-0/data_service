from fastapi import APIRouter
from models.compound import CompoundCreate, Compound
from crud.compound import create_compound, get_compound
from api.dependencies import AsyncMongoDB

router = APIRouter(prefix="/compound", tags=['Compounds'])

@router.get("/")
async def list_compounds(db: AsyncMongoDB) -> list[int]:
    """
    Retrieve all chemical compounds from the database.
    
    Args:
        db (AsyncMongoDB): Database connection instance injected by FastAPI
        
    Returns:
        list[int]: List of all compound id documents in the database
        
    Note:
        Uses async iteration for better memory efficiency with large datasets
    """
    response = []
    async for doc in db.compound.find({}):
        response.append(doc["cid"])
    return response

@router.post("/insert", response_model=Compound)
async def insert_compound(db: AsyncMongoDB, compound: CompoundCreate) -> Compound:
    """
    Create a new compound document in the database.
    
    Args:
        db (AsyncMongoDB): Database connection instance
        compound (CompoundCreate): Compound data to be inserted
        
    Returns:
        Compound: Created compound document with MongoDB ID
        
    Raises:
        HTTPException: If database operation fails
    """
    return await create_compound(db, compound)


@router.get("/get/{cid}", response_model=Compound)
async def get(db: AsyncMongoDB, cid: int) -> Compound:
    """
    Retrieve a compound document by its CID.
    
    Args:
        db (AsyncMongoDB): Database connection instance
        cid (int): Compound ID to search for
        
    Returns:
        Compound: Compound document if found
        
    Raises:
        HTTPException: If compound is not found
    """
    return await get_compound(db, cid)