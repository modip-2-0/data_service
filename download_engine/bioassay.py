import requests

from core.db import AsyncIOMotorClient
from crud.bioassay import Bioassay, BioassayCreate, create_bioassay



BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid"

async def download_bioassay(db: AsyncIOMotorClient, aid: int) -> Bioassay:
    
    summary_url = f"{BASE_URL}/{aid}/summary/JSON"
    summary_response = requests.get(summary_url)
    summary = summary_response.json()["AssaySummaries"]["AssaySummary"][0]

    data_url = f"{BASE_URL}/{aid}/concise/JSON"
    data_response = requests.get(data_url)    
    data = data_response.json()["Table"]["Row"]
    cids = set()
    cids.update([int(row["Cell"][2]) for row in data])

    bioassay = BioassayCreate(
        aid = aid,
        name = summary["Name"],
        description = summary["Description"],
        compounds = list(cids)
    ) 

    return await create_bioassay(db, bioassay)




    




