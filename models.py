from pydantic import BaseModel

class TasteDive(BaseModel):
    name: str
    type: str
    description: str