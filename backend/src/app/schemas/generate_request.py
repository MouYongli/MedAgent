from pydantic import BaseModel


class GenerateRequest(BaseModel):
    query: str
