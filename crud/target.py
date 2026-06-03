import logging
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models.target import TargetDB

DB_COLLECTION = "target"

async def create_target_doc(db: AsyncIOMotorClient, doc: dict) -> TargetDB:
    """Inserta un documento de target en MongoDB y devuelve el objeto."""
    try:
        result = await db[DB_COLLECTION].insert_one(doc)
        inserted = await db[DB_COLLECTION].find_one({"_id": result.inserted_id})
        return TargetDB(**inserted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

async def get_target_by_id(db: AsyncIOMotorClient, target_id: str) -> TargetDB:
    try:
        obj_id = ObjectId(target_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    doc = await db[DB_COLLECTION].find_one({"_id": obj_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Target not found")
    return TargetDB(**doc)

async def get_targets_by_user(db: AsyncIOMotorClient, username: str) -> list[TargetDB]:
    cursor = db[DB_COLLECTION].find({"user": username})
    result = []
    async for doc in cursor:
        result.append(TargetDB(**doc))
    return result

async def delete_all_targets(db: AsyncIOMotorClient):
    result = await db[DB_COLLECTION].delete_many({})
    logging.info(f"Deleted {result.deleted_count} targets")
    return {"deleted": result.deleted_count}