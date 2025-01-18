# import os
# from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# from app.conf.config import Config

# load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_client: AsyncIOMotorClient = None

async def get_db() -> AsyncIOMotorClient:
    # db_name = Config.app_settings.get('db_name')
    db_name = "modip"
    return db_client[db_name]

async def connect_and_init_db():
    global db_client
    try:
        # db_client = AsyncIOMotorClient(
        #     Config.app_settings.get('mongodb_url'),
        #     username=Config.app_settings.get('db_username'),
        #     password=Config.app_settings.get('db_password'),
        #     maxPoolSize=Config.app_settings.get('max_db_conn_count'),
        #     minPoolSize=Config.app_settings.get('min_db_conn_count'),
        #     uuidRepresentation="standard",
        # )
        db_client = AsyncIOMotorClient("mongodb://localhost")
        logger.info('Connected to mongo.')
    except Exception as e:
        logger.exception(f'Could not connect to mongo: {e}')
        raise


async def close_db_connect():
    global db_client
    if db_client is None:
        logger.warning('Connection is None, nothing to close.')
        return
    db_client.close()
    db_client = None
    logger.info('Mongo connection closed.')
