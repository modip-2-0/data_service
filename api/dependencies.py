"""
Dependencies module for FastAPI application.

This module provides dependency injection configurations for database connections
and other shared resources across the API endpoints.
"""

from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends

from core.db import get_db

# Type annotation for MongoDB dependency injection
AsyncMongoDB = Annotated[AsyncIOMotorClient, Depends(get_db)]

