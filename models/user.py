from pydantic import BaseModel
from models.mongo import MongoModel


class UserIn(BaseModel):
    name: str  
    username: str
    email: str
    password: str   

    
class UserDB(MongoModel, UserIn):
    pass    


class UserOut(BaseModel):
    name: str  
    username: str
    email: str
