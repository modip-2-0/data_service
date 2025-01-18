from pydantic import BaseModel

from models.mongo import MongoModel

class BioassayCreate(BaseModel):
    aid: int    
    name: str
    description: list[str]      
    compounds: list[int]

    class Config:
        json_schema_extra = {
            "example": {
                "aid": 1,
                "name": "NCI human tumor cell line growth inhibition assay",
                "description": ["Growth inhibition of the NCI-H23 human Non-Small Cell Lung tumor cell line is measured as a screen for anti-cancer activity."],
                "compounds": [5477653,155815172]
            }
        }    
    
  
class Bioassay(MongoModel, BioassayCreate):    
    class Config:
        json_schema_extra = {
            "example": {
                "_id": "678b037f46f8d52a70581ad6",
                "aid": 1,
                "name": "NCI human tumor cell line growth inhibition assay",
                "description": ["Growth inhibition of the NCI-H23 human Non-Small Cell Lung tumor cell line is measured as a screen for anti-cancer activity."],
                "compounds": [5477653,155815172]
            }
        }

    
    
