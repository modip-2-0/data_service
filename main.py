from fastapi import FastAPI
#import uvicron
from contextlib import asynccontextmanager

from core.db import connect_and_init_db, close_db_connect
from api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_and_init_db()
    yield
    await close_db_connect()


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="Data Service API",
        description="API for managing data from PubChem",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Include API routes
    app.include_router(api_router)
    
    return app


app = create_app()