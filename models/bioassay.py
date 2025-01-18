from pydantic import BaseModel
from models.mongo import MongoModel

class BioassayCreate(BaseModel):
    """
    Pydantic model for creating a new bioassay.
    
    Attributes:
        aid (int): Unique PubChem Assay ID
        name (str): Name/title of the bioassay
        description (list[str]): List of text descriptions about the bioassay
        compounds (list[int]): List of PubChem Compound IDs (CIDs) tested in this assay
    """
    aid: int    
    name: str
    description: list[str]      
    compounds: list[int]

    class Config:
        """Configuration with example data for API documentation"""
        json_schema_extra = {
            "example": {
                "aid": 1,
                "name": "NCI human tumor cell line growth inhibition assay",
                "description": [
                    "Growth inhibition of the NCI-H23 human Non-Small Cell Lung "
                    "tumor cell line is measured as a screen for anti-cancer activity."
                ],
                "compounds": [5477653, 155815172]
            }
        }    

class Bioassay(MongoModel, BioassayCreate):    
    """
    Pydantic model representing a bioassay document in MongoDB.
    Inherits all fields from BioassayCreate and adds MongoDB-specific fields.
    
    Additional Attributes:
        _id: MongoDB ObjectId field (inherited from MongoModel)
    """
    class Config:
        """Configuration with example data including MongoDB ID"""
        json_schema_extra = {
            "example": {
                "_id": "678b037f46f8d52a70581ad6",
                "aid": 1,
                "name": "NCI human tumor cell line growth inhibition assay",
                "description": [
                    "Growth inhibition of the NCI-H23 human Non-Small Cell Lung "
                    "tumor cell line is measured as a screen for anti-cancer activity."
                ],
                "compounds": [5477653, 155815172]
            }
        }