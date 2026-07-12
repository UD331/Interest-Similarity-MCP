from fastmcp import FastMCP
from models import WikidataRelationship
import requests

wikidata_server = FastMCP("Wikidata MCP") # server

@wikidata_server.tool(
    description="""Search for a Wikidata entity by its label and gets its QID (unique identifier)
    for further exploration of relationships."""
)
def search_entity(label:str, lang="en") -> str:
    # this one is to get the QID & other high-level of the entity from Wikidata
    # which can then be used for relationship search after
    # Needs the label to actually be searchable entity
    url = "https://www.wikidata.org/w/api.php"
    headers = {
        'User-Agent': 'CuriosityEngine/1.0'
    }
    params = {
        "action": "wbsearchentities",
        "search": label,
        "language": lang,
        "format": "json"
    }
    res = requests.get(url, params=params, headers=headers, timeout=(5, 10))  # (connect timeout, read timeout)
    return res.json()["search"][0]["id"]

@wikidata_server.tool(
    description="""Get relationships for a Wikidata entity by its QID including relationship types and
    related items name and QID."""
)
def get_wikidata_relationships(qid: str) -> list[WikidataRelationship]:
    url = "https://query.wikidata.org/sparql"
    headers = {
        'User-Agent': 'InterestAgent/1.0',
        'Accept': 'application/json'
    }
    
    # SPARQL query fetching specific properties and their human-readable labels
    sparql_query = f"""
    SELECT ?propertyLabel ?relatedItem ?relatedItemLabel WHERE {{
      VALUES ?prop {{ wdt:P136 wdt:P941 wdt:P921 wdt:P135 wdt:P4969 wdt:P144 wdt:P179 wdt:P4878 wdt:P31}}
      wd:{qid} ?prop ?relatedItem .
      
      # Fetch the human-readable labels for the properties and items
      ?property wikibase:directClaim ?prop .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """
    
    try:
        res = requests.get(url, params={'query': sparql_query, 'format': 'json'}, headers=headers, timeout=(5, 10))
        data = res.json()
        
        relationships = []
        for row in data['results']['bindings']:
            relationships.append(WikidataRelationship(
                relationship_type=row['propertyLabel']['value'],
                name=row['relatedItemLabel']['value'],
                qid=row['relatedItem']['value'].split('/')[-1]
            ))
        return relationships
    except Exception as e:
        print(f"Error fetching Wikidata relationships: {e}")
        return []
