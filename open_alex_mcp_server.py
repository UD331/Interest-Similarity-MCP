from fastmcp import FastMCP
import requests
from config import OPEN_ALEX_API_KEY
from models import OpenAlexSearchResult

open_alex_server = FastMCP("OpenAlex MCP") # server

def undo_inverted_index(inverted_index):
    
    """
    The purpose of the function is to 'undo' and inverted index. It inputs an inverted index and
    returns the original string.
    """
    if not inverted_index:
        return ""
    #create empty lists to store uninverted index
    word_index = []
    words_unindexed = []
    
    #loop through index and return key-value pairs
    for k,v in inverted_index.items(): 
        for index in v: word_index.append([k,index])

    #sort by the index
    word_index = sorted(word_index, key = lambda x : x[1])
    
    #join only the values and flatten
    for pair in word_index:
        words_unindexed.append(pair[0])
    words_unindexed = ' '.join(words_unindexed)
    
    return(words_unindexed)

@open_alex_server.tool(
    description="""Perform a semantic search for research papers entities on OpenAlex based on
    our concept and return the top 10 results titles, ids, abstracts (if available), etc.
    sorted by relevance and citations"""
)
def semantic_search_entity(concept:str) -> list[OpenAlexSearchResult]:    
    url = f"https://api.openalex.org/works?search.semantic={concept}&sort=cited_by_count:desc&per_page=10"
    
    headers = {
        'User-Agent': 'InterestAgent/1.0'
    }
    params = {
        "api_key": OPEN_ALEX_API_KEY
    }
    res = requests.get(url, params=params, headers=headers, allow_redirects=True, timeout=(5, 10))  # (connect timeout, read timeout)
    search_results = []
    for work in res.json()['results']:
        search_result = OpenAlexSearchResult(
            title=work.get("display_name"),
            year=work.get("publication_year"),
            citations=work.get("cited_by_count"),
            similarity=work.get("relevance_score", -float('inf')),
            id=work.get("id").split('.org/')[1],
            abstract=undo_inverted_index(work.get("abstract_inverted_index", None))
        )
        search_results.append(search_result)
    return search_results

@open_alex_server.tool(
    description="""Perform a direct search for research paper based on OpenAlex article id on
    our concept and return the title, citations count, abstracts (if available), etc.
    sorted by relevance and citations"""
)
def direct_entity_search(article_id:str) -> OpenAlexSearchResult:
    url = f"https://api.openalex.org/works/{article_id}"
    
    headers = {
        'User-Agent': 'InterestAgent/1.0'
    }
    params = {
        "api_key": OPEN_ALEX_API_KEY
    }
    res = requests.get(url, params=params, headers=headers, allow_redirects=True, timeout=(5, 10))  # (connect timeout, read timeout)
    search_result = OpenAlexSearchResult(
        title=res.json().get("display_name"),
        year=res.json().get("publication_year"),
        citations=res.json().get("cited_by_count"),
        id=res.json().get("id").split('.org/')[1],
        abstract=undo_inverted_index(res.json().get("abstract_inverted_index", None))
    )
    return search_result


    