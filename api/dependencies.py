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



# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from api.database import get_db  # o la función que retorna la conexión a MongoDB
# from crud.user import get_user_by_id
# from models.user import UserOut

# SECRET = "1652e68e6e5c4c9d21c6c38a87c143ea3f0b865fe318fae0374de808f5f0016f"
# ALGORITHM = "HS256"

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: AsyncMongoDB = Depends(get_db)
# ) -> UserOut:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = await get_user_by_id(db, user_id)
#     return user

# @router.get("/user/me")
# async def get_me(current_user: UserOut = Depends(get_current_user)):
#     return current_user
