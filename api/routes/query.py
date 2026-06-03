from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, status
from models.query import QueryIn, QueryDB
from crud.query import create_query, get_queries_by_user, delete_queries_by_user, get_compound_file_paths
from download_engine.download import download
from download_engine.entrez import search_bioassays
from api.dependencies import AsyncMongoDB

router = APIRouter(tags=["Queries"])


# cathepsin B AND active AND inhibitor NOT Experimentally measured binding affinity data NOT cathepsin E NOT cathepsin D NOT HCV NOT cathepsin K NOT cathepsin H NOT calpain NOT papain NOT MCF10A NOT trypsin NOT cathepsin G NOT plasmin NOT thrombin NOT urease NOT MT3 NOT APPSwInd NOT water-immersion NOT aid=368053 NOT aid=410195 NOT aid=723768 NOT aid=723765 NOT aid=723764 NOT aid=723762 NOT aid=723760 NOT aid=723759 NOT aid=723751 NOT aid=723754 NOT aid=723752 NOT aid=723748 NOT aid=723769 NOT aid=723749 NOT aid=723742 NOT aid=723758 NOT aid=723756 NOT aid=723757 NOT aid=240746 NOT aid=673910 NOT aid=316530 NOT aid=750035 NOT aid=750030 NOT aid=340380 NOT aid=1063737 NOT aid=1063738 NOT aid=240614 NOT aid=233894




@router.post("/queries/", response_model=QueryDB, status_code=201)
async def create_new_query(
    db: AsyncMongoDB,
    background_tasks: BackgroundTasks,
    query_input: QueryIn = Body(...)
):
    assays = await search_bioassays(query_input.content)
    doc = {
        "user": query_input.user,
        "content": query_input.content,
        "targets": query_input.targets,
        "assays": assays,
        "compounds": []
    }
    query_db = await create_query(db, doc)
    # Pasamos el query_id a la tarea de descarga
    background_tasks.add_task(download, db, assays, query_db.id)
    return query_db



@router.get("/queries/{query_id}/compounds", response_model=list[dict[str,str]])
async def get_compound_by_query(db: AsyncMongoDB, query_id: str):
    return await get_compound_file_paths(db,query_id)




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
