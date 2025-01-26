from fastapi import HTTPException
from core.db import AsyncIOMotorClient
from models.compound import Compound, CompoundCreate
import logging

# Constants should be at module level
DB_COLLECTION = "compound"

async def create_compound(db: AsyncIOMotorClient, compound: CompoundCreate) -> Compound:
    """
    Creates a new compound document in the database.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance
        compound (CompoundCreate): Compound data to be inserted

    Returns:
        Compound: The created compound document

    Raises:
        HTTPException: If database operation fails
    """
    logging.info(f'Inserting compound {compound.cid} into db...')
    try:
        await db[DB_COLLECTION].insert_one(dict(compound))
        return await db[DB_COLLECTION].find_one({"cid": compound.cid})
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating compound: {str(e)}"
        )

async def get_compound(db: AsyncIOMotorClient, cid: int) -> Compound:
    """
    Retrieves a compound document from the database by its CID.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance
        cid (int): PubChem Compound ID to search for

    Returns:
        Compound: The found compound document

    Raises:
        HTTPException: If compound is not found
    """    
    doc = await db[DB_COLLECTION].find_one({"cid": cid})    
    if not doc:
        raise HTTPException(
            status_code=404, 
            detail=f"No compound found for CID: {cid}"
        )
    return doc


async def delete_compounds(db: AsyncIOMotorClient):
    """
    Deletes all compounds documents from the database.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance    
    """
    try:
        result = await db[DB_COLLECTION].delete_many({})
        logging.info(f'Deleted {result.deleted_count} compounds.')        
    except Exception as e:
        logging.error(f"Error deleting compounds: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete compounds")
