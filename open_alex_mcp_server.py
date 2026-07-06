from fastmcp import FastMCP
import requests
from config import OPEN_ALEX_API_KEY

open_alex_server = FastMCP("OpenAlex MCP") # server

@open_alex_server.tool
def semantic_search_entity(concept:str):    
    url = f"https://api.openalex.org/works?search.semantic={concept}&sort=cited_by_count:desc&per_page=10"
    
    headers = {
        'User-Agent': 'InterestAgent/1.0'
    }
    params = {
        "api_key": OPEN_ALEX_API_KEY
    }
    res = requests.get(url, params=params, headers=headers, allow_redirects=True)
    return res.json()['results']

@open_alex_server.tool
def direct_entity_search(article_id:str):
    url = f"https://api.openalex.org/works/{article_id}"
    
    headers = {
        'User-Agent': 'InterestAgent/1.0'
    }
    params = {
        "api_key": OPEN_ALEX_API_KEY
    }
    res = requests.get(url, params=params, headers=headers, allow_redirects=True)
    return res.json()

work = (direct_entity_search("W602506921"))

if work:
    print({
        "title": work["display_name"],
        "year": work["publication_year"],
        "citations": work["cited_by_count"],
        "doi": work.get("doi"),
        "id": work["id"].split('.org/')[1],
    })