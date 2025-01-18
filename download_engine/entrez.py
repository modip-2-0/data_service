"""
Entrez API client module for PubChem bioassay searches.

This module provides functionality to search PubChem bioassays using the 
NCBI E-utilities API (Entrez).
"""

import requests

# Base URL for NCBI Entrez E-utilities API
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

async def search_bioassays(query: str) -> list[int]:
    """
    Search PubChem bioassays using a text query.

    Makes an asynchronous request to PubChem's Entrez API to find bioassays
    matching the provided search term.

    Args:
        query (str): Search term to find relevant bioassays

    Returns:
        List[int]: List of PubChem Assay IDs (AIDs) matching the query

    Raises:
        requests.RequestException: If the API request fails
        KeyError: If the response JSON structure is invalid
    """
    url = f"{BASE_URL}/?db=pcassay&term={query}[PTN]&retmode=json"
    response = requests.get(url)
    response.raise_for_status()
    
    aid_list = response.json()["esearchresult"]["idlist"]
    return [int(aid) for aid in aid_list]