from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from models.mongo import MongoModel

class BioassayIn(BaseModel):
    """
    Input model for a bioassay (e.g., from user upload or manual creation).
    All fields are optional because the user may provide only partial information.
    """
    aid: Optional[int] = Field(None, description="PubChem Assay Identifier (AID)")
    name: Optional[str] = Field(None, description="Assay name")
    description: Optional[List[str]] = Field(None, description="Assay description")
    project_category: Optional[str] = Field(None, description="Project category (mlscn, mlpcn, etc.)")
    comments: Optional[List[str]] = Field(None, description="Additional comments")
    target: Optional[List[Dict[str, Any]]] = Field(None, description="Target information")
    compounds: Optional[List[int]] = Field(None, description="List of compound CIDs tested in this assay")
    revision: Optional[int] = Field(None, description="Revision identifier for textual description")
    aid_version: Optional[int] = Field(None, description="Version incremented when record is updated by depositor")

    class Config:
        json_schema_extra = {
            "example": {
                "aid": 1234,
                "name": "Inhibition of ABCG2",
                "description": "This assay measures inhibition of ABCG2 transporter...",
                "project_category": "mlscn",
                "compounds": [2244, 12345, 67890]
            }
        }

class BioassayDB(MongoModel):
    """
    MongoDB document model for bioassays.
    Extends MongoModel to include the automatically generated _id.
    """
    aid: Optional[int] = None
    name: Optional[str] = None
    description: Optional[List[str]] = None
    project_category: Optional[str] = None
    comments: Optional[List[str]] = None
    target: Optional[List[Dict[str, Any]]] = None
    compounds: Optional[List[int]] = None
    revision: Optional[int] = None
    aid_version: Optional[int] = None



# from pydantic import BaseModel
# from models.mongo import MongoModel

# class BioassayCreate(BaseModel):

#     aid: int    
#     name: str
#     description: list[str]      
#     compounds: list[int]

#     # class Config:
#     #     """Configuration with example data for API documentation"""
#     #     json_schema_extra = {
#     #         "example": {
#     #             "aid": 1,
#     #             "name": "NCI human tumor cell line growth inhibition assay",
#     #             "description": [
#     #                 "Growth inhibition of the NCI-H23 human Non-Small Cell Lung "
#     #                 "tumor cell line is measured as a screen for anti-cancer activity."
#     #             ],
#     #             "compounds": [5477653, 155815172]
#     #         }
#     #     }    

# class Bioassay(MongoModel):  
#     aid: int    
#     name: str
#     description: list[str]      
#     compounds: list[int]  

#     # class Config:
#     #     """Configuration with example data including MongoDB ID"""
#     #     json_schema_extra = {
#     #         "example": {
#     #             "_id": "678b037f46f8d52a70581ad6",
#     #             "aid": 1,
#     #             "name": "NCI human tumor cell line growth inhibition assay",
#     #             "description": [
#     #                 "Growth inhibition of the NCI-H23 human Non-Small Cell Lung "
#     #                 "tumor cell line is measured as a screen for anti-cancer activity."
#     #             ],
#     #             "compounds": [5477653, 155815172]
#     #         }
#     #     }