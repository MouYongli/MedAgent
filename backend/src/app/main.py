from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models.components.component_registry ## MUST BE KEPT HERE!!

from app.api.routes import pdf_files, vector_database
from app.routes import chat, workflow

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
fast_app.include_router(pdf_files.router, prefix="/api/knowledge/pdf", tags=["files"])
fast_app.include_router(vector_database.router, prefix="/api/knowledge/vector")
fast_app.include_router(chat.router, prefix="/api/chat")
fast_app.include_router(workflow.router, prefix="/api/workflow")

# Start the service: Run with `python app/main.py` or `uvicorn app.main:app --reload`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:fast_app", host="0.0.0.0", port=8000, reload=True)
