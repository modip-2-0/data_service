from fastapi import APIRouter
from models.bioassay import BioassayCreate, Bioassay
from crud.bioassay import create_bioassay, get_bioassay, delete_bioassays
from api.dependencies import AsyncMongoDB

router = APIRouter(prefix="/bioassay", tags=['Bioassays'])

@router.get("/")
async def list_bioassays(db: AsyncMongoDB) -> list[int]:
    """
    Retrieve all bioassays from the database.
    
    Args:
        db (AsyncMongoDB): Database connection instance injected by FastAPI
        
    Returns:
        list[int]: List of all bioassay id documents in the database
        
    Note:
        Uses async iteration for better memory efficiency with large datasets
    """
    response = []
    async for doc in db.bioassay.find({}):
        response.append(doc["aid"])
    return response

@router.post("/insert", response_model=Bioassay)
async def insert_bioassay(db: AsyncMongoDB, bioassay: BioassayCreate) -> Bioassay:
    """
    Create a new bioassay document in the database.
    
    Args:
        db (AsyncMongoDB): Database connection instance
        bioassay (BioassayCreate): Bioassay data to be inserted
        
    Returns:
        Bioassay: The created bioassay document with MongoDB ID
        
    Raises:
        HTTPException: If database operation fails
    """
    return await create_bioassay(db, bioassay) 


@router.get("/get/{aid}", response_model=Bioassay)
async def get(db: AsyncMongoDB, aid: int) -> Bioassay:
    """
    Retrieve a bioassay document by its ID.
    
    Args:
        aid (int): The ID of the bioassay to retrieve
        db (AsyncMongoDB): Database connection instance
        
    Returns:
        Bioassay: The bioassay document with the specified ID
        
    Raises:
        HTTPException: If the bioassay is not found
    """
    return await get_bioassay(db, aid)


@router.delete("/drop")
async def drop_bioassays(db: AsyncMongoDB):
    """
    Delete all bioassay documents from the database.
    
    Args:
        db (AsyncMongoDB): Database connection instance   
    """
    return await delete_bioassays(db)
    