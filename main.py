from fastapi import FastAPI
from core.db import connect_and_init_db, close_db_connect
from api.main import api_router


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="Data Service API",
        description="API for managing data from PubChem",
        version="1.0.0"
    )
    
    # Register event handlers
    app.add_event_handler("startup", connect_and_init_db)
    app.add_event_handler("shutdown", close_db_connect)
    
    # Include API routes
    app.include_router(api_router)
    
    return app


app = create_app()