from fastapi import APIRouter
from models.query import QueryIn, QueryDB  
from crud.query import create_query, get_queries_by_user, delete_queries_by_user
from download_engine.download import download
from download_engine.entrez import search_bioassays
from api.dependencies import AsyncMongoDB

from fastapi import BackgroundTasks, status, Body
router = APIRouter(tags=["Queries"])

@router.post(
    "/queries/",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new query"
)
async def create_new_query(db: AsyncMongoDB, background_tasks: BackgroundTasks, query: list = Body(...)): 
    user = query[0]
    content = query[1]
    result = await search_bioassays(content)

    background_tasks.add_task(download, db, result)
    queryDB = await create_query(db, QueryIn(user=user, content=content, assays=result))

    return len(queryDB["assays"])


@router.get(
    "/queries/user/{username}",
    response_model=list[QueryDB],
    summary="Get all queries for a user"
)
async def get_user_queries(db: AsyncMongoDB, username: str):
    return await get_queries_by_user(db, username)
    

@router.delete(
    "/queries/user/{username}",
    summary="Delete all queries for a user",
)
async def delete_user_queries(db: AsyncMongoDB, username: str):

    deleted_count = await delete_queries_by_user(db, username)
    return {
        "status": "success",
        "message": f"Deleted {deleted_count} queries for user {username}",
        "deleted_count": deleted_count
    }
