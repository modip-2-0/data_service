from fastapi import HTTPException
import logging
from core.db import AsyncIOMotorClient
from models.query import QueryDB
from bson import ObjectId

DB_COLLECTION = "query"

async def create_query(db: AsyncIOMotorClient, query_dict: dict) -> QueryDB:
    """
    Inserta un documento de query en MongoDB.
    `query_dict` debe contener: user, content, assays, targets
    """
    try:
        result = await db[DB_COLLECTION].insert_one(query_dict)
        inserted = await db[DB_COLLECTION].find_one({"_id": result.inserted_id})
        return QueryDB(**inserted)
    except Exception as e:
        logging.error(f"Error creating query: {e}")
        raise HTTPException(status_code=500, detail="Failed to create query")

async def get_queries_by_user(db: AsyncIOMotorClient, user: str) -> list[QueryDB]:
    cursor = db[DB_COLLECTION].find({"user": user})
    queries = await cursor.to_list(length=None)
    return [QueryDB(**doc) for doc in queries]

async def delete_queries_by_user(db: AsyncIOMotorClient, user: str) -> int:
    result = await db[DB_COLLECTION].delete_many({"user": user})
    return result.deleted_count


async def update_query_compounds(
    db: AsyncIOMotorClient,
    query_id: str,
    compounds: list[int]
) -> bool:
    try:
        result = await db[DB_COLLECTION].update_one(
            {"_id": ObjectId(query_id)},
            {"$set": {"compounds": compounds}}
        )
        return result.modified_count > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating query compounds: {e}")



async def get_compound_file_paths(db: AsyncIOMotorClient, query_id: str) -> list[dict[str,str]]:
    query = await db.query.find_one({"_id": ObjectId(query_id)})
    if not query:
        raise HTTPException(404, "Query not found")
    cids = query.get("compounds", [])
    result = []    
    for cid in cids:
        compound = await db.compound.find_one({"cid": cid})
        if compound and compound.get("path"):
            result.append({"id": str(cid), "path": compound["path"]})
    return result