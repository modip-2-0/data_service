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



async def download(db: AsyncIOMotorClient, aids: list[int]) -> None:
   
  
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
                    

        
        
            






