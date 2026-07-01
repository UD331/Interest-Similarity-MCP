from fastmcp import FastMCP
import requests

server = FastMCP("Wikidata MCP") # server

def search_entity(label:str, lang="en"):
    # this one is to get the QID & other high-level of the entity from Wikidata
    # which can then be used for relationship search after
    # Needs the label to actually be searchable entity
    url = "https://www.wikidata.org/w/api.php"
    headers = {
        'User-Agent': 'InterestAgent/1.0'
    }
    params = {
        "action": "wbsearchentities",
        "search": label,
        "language": lang,
        "format": "json"
    }
    res = requests.get(url, params=params, headers=headers)
    return res.json()["search"][0]["id"]

def get_wikidata_relationships(qid: str):
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
        res = requests.get(url, params={'query': sparql_query, 'format': 'json'}, headers=headers)
        data = res.json()
        
        relationships = []
        for row in data['results']['bindings']:
            relationships.append({
                "relationship_type": row['propertyLabel']['value'],
                "item_name": row['relatedItemLabel']['value'],
                "item_qid": row['relatedItem']['value'].split('/')[-1]
            })
        return relationships
    except Exception as e:
        print(f"Error fetching Wikidata relationships: {e}")
        return []

# Example Usage:
radiohead_qid = search_entity("Radiohead") # Q11680
print(get_wikidata_relationships(radiohead_qid))

#print(search_entity("Python (programming language)"))