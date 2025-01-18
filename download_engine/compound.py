"""
Module for downloading compound data from PubChem's REST API.

This module provides functionality to fetch and process chemical compound information
from PubChem, including basic properties like compound names.
"""

import requests
from core.db import AsyncIOMotorClient
from crud.compound import Compound, CompoundCreate, create_compound

# PubChem REST API base URL for compound endpoints
BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid"

async def download_compound(db: AsyncIOMotorClient, cid: int) -> Compound:
    """
    Downloads compound data from PubChem and stores it in the database.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance
        cid (int): PubChem Compound ID (CID)

    Returns:
        Compound: Created compound document with MongoDB ID

    Raises:
        requests.RequestException: If PubChem API request fails
        HTTPException: If database operation fails
    """
    # Construct URL for compound title property
    url = f"{BASE_URL}/{cid}/property/Title/JSON"
    
    # Fetch compound data from PubChem
    response = requests.get(url)
    data = response.json()["PropertyTable"]["Properties"][0]

    # Create compound model instance
    compound = CompoundCreate(
        cid=cid,
        name=data["Title"]
    )

    # Store in database and return
    return await create_compound(db, compound)