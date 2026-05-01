"""
Module for downloading bioassay data from PubChem's REST API.

This module provides functionality to fetch and process bioassay information
including summary data and compound relationships.
"""


import logging
import requests
from typing import Set
from motor.motor_asyncio import AsyncIOMotorClient
import pubchempy as pcp
from fastapi import HTTPException

from models.bioassay import BioassayIn
from crud.bioassay import create_bioassay

# Base URL de la API REST de PubChem
BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid"

async def download_bioassay(db: AsyncIOMotorClient, aid: int):
    """
    Descarga un ensayo desde PubChem:
    - Metadatos generales con pubchempy (name, description, etc.)
    - Tabla de resultados con requests (para obtener los CIDs)
    """
    logging.info(f"Downloading bioassay AID={aid} from PubChem...")

    # 1. Obtener metadatos con pubchempy (resumen)
    try:
        assay = pcp.Assay.from_aid(aid)
    except Exception as e:
        logging.error(f"Failed to fetch assay summary for {aid}: {e}")
        raise HTTPException(status_code=404, detail=f"Assay AID={aid} not found")

    # 2. Obtener tabla de datos concisos con requests
    try:
        url = f"{BASE_URL}/{aid}/concise/JSON"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rows = data["Table"]["Row"]
        cids = {int(row["Cell"][2]) for row in rows}
    except Exception as e:
        logging.error(f"Failed to fetch concise data for AID {aid}: {e}")
        # Si falla, al menos guardamos el ensayo sin lista de compuestos
        rows = []
        cids = {}


    bioassay_data = BioassayIn(
        aid=assay.aid,
        name=assay.name,
        description=getattr(assay, 'description', None),
        project_category=str(assay.project_category) if hasattr(assay, 'project_category') else None,
        comments=getattr(assay, 'comments', None),
        target=getattr(assay, 'target', None),
        compounds=list(cids),
        revision=getattr(assay, 'revision', None),
        aid_version=getattr(assay, 'aid_version', None),
    )

    # 5. Guardar en MongoDB (la función create_bioassay debe existir)
    return await create_bioassay(db, bioassay_data)

