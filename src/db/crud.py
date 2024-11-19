from sqlalchemy.orm import Session
from sqlalchemy.sql import func 
from src.db import models, schemas
from src.db.models import Contract 

# 사용자 CRUD
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password  # 비밀번호는 이미 해싱된 것으로 가정
    db_user = models.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 계약/구독 CRUD
def create_contract(db: Session, contract: schemas.ContractCreate, user_id: int):
    db_contract = models.Contract(**contract.dict(), user_id=user_id)
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def get_contract_by_id(db: Session, contract_id: int):
    return db.query(models.Contract).filter(models.Contract.id == contract_id).first()

def get_contracts_by_user(db: Session, user_id: int):
    return db.query(models.Contract).filter(models.Contract.user_id == user_id).all()

def delete_contract(db: Session, contract_id: int):
    contract = get_contract_by_id(db, contract_id)
    if contract:
        db.delete(contract)
        db.commit()
    return contract
#월간 구독료 총합
def get_total_monthly_cost(db: Session, user_id: int) -> float:
    """
    특정 사용자의 모든 계약의 monthly_cost 합산 반환.
    """
    total_cost = db.query(func.sum(Contract.monthly_cost)).filter(Contract.user_id == user_id).scalar()
    return total_cost or 0.0

# 알림 CRUD
def create_notification(db: Session, notification: schemas.NotificationBase):
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notifications_by_contract(db: Session, contract_id: int):
    return db.query(models.Notification).filter(models.Notification.contract_id == contract_id).all()

def mark_notification_as_sent(db: Session, notification_id: int):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if notification:
        notification.status = True
        db.commit()
        db.refresh(notification)
    return notification