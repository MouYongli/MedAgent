from pydantic import BaseModel


class GenerateResponse(BaseModel):
    result: str
