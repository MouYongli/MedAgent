from pydantic import BaseModel


class RetrieverRequest(BaseModel):
    query: str
