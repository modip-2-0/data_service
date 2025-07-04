"""
Download Engine Module

This module coordinates the download of bioassays and compounds from PubChem
based on search queries. It manages the download process and database storage.
"""

from core.db import AsyncIOMotorClient
from crud.bioassay import get_bioassay
from crud.compound import get_compound
from download_engine.bioassay import download_bioassay
from download_engine.compound import download_compound



async def download(db: AsyncIOMotorClient, aids: str) -> None:
    """
    Downloads bioassays and their associated compounds based on a search query.

    Args:
        db (AsyncIOMotorClient): MongoDB client instance
        query (str): Search query for PubChem bioassays

    The function:
    1. Searches for bioassays matching the query
    2. Downloads each bioassay if not already in database
    3. Downloads the compounds associated with each bioassay
    """
   
  
    for aid in aids[:5]:
        try:            
            bioassay = await get_bioassay(db, aid)
        except:
            
            bioassay = await download_bioassay(db, aid)

            
            for cid in bioassay["compounds"][:5]:
                try:
                    
                    compound = await get_compound(db, cid)
                except:
                    
                    compound = await download_compound(db, cid)
                    

        
        
            






