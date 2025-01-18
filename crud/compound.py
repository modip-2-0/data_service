from fastapi import HTTPException

from core.db import AsyncIOMotorClient
from models.compound import Compound, CompoundCreate

import logging

DB_COLLECTION = "compound"

async def create_compound(db: AsyncIOMotorClient, compound: CompoundCreate) -> Compound:
    logging.info(f'Inserting compound {compound.cid} into db...')
    await db.compound.insert_one(dict(compound))
    return await db.compound.find_one({"cid":compound.cid})

async def get_compound(db: AsyncIOMotorClient, cid: int):    
    doc = await db[DB_COLLECTION].find_one({"cid": cid})    
    if not doc:
        raise HTTPException(status_code=404, detail="No compound found for given cid")
    return doc
