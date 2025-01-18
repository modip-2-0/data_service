from fastapi import FastAPI

from core.db import connect_and_init_db, close_db_connect
from api.main import api_router


app: FastAPI = FastAPI()
app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connect)

app.include_router(api_router)