from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from src.services.notification_service import send_firebase_notifications
from src.db.database import SessionLocal

app = FastAPI(title="구독케어 (SubscriptionCare)")

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