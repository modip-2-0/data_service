from pydantic import BaseModel
from models.mongo import MongoModel

class QueryIn(BaseModel):
    user: str
    content: str
    assays: list[int]


class QueryDB(MongoModel, QueryIn):
    pass   