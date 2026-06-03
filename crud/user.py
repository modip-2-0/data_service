from fastapi import HTTPException
from core.db import AsyncIOMotorClient
from bson import ObjectId
from models.user import UserIn, UserDB, UserOut
import logging

# Constants should be at module level
DB_COLLECTION = "user"

async def create_user(db: AsyncIOMotorClient, email: str, name: str, hashed_password: str) -> UserOut:
    user_doc = {
        "email": email,
        "name": name,
        "hashed_password": hashed_password
    }
    try:
        result = await db[DB_COLLECTION].insert_one(user_doc)
        return UserOut(id=result.inserted_id, email=email, name=name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

async def get_user_by_email(db: AsyncIOMotorClient, email: str) -> UserOut:
    user_doc = await db[DB_COLLECTION].find_one({"email": email})
    if not user_doc:
        raise HTTPException(status_code=404, detail=f"No user found for email: {email}")
    return UserOut(id=user_doc["_id"], email=user_doc["email"], name=user_doc["name"])

async def get_user_db_by_email(db: AsyncIOMotorClient, email: str) -> UserDB:
    user_doc = await db[DB_COLLECTION].find_one({"email": email})
    if not user_doc:
        raise HTTPException(status_code=404, detail=f"No user found for email: {email}")
    return UserDB(
        id=user_doc["_id"],
        email=user_doc["email"],
        name=user_doc["name"],
        hashed_password=user_doc["hashed_password"]
    )

async def get_user_by_id(db: AsyncIOMotorClient, user_id: str) -> UserOut:
    try:
        obj_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user id format")
    user_doc = await db[DB_COLLECTION].find_one({"_id": obj_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(id=user_doc["_id"], email=user_doc["email"], name=user_doc["name"])

async def delete_users(db: AsyncIOMotorClient):
    try:
        result = await db[DB_COLLECTION].delete_many({})
        logging.info(f'Deleted {result.deleted_count} users.')
    except Exception as e:
        logging.error(f"Error deleting users: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete users")