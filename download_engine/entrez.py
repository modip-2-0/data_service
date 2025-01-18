import requests

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

async def search_bioassays(query: str) -> list[int]:
    url = f"{BASE_URL}/?db=pcassay&term={query}[PTN]&retmode=json"
    response = requests.get(url)
    aid_list = response.json()["esearchresult"]["idlist"]
    return [int(aid) for aid in aid_list]

