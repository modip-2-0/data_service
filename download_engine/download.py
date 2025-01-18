from core.db import AsyncIOMotorClient
from crud.bioassay import Bioassay, get_bioassay
from crud.compound import Compound, get_compound

from download_engine.entrez import search_bioassays
from download_engine.bioassay import download_bioassay
from download_engine.compound import download_compound


async def download(db: AsyncIOMotorClient, query: str):

    aids_list = await search_bioassays(query)

    for aid in aids_list:
        bioassay: Bioassay
        try:
            bioassay = await get_bioassay(db, aid)
        except:
            bioassay = await download_bioassay(db, aid)

            for cid in bioassay["compounds"][:5]:
                compound: Compound
                try:
                    compound = await get_compound(db, cid)
                except:
                    compound = await download_compound(db, cid)
        
        
            






