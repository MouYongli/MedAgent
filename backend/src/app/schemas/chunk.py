from pydantic import BaseModel


class Chunk(BaseModel):
    page_content: str
    book_name: str
    page_number: str
    id: int

    class Config:
        orm_mode = True
