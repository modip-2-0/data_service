from pydantic import BaseModel, Field
from typing import Optional
from models.mongo import MongoModel

class TargetIn(BaseModel):
    """
    Input model for creating a new target (receptor).
    The actual file paths are set by the server during creation.
    """
    name: str = Field(..., description="Descriptive name of the target")
    receptor: str = Field(..., description="Source organism/receptor type, e.g., 'human', 'bovine'")
    user: str = Field(..., description="Owner's username or email")


class TargetDB(MongoModel):
    """
    MongoDB document model for a docking target.
    """
    name: str
    receptor: str
    user: str
    pdbqt_path: str      # path to the uploaded .pdbqt file
    config_path: str     # path to the docking configuration file