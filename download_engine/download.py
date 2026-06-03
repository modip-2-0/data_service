"""
Download Engine Module

This module coordinates the download of bioassays and compounds from PubChem
based on search queries. It manages the download process and database storage.
"""

from core.db import AsyncIOMotorClient
from crud.bioassay import get_bioassay
from crud.compound import get_compound
from crud.query import update_query_compounds
from download_engine.bioassay import download_bioassay
from download_engine.compound import download_compound



async def download(db: AsyncIOMotorClient, aids: list[int], query_id: str) -> None:
    all_cids = set()
    for aid in aids[:5]:  
        try:
            bioassay = await get_bioassay(db, aid)
        except:
            bioassay = await download_bioassay(db, aid)
        for cid in bioassay.get("compounds", [])[:5]:
            try:
                compound = await get_compound(db, cid)
            except:
                compound = await download_compound(db, cid)
            all_cids.add(cid)
    # Una vez terminado, actualizar la query con la lista de cids
    await update_query_compounds(db, query_id, list(all_cids))
        
        
            






