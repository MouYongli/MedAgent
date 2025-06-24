from app.schemas.chunk import Chunk
from pydantic import BaseModel

# {
#     "query":"",
#     "chunks":[
#         {
#             "page_content":"The quick brown fox jumps over the lazy dog.",
#             "book_name":"example.txt",
#             "page_number":1,
#             "id":0


#         },
#         {
#             "page_content":"A journey of a thousand miles begins with a single step.",
#             "book_name":"Lao.txt",
#             "page_number":5,
#             "id":1
#         }
#     ],
#     "answer":"The quick brown fox jumps over the lazy dog. A journey of a thousand miles begins with a single step."
# }


class RetrieverResponse(BaseModel):
    query: str
    chunks: list[Chunk]
