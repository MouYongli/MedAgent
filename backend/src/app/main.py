from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import pdf_files

app = FastAPI(
    title="PDF File Manager",
    description="Provides functionalities such as file upload, retrieval, and deletion through FastAPI.",
    version="0.1.0"
)

# Enable CORS to allow frontend access from different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register file management routes
app.include_router(pdf_files.router, prefix="/api/knowledge/pdf", tags=["files"])

# Start the service: can be run using `python app/main.py` or `uvicorn app.main:app --reload`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
