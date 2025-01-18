from pydantic import BaseModel
from models.mongo import MongoModel

class CompoundCreate(BaseModel):
    """
    Pydantic model for creating a new chemical compound.
    
    Attributes:
        cid (int): Unique PubChem Compound ID
        name (str): Chemical compound name/title from PubChem
    """
    cid: int    
    name: str       

    class Config:
        """Configuration with example data for API documentation"""
        json_schema_extra = {
            "example": {
                "cid": 1,
                "name": "Acetyl-DL-carnitine"                
            }
        }    
    
class Compound(MongoModel, CompoundCreate):    
    """
    MongoDB model for chemical compounds, inheriting from MongoModel and CompoundCreate.
    
    Extends CompoundCreate by adding MongoDB-specific fields like _id.
    Used for database operations and API responses.
    """
    class Config:
        """Configuration with example data including MongoDB ID"""
        json_schema_extra = {
            "example": {
                "_id": "678b037f46f8d52a70581ad6",
                "cid": 1,
                "name": "Acetyl-DL-carnitine" 
            }
        }