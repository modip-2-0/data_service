from fastapi import APIRouter, HTTPException
from models.bioassay import BioassayCreate, Bioassay
from crud.bioassay import create_bioassay, get_bioassay, delete_bioassays
from api.dependencies import AsyncMongoDB

from crud.query import get_queries_by_user

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



@router.get(
    "/user/{username}",
    response_model=list[Bioassay],
    summary="Get all unique bioassays for a user"
)
async def get_user_assays(db: AsyncMongoDB, username: str):
    """
    Retrieves all unique bioassay documents associated with a user's queries.
    
    Steps:
    1. Get all queries for the user
    2. Extract unique assay IDs from all queries
    3. Fetch corresponding assay documents
    
    Args:
        db: MongoDB client
        username: User to filter assays
    
    Returns:
        List of unique BioAssayDB documents
    """
    try:
        # Paso 1: Obtener todas las queries del usuario
        queries = await get_queries_by_user(db, username)
        
        # Paso 2: Consolidar IDs únicos de ensayos
        assay_ids = set()
        for query in queries:
            assay_ids.update(query.get("assays", []))
        
        if not assay_ids:
            return []
        
        # Paso 3: Obtener documentos de ensayos
        cursor = db["bioassay"].find({"aid": {"$in": list(assay_ids)}})
        return await cursor.to_list(length=None)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve assays")
    