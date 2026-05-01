from pydantic import BaseModel, EmailStr
from models.mongo import MongoModel, PyObjectId

class UserIn(BaseModel):
    email: str
    name: str
    password: str
    
class UserDB(MongoModel):
    email: str
    name: str
    hashed_password: str 

class UserOut(BaseModel):
    id: PyObjectId
    email: str
    name: str  


