from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global database client
db_client: AsyncIOMotorClient = None

async def get_db() -> AsyncIOMotorClient:
    """
    Get database instance for dependency injection.
    
    Returns:
        AsyncIOMotorClient: MongoDB client instance for the 'modip' database
    """
    db_name = "modip"
    return db_client[db_name]

async def connect_and_init_db() -> None:
    """
    Initialize MongoDB connection on application startup.
    
    Establishes connection to local MongoDB instance.
    Sets global db_client for use across the application.
    
    Raises:
        Exception: If connection to MongoDB fails
    """
    global db_client
    try:
        db_client = AsyncIOMotorClient("mongodb://mongodb:27017")
        #db_client = AsyncIOMotorClient("mongodb://localhost:27017")
        logger.info('Connected to MongoDB successfully')
    except Exception as e:
        logger.exception('Failed to connect to MongoDB: %s', e)
        raise

async def close_db_connect() -> None:
    """
    Close MongoDB connection on application shutdown.
    
    Safely closes the database connection if it exists.
    Resets the global db_client to None.
    """
    global db_client
    if db_client is None:
        logger.warning('Database connection is None, nothing to close')
        return
        
    db_client.close()
    db_client = None
    logger.info('MongoDB connection closed successfully')
