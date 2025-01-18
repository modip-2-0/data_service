import requests

from core.db import AsyncIOMotorClient
from crud.compound import Compound, CompoundCreate, create_compound



BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid"

async def download_compound(db: AsyncIOMotorClient, cid: int) -> Compound:
    
    url = f"{BASE_URL}/{cid}/property/Title/JSON"
    response = requests.get(url)
    data = response.json()["PropertyTable"]["Properties"][0]     

    compound = CompoundCreate(
        cid = cid,
        name = data["Title"]             
    ) 

    return await create_compound(db, compound)

