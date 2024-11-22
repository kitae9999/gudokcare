from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from src.services.notification_service import send_firebase_notifications
from src.db.database import SessionLocal
from src.api.routes import auth, contracts
from src.services.scheduler import scheduler

app = FastAPI(title="구독케어 (SubscriptionCare)")

# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])

# 스케줄러 설정
scheduler = BackgroundScheduler()

def notification_task():
    db = SessionLocal()
    send_firebase_notifications(db)
    db.close()

# 매일 오전 9시에 알림 확인
scheduler.add_job(notification_task, 'cron', hour=9, minute=0)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()