from firebase_admin import messaging
from sqlalchemy.orm import Session
from datetime import date, timedelta
from src.db.crud import get_contracts_for_notifications
from src.db.models import User

def send_firebase_notifications(db: Session):
    """
    Firebase Cloud Messaging을 사용하여 알림 전송
    """
    today = date.today()
    contracts = get_contracts_for_notifications(db, today)

    for contract in contracts:
        user = db.query(User).filter(User.id == contract.user_id).first()
        if user and user.email:
            # Firebase 메시지 구성
            message = messaging.Message(
                notification=messaging.Notification(
                    title="구독 만료 알림",
                    body=f"{contract.service_name}의 구독이 {contract.end_date}에 만료됩니다.",
                ),
                token=user.firebase_token,  # 사용자 디바이스 토큰
            )
            try:
                # 메시지 전송
                response = messaging.send(message)
                print(f"Successfully sent message: {response}")
            except Exception as e:
                print(f"Failed to send message: {e}")