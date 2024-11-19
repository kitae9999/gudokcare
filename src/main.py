from fastapi import FastAPI
from src.api.routes import auth, contracts
from src.db.database import Base, engine

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)

app = FastAPI(title="구독케어 (SubscriptionCare)")

# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])