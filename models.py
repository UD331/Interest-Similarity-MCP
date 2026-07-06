from pydantic import BaseModel

class TasteDive(BaseModel):
    name: str
    type: str
    description: str

class WikipediaPageInfo(BaseModel):
    exists: bool = False
    summary: str | None = None

class WikipediaSearchResult(BaseModel):
    title: str
