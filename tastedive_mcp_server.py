from typing import List
from fastmcp import FastMCP
import requests
from config import TASTEDIVE_API_KEY
from models import TasteDive



tastedive_server = FastMCP("Tastedive MCP") # server

@tastedive_server.tool
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

        res = requests.get(url, params=params)
        for values in res.json()['similar']['results']:
            recommendation = TasteDive
            recommendation.name = values['name']
            recommendation.type = t
            recommendation.description = values['description']
            recommendations.append(recommendation)
            
    return recommendations

