#src/db/models.py

from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from src.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    contracts = relationship("Contract", back_populates="user")

class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_name = Column(String, nullable=False)
    monthly_cost = Column(Float, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    auto_renew = Column(Boolean, default=False)
    renewal_period = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    used_today = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="contracts")
    usage_logs = relationship("UsageLog", back_populates="contract")

    

    

class UsageLog(Base):
    __tablename__ = "usage_logs"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    date = Column(Date, nullable=False)
    used = Column(Boolean, default=False, nullable=False)

    contract = relationship("Contract", back_populates="usage_logs")

class UsageAnalysis(Base):
    __tablename__ = "usage_analysis"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    total_days = Column(Integer, nullable=False)  # 구독 기간 동안 총 일수
    used_days = Column(Integer, nullable=False)  # 실제 사용한 일수
    usage_rate = Column(Float, nullable=False)  # 사용 비율 (used_days / total_days)
    cost_per_use = Column(Float, nullable=True)  # 사용 1회당 비용
    created_at = Column(DateTime, default=func.now(), nullable=False)

    contract = relationship("Contract")
    user = relationship("User")

class UsagePattern(Base):
    __tablename__ = "usage_patterns"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_used_days = Column(Integer, default=0, nullable=False)  # 총 사용한 날
    daily_average = Column(Float, default=0.0, nullable=True)  # 하루 평균 사용 횟수
    weekly_average = Column(Float, default=0.0, nullable=True)  # 주간 평균 사용 횟수
    monthly_average = Column(Float, default=0.0, nullable=True)  # 월간 평균 사용 횟수
    last_used_date = Column(Date, nullable=True)  # 마지막으로 사용한 날짜
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    most_used_weekday = Column(String)  # 주로 사용하는 요일 추가

    contract = relationship("Contract")
    user = relationship("User")