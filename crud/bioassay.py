from fastapi import HTTPException
import logging
from core.db import AsyncIOMotorClient
from models.bioassay import Bioassay, BioassayCreate

DB_COLLECTION = "bioassay"

async def create_bioassay(db: AsyncIOMotorClient, bioassay: BioassayCreate) -> Bioassay:
    """
    Creates a new bioassay document in the database.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance
        bioassay (BioassayCreate): Bioassay data to be inserted

    Returns:
        Bioassay: The created bioassay document

    Raises:
        HTTPException: If database operation fails
    """
    logging.info(f'Inserting bioassay {bioassay.aid} into db...')
    try:
        await db[DB_COLLECTION].insert_one(dict(bioassay))
        return await db[DB_COLLECTION].find_one({"aid": bioassay.aid})
    except Exception as e:
        logging.error(f"Error creating bioassay: {e}")
        raise HTTPException(status_code=500, detail="Failed to create bioassay")


async def get_bioassay(db: AsyncIOMotorClient, aid: int) -> Bioassay:
    """
    Retrieves a bioassay document by its assay ID (aid).

    Args:
        db (AsyncIOMotorClient): MongoDB client instance
        aid (int): PubChem Assay ID to search for

    Returns:
        Bioassay: The found bioassay document

    Raises:
        HTTPException: If bioassay is not found (404) or database operation fails
    """
    try:
        doc = await db[DB_COLLECTION].find_one({"aid": aid})
        if not doc:
            raise HTTPException(
                status_code=404, 
                detail=f"No bioassay found for aid: {aid}"
            )
        return doc
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving bioassay: {e}")
        raise HTTPException(status_code=500, detail="Database error")


async def delete_bioassays(db: AsyncIOMotorClient):
    """
    Deletes all bioassay documents from the database.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance    
    """
    try:
        result = await db[DB_COLLECTION].delete_many({})
        logging.info(f'Deleted {result.deleted_count} bioassays.')        
    except Exception as e:
        logging.error(f"Error deleting bioassays: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete bioassays")
