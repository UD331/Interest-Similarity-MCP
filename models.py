from pydantic import BaseModel

class TasteDive(BaseModel):
    name: str
    type: str
    description: str

class WikipediaPageInfo(BaseModel):
    exists: bool = False
    summary: str | None = None

class OpenAlexSearchResult(BaseModel):
    title: str
    year: int
    citations: int
    similarity: float = -float('inf') # this is to differentiate between direct vs semantic search results
    id: str
    abstract: str | None = None

class WikidataRelationship(BaseModel):
    relationship_type: str
    name: str
    qid: str

class WikidataEntity(BaseModel):
    qid: str
    name: str
    description: str | None = None