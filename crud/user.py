from fastapi import HTTPException
from core.db import AsyncIOMotorClient
from models.user import UserIn, UserDB, UserOut
import logging

# Constants should be at module level
DB_COLLECTION = "user"


async def create_user(db: AsyncIOMotorClient, user: UserIn) -> UserOut:

    try:
        await db[DB_COLLECTION].insert_one(dict(user))
        userDB: UserDB = await db[DB_COLLECTION].find_one({"username": user.username})
        return UserOut(name=userDB["name"], username=userDB["username"], email=userDB["email"])
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating user: {str(e)}"
        )

async def get_user(db: AsyncIOMotorClient, username: str) -> UserOut:
  
    userDB = await db[DB_COLLECTION].find_one({"username": username})    
    if not userDB:
        raise HTTPException(
            status_code=404, 
            detail=f"No user found for username: {username}"
        )
    return UserOut(name=userDB["name"], username=userDB["username"], email=userDB["email"])


async def get_userDB(db: AsyncIOMotorClient, username: str) -> UserDB:
  
    userDB = await db[DB_COLLECTION].find_one({"username": username})    
    if not userDB:
        raise HTTPException(
            status_code=404, 
            detail=f"No user found for username: {username}"
        )
    return UserDB(name=userDB["name"], username=userDB["username"], email=userDB["email"], password=userDB["password"], _id=userDB["_id"])


async def delete_users(db: AsyncIOMotorClient):
    """
    Deletes all users documents from the database.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance    
    """
    try:
        result = await db[DB_COLLECTION].delete_many({})
        logging.info(f'Deleted {result.deleted_count} compounds.')        
    except Exception as e:
        logging.error(f"Error deleting compounds: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete compounds")
