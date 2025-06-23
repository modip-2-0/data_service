from fastapi import HTTPException
import logging
from core.db import AsyncIOMotorClient
from models.query import QueryIn, QueryDB

DB_COLLECTION = "query"

async def create_query(db: AsyncIOMotorClient, query: QueryIn) -> QueryDB:

    try:
        await db[DB_COLLECTION].insert_one(dict(query))
        return await db[DB_COLLECTION].find_one({"content": query.content, "user": query.user})
    except Exception as e:
        logging.error(f"Error creating QueryDB: {e}")
        raise HTTPException(status_code=500, detail="Failed to create QueryDB")


async def get_queries_by_user(db: AsyncIOMotorClient, user: str) -> list[QueryDB]:
    """
    Retrieves all QueryDB documents for a specific user.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance
        user (str): Username to filter queries

    Returns:
        list[QueryDB]: List of QueryDB documents for the specified user

    Raises:
        HTTPException: If database operation fails
    """
    try:
        cursor = db[DB_COLLECTION].find({"user": user})
        queries = await cursor.to_list(length=None)
        return queries
    except Exception as e:
        logging.error(f"Error retrieving queries for user {user}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve queries")



async def delete_queries_by_user(db: AsyncIOMotorClient, user: str) -> int:

    try:

        result = await db[DB_COLLECTION].delete_many({"user": user})      
        return result.deleted_count
        
    except Exception as e:
        logging.error(f"Error eliminando consultas para usuario {user}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error del servidor al eliminar consultas: {str(e)}"
        )