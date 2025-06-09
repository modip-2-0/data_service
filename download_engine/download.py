"""
Download Engine Module

This module coordinates the download of bioassays and compounds from PubChem
based on search queries. It manages the download process and database storage.
"""

from core.db import AsyncIOMotorClient
from crud.bioassay import get_bioassay
from crud.compound import get_compound
from download_engine.entrez import search_bioassays
from download_engine.bioassay import download_bioassay
from download_engine.compound import download_compound

import logging

async def download(db: AsyncIOMotorClient, query: str) -> None:
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
    aids_list = await search_bioassays(query)

    print(f"Found {len(aids_list)} bioassays matching the query:")
    print(aids_list)    
  
    for aid in aids_list[:5]:
        try:            
            bioassay = await get_bioassay(db, aid)
        except:
            
            bioassay = await download_bioassay(db, aid)

            
            for cid in bioassay["compounds"][:5]:
                try:
                    
                    compound = await get_compound(db, cid)
                except:
                    
                    compound = await download_compound(db, cid)
                    
    return aids_list
        
        
            






