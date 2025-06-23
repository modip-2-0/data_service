from pydantic import BaseModel, Field
from models.mongo import MongoModel


class BioassayDataIn(BaseModel):
    """
    Pydantic model for creating a new bioassay data entry.
    """

    aid: int = Field(..., description="Unique PubChem BioAssay ID.")
    sid: int = Field(..., description="Unique PubChem Substance ID.")
    cid: int = Field(..., description="Unique PubChem Compound ID.")
    activity_outcome: str = Field(..., description="Activity outcome of the bioassay (e.g., active, inactive).")
    target_accession: str = Field(..., description="Accession number of the target associated with the bioassay.")
    target_geneid: int = Field(..., description="Gene ID of the target associated with the bioassay.")
    activity_value_um: float = Field(..., description="Activity value in micromolar (uM).")
    activity_name: str = Field(..., description="Name of the activity associated with the bioassay.")
    assay_name: str = Field(..., description="Name of the assay used in the bioassay.")
    assay_type: str = Field(..., description="Type of the assay used in the bioassay.")
    pubmed_id: int = Field(..., description="PubMed ID associated with the bioassay.")
    rna_i: str = Field(..., description="RNA interference information associated with the bioassay.")


class BioassayDataDB(MongoModel, BioassayDataIn): 
    """
    Pydantic model representing a bioassay data entry document in MongoDB.
    Inherits all fields from CompoundIN and adds MongoDB-specific fields.
    
    Additional Attributes:
        _id: MongoDB ObjectId field (inherited from MongoModel)
    """
    pass
