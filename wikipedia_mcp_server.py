from fastmcp import FastMCP
import wikipediaapi
import asyncio
import re
import aiohttp

wikipedia_server = FastMCP("Wikipedia MCP") # server

wiki = wikipediaapi.AsyncWikipedia(
    user_agent="Curiostiy Agent/1.0",
    language="en"
)

async def get_page_info(query: str = ""):
    # this is lazy loading; until we search something like page.exists or something, nothing is there
    wiki_page = wiki.page(query)
    page_exists = await wiki_page.exists()
    wiki_info = {
        "exists": page_exists,
        "summary": None,
    }
    if page_exists:
        summary = await wiki_page.summary
        links = await wiki_page.links
        SKIP_PREFIXES = [
            "Wikipedia:", "Help:", "Template:", "File:",
            "Portal:", "Special:", "Talk:", "Category:",
            "List of",   
        ]

        filtered_links = [l for l in links if not any(l.startswith(p) for p in SKIP_PREFIXES)]
        filtered_links = set(filtered_links)
        categories = await wiki_page.categories
        categories_filtered = filtered = [
            s for s in list(categories.keys())
            if not re.search(r'articles?', s, re.IGNORECASE)
        ]
        wiki_info.update({
            "summary": summary,
        })
    return wiki_info

async def get_clean_section_links(title: str):
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
            
            # ns: 0 means "Main Namespace" (encyclopedic articles). 
            # This automatically drops Categories, Talk pages, and Help links.
            clean_links = [
                link["*"] for link in raw_links 
                if link["ns"] == 0 and "exists" in link
            ]
            
            return clean_links

@wikipedia_server.tool
async def search_for_possible_articles(query:str):
    # this one is for letting LLM search for possible articles and then selecting from there
    # which one is actually relevant
    results = await wiki.search(query, limit=5)
    options = []
    for title, pages in results.pages.items():
        options.append(title)
    return options

print(asyncio.run(get_clean_section_links("Radiohead")))