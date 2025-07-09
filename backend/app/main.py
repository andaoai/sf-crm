from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import companies, talents, communications

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM System API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(talents.router, prefix="/api/talents", tags=["talents"])
app.include_router(communications.router, prefix="/api/communications", tags=["communications"])

@app.get("/")
def read_root():
    return {"message": "CRM System API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
