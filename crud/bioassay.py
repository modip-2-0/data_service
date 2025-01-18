from fastapi import HTTPException
import logging

from core.db import AsyncIOMotorClient
from models.bioassay import Bioassay, BioassayCreate


DB_COLLECTION = "bioassay"

async def create_bioassay(db: AsyncIOMotorClient, bioassay: BioassayCreate) -> Bioassay:
    logging.info(f'Inserting bioassay {bioassay.aid} into db...')
    await db[DB_COLLECTION].insert_one(dict(bioassay))
    return await db.bioassay.find_one({"aid":bioassay.aid})

async def get_bioassay(db: AsyncIOMotorClient, aid: int):    
    doc = await db[DB_COLLECTION].find_one({"aid": aid})    
    if not doc:
        raise HTTPException(status_code=404, detail="No bioassay found for given aid")
    return doc




