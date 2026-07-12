from fastmcp import FastMCP
import wikipediaapi
import asyncio
import aiohttp
from models import WikipediaPageInfo

wikipedia_server = FastMCP("Wikipedia MCP") # server

wiki = wikipediaapi.AsyncWikipedia(
    user_agent="Curiostiy Agent/1.0",
    language="en"
)

@wikipedia_server.tool(
    description="Get if a Wikipedia page exists and if so, its summary."
)
async def get_page_info(query: str = "") -> WikipediaPageInfo:
    # this is lazy loading; until we search something like page.exists or something, nothing is there
    wiki_page = wiki.page(query)
    page_exists = await wiki_page.exists()
    wiki_info = WikipediaPageInfo(exists=page_exists, summary=None)
    if page_exists:
        summary = await wiki_page.summary
        wiki_info.summary = summary
    return wiki_info

@wikipedia_server.tool(
    description="""Get clean links from a Wikipedia page introduction section that be used for
    further exploration of related topics. This function filters out non-encyclopedic links such
    as categories, talk pages, and help links."""
)
async def get_clean_section_links(title: str) -> list[str]:
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": title,
        "section": "0",  # 0 is the introduction
        "prop": "links", # Tells Wikipedia to return a JSON array of links, NOT HTML
        "format": "json"
    }
    headers = {'User-Agent': 'InterestAgent/1.0'}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            data = await response.json()
            if "parse" not in data:
                return []
            raw_links = data["parse"]["links"]
            
            # This automatically drops Categories, Talk pages, and Help links.
            SKIP_PREFIXES = [
                "Wikipedia:", "Help:", "Template:", "File:",
                "Portal:", "Special:", "Talk:", "Category:",
                "List of",   
            ]

            # ns: 0 means "Main Namespace" (encyclopedic articles). 
            clean_links = [
                link["*"] for link in raw_links 
                if link["ns"] == 0 and "exists" in link
            ]
            filtered_links = [l for l in clean_links if not any(l.startswith(p) for p in SKIP_PREFIXES)]
            return filtered_links

@wikipedia_server.tool(
    description="""Search for possible Wikipedia articles based on a  name. This function returns
    a list of article titles that match the search query, allowing for targeted search of the exact page
    we want."""
)
async def search_for_possible_articles(query:str) -> list[str]:
    # this one is for letting LLM search for possible articles and then selecting from there
    # which one is actually relevant- i.e. searching Python and then deciding between the proramming language 
    # and the snake
    results = await wiki.search(query, limit=5)
    options = []
    print(results.pages)
    for title, pages in results.pages.items():
        options.append(title)
    return options

