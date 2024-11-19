from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.database import Base

# 사용자 모델
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    contracts = relationship("Contract", back_populates="user")


# 계약/구독 모델
class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_name = Column(String, nullable=False)
    monthly_cost = Column(Float, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    auto_renew = Column(Boolean, default=False)
    notes = Column(String, nullable=True)

    user = relationship("User", back_populates="contracts")
    notifications = relationship("Notification", back_populates="contract")


# 알림 모델
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notification_date = Column(Date, nullable=False)
    status = Column(Boolean, default=False)  # False: 미발송, True: 발송 완료

    contract = relationship("Contract", back_populates="notifications")