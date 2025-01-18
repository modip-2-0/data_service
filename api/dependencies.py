from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends


from core.db import get_db

AsyncMongoDB = Annotated[AsyncIOMotorClient, Depends(get_db)]


