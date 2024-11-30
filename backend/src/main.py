#src/main.py


from fastapi import FastAPI
from src.api.routes import auth, contracts
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.scheduler import start_scheduler
app = FastAPI(title="구독케어 (SubscriptionCare)")

# CORS 설정
origins = [
    "http://localhost:5173",  # Svelte 개발 서버
    "http://127.0.0.1:5173",  # Svelte 개발 서버 (IP 주소)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])

start_scheduler()