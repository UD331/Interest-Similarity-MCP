from fastmcp import FastMCP
import requests

conceptnet_server = FastMCP("Conceptnet MCP") # server

def get_concept(word, lang="en"):
    url = f"http://api.conceptnet.io/c/{lang}/{word}"
    res = requests.get(url).json()
    return res

def get_relation(word, relation, lang="en"):
    # relation e.g. "IsA", "UsedFor", "PartOf", "HasA", "CapableOf"
    url = f"http://api.conceptnet.io/query"
    params = {
        "node": f"/c/{lang}/{word}",
        "rel": f"/r/{relation}"
    }
    res = requests.get(url, params=params)
    return res.json()["edges"]

def relatedness(word1, word2, lang="en"):
    url = f"http://api.conceptnet.io/relatedness"
    params = {
        "node1": f"/c/{lang}/{word1}",
        "node2": f"/c/{lang}/{word2}"
    }
    res = requests.get(url, params=params)
    return res.json()["value"]  # float 0.0–1.0

