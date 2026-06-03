from pydantic import BaseModel
from typing import List, Optional
from models.mongo import MongoModel

# models/query.py
from pydantic import BaseModel
from typing import List, Optional
from models.mongo import MongoModel

class QueryIn(BaseModel):
    user: str
    content: str
    targets: List[str]

class QueryDB(MongoModel):
    user: str
    content: str
    targets: List[str]
    assays: List[int] = []
    compounds: List[int] = []   