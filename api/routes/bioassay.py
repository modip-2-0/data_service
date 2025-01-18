from fastapi import APIRouter
from models.bioassay import BioassayCreate, Bioassay
from crud.bioassay import create_bioassay
from api.dependencies import AsyncMongoDB

router = APIRouter(prefix="/bioassay", tags=['Bioassays'])

@router.get("/")
async def list_bioassays(db: AsyncMongoDB) -> list[Bioassay]:
    """
    Retrieve all bioassays from the database.
    
    Args:
        db (AsyncMongoDB): Database connection instance injected by FastAPI
        
    Returns:
        list[Bioassay]: List of all bioassay documents in the database
        
    Note:
        Uses async iteration for better memory efficiency with large datasets
    """
    response = []
    async for doc in db.bioassay.find({}):
        response.append(doc)
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
    