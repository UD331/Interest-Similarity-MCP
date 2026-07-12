from typing import List
from fastmcp import FastMCP
import requests
from config import TASTEDIVE_API_KEY
from models import TasteDive

tastedive_server = FastMCP("Tastedive MCP") # server

@tastedive_server.tool(
        description="""Get similar items limited to types belonging to 
        'music', 'movie', 'show', 'book', 'game' regarding the given popular interest from 
        Tastedive API based on a name and limit"""
    )
def get_recommendations(name, limit=3)-> List[TasteDive]:
    url = "https://tastedive.com/api/similar"
    types = ['music', 'movie', 'show', 'book', 'game']
    recommendations = []
    for t in types:
        params = {
            "q": name, "limit": limit,
            "k": TASTEDIVE_API_KEY, "info": 1,  # include descriptions
            "type": t
        }
        try:
            res = requests.get(url, params=params, timeout=(5, 10))  # (connect timeout, read timeout)
            res.raise_for_status()  # Raise an exception for HTTP errors

            for values in res.json()['similar']['results']:
                recommendation = TasteDive
                recommendation.name = values['name']
                recommendation.type = t
                recommendation.description = values['description']
                recommendations.append(recommendation)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching recommendations for type '{t}': {e}")
            
    return recommendations

