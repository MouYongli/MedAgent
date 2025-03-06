# backend/app/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import pdf_files

app = FastAPI(
    title="PDF File Manager",
    description="通过 FastAPI 提供文件上传、查询和删除等功能。",
    version="0.1.0"
)

# 允许跨域，以便前端在不同端口访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境下允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册文件管理路由
app.include_router(pdf_files.router, prefix="/api/knowledge/pdf", tags=["files"])

# 启动服务：可以通过 `python app/main.py` 或 `uvicorn app.main:app --reload` 运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)