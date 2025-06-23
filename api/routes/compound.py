from fastapi import APIRouter, HTTPException
from models.compound import CompoundCreate, Compound
from crud.compound import create_compound, get_compound, delete_compounds
from api.dependencies import AsyncMongoDB

from crud.query import get_queries_by_user

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


@router.delete("/drop")
async def drop_compounds(db: AsyncMongoDB):
    """
    Delete all compound documents from the database.
    
    Args:
        db (AsyncMongoDB): Database connection instance       
    """
    return await delete_compounds(db)



@router.get(
    "/user/{username}",
    response_model=list[Compound],
    summary="Get all unique compounds for a user"
)
async def get_user_compounds(db: AsyncMongoDB, username: str):
    """
    Retrieves all unique compound documents associated with a user's bioassays.
    
    Steps:
    1. Get all bioassays for the user
    2. Extract unique compound IDs from all bioassays
    3. Fetch corresponding compound documents
    
    Args:
        db: MongoDB client
        username: User to filter compounds
    
    Returns:
        List of unique CompoundDB documents
    """
    try:
        # Paso 1: Obtener ensayos del usuario
        assays = await get_user_assays(db, username)
        
        # Paso 2: Consolidar IDs únicos de compuestos
        compound_ids = set()
        for assay in assays:
            compound_ids.update(assay.get("compounds", []))
        
        if not compound_ids:
            return []
        
        # Paso 3: Obtener documentos de compuestos
        cursor = db["compound"].find({"cid": {"$in": list(compound_ids)}})
        return await cursor.to_list(length=None)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve compounds")
    

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