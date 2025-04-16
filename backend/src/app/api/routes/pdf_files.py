# backend/app/routers/file_manager.py
import os
import os.path as osp
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter()

# File storage directory (the `data` folder is located at the backend root)
HERE = osp.dirname(osp.abspath(__file__))
BASE_DIR = osp.join(HERE, "..", "..", "..", "..")
FILE_DIR = osp.join(BASE_DIR, "data")
os.makedirs(FILE_DIR, exist_ok=True)

def get_file_path(filename: str) -> str:
    return osp.join(FILE_DIR, filename)

@router.get("/", response_model=List[str])
async def list_files():
    """
    List all .pdf filenames
    """
    files = [f for f in os.listdir(FILE_DIR) if f.endswith(('.pdf'))]
    return files

@router.post("/", status_code=HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a .pdf file
    """
    if not file.filename.endswith(('.pdf')):
        raise HTTPException(status_code=400, detail="Only .pdf files are allowed")
    file_path = get_file_path(file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"filename": file.filename, "message": "Upload successful"}

@router.get("/{filename}")
async def get_file(filename: str):
    """
    Retrieve the specified file's contents (for editing)
    """
    file_path = get_file_path(filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)

@router.put("/{filename}")
async def update_file(filename: str, content: str = None):
    """
    Update the contents of a specified file
    """
    file_path = get_file_path(filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content or "")
    return {"message": "Update successful", "filename": filename}

@router.delete("/{filename}")
async def delete_file(filename: str):
    """
    Delete a specified file
    """
    file_path = get_file_path(filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(file_path)
    return {"message": "Deletion successful", "filename": filename}
