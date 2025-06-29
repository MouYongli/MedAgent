
# backend/app/app.py

from app.dependencies.graph_retriever import get_graph_retriever
from app.dependencies.tf_matrix import load_tf_matrix
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import pdf_files  # Import pdf_files
from app.api.routes import chat  # Import chat
from app.routes import generator  # Import generator (internal)
from app.routes import retriever  # Import retriever (internal)
from app.dependencies.pinecone_driver import get_pinecone_index
from app.dependencies.vector_retriever import get_vector_retriever
from app.dependencies.para_chunks import load_para_chunks


fast_app = FastAPI(
    title="PDF File Manager",
    description="Provides file upload, query, and deletion functionalities via FastAPI.",
    version="0.1.0"
)

# Allow cross-origin requests so that the frontend can access the API from a different port
fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register file management routes

app.include_router(pdf_files.router, prefix="/api/knowledge/pdf", tags=["files"])
# Register chat routes
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# Register internal generator routes (not exposed to public API) for testing
app.include_router(
    generator.router, prefix="/internal/generate", tags=["internal-generate"]
)
app.include_router(
    retriever.router, prefix="/internal/retrieve", tags=["internal-retrieve"]
)


@app.on_event("startup")
async def load_singletons():
    # Initialize Pinecone index singleton
    # get_pinecone_index()
    # Initialize VectorRetriever singleton (with default top_k)
    get_vector_retriever()

    load_para_chunks()

    load_tf_matrix()

    get_graph_retriever()


# Start the service: can be run with `python app/main.py` or `uvicorn app.main:app --reload`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

