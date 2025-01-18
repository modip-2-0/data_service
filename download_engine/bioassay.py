"""
Module for downloading bioassay data from PubChem's REST API.

This module provides functionality to fetch and process bioassay information
including summary data and compound relationships.
"""

import requests
from core.db import AsyncIOMotorClient
from crud.bioassay import Bioassay, BioassayCreate, create_bioassay

# PubChem REST API base URL for assay endpoints
BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid"

async def download_bioassay(db: AsyncIOMotorClient, aid: int) -> Bioassay:
    """
    Downloads bioassay data from PubChem and stores it in the database.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance
        aid (int): PubChem Assay ID (AID)

    Returns:
        Bioassay: Created bioassay document with MongoDB ID

    Raises:
        requests.RequestException: If PubChem API requests fail
        HTTPException: If database operation fails
    """
    # Fetch assay summary data
    summary_url = f"{BASE_URL}/{aid}/summary/JSON"
    summary_response = requests.get(summary_url)
    summary = summary_response.json()["AssaySummaries"]["AssaySummary"][0]

    # Fetch assay compound data
    data_url = f"{BASE_URL}/{aid}/concise/JSON"
    data_response = requests.get(data_url)    
    data = data_response.json()["Table"]["Row"]
    
    # Extract unique compound IDs
    cids = {int(row["Cell"][2]) for row in data}

    # Create bioassay document
    bioassay = BioassayCreate(
        aid=aid,
        name=summary["Name"],
        description=summary["Description"],
        compounds=list(cids)
    )

    return await create_bioassay(db, bioassay)

    




