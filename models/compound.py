from pydantic import BaseModel

from models.mongo import MongoModel

class CompoundCreate(BaseModel):
    cid: int    
    name: str       

    class Config:
        json_schema_extra = {
            "example": {
                "cid": 1,
                "name": "Acetyl-DL-carnitine"                
            }
        }    
    
  
class Compound(MongoModel, CompoundCreate):    
    class Config:
        json_schema_extra = {
            "example": {
                "_id": "678b037f46f8d52a70581ad6",
                "cid": 1,
                "name": "Acetyl-DL-carnitine" 
            }
        }
