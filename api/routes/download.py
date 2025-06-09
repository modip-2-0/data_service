from fastapi import APIRouter, HTTPException
from api.dependencies import AsyncMongoDB
from download_engine.download import download

router = APIRouter(prefix="/download", tags=['Download Engine'])

@router.post("/{query}")
async def download_query(db: AsyncMongoDB, query: str):
    """
    Downloads bioassays and compounds from PubChem based on a search query.
    
    Args:
        db (AsyncMongoDB): Database connection instance injected by FastAPI
        query (str): Search query string to find relevant bioassays in PubChem
        
    Returns:
        dict: Status message indicating completion
        
    Raises:
        HTTPException: If download process fails
    """
    try:
        return await download(db, query)        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}"
        )
