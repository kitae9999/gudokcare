# src/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from src.db.database import engine
from src.db.models import Contract
from sqlalchemy import and_
import logging
from src.db import models
from src.db.crud import renew_contract

# 세션 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_and_renew_contracts():
    db = SessionLocal()
    try:
        # 자동 갱신이 설정된 모든 계약 가져오기
        contracts = db.query(models.Contract).filter(
            models.Contract.auto_renew == True
        ).all()

        for contract in contracts:
            if contract.end_date <= datetime.today().date():
                renew_contract(db, contract.id)
    finally:
        db.close()

def delete_expired_contracts():
    """
    자동 갱신이 설정되지 않았고, 만료일이 현재 날짜보다 이전인 계약을 삭제합니다.
    """
    db = SessionLocal()
    try:
        today = datetime.today().date()
        expired_contracts = db.query(Contract).filter(
            and_(
                Contract.auto_renew == False,
                Contract.end_date < today
            )
        ).all()

        for contract in expired_contracts:
            # 관련된 데이터 삭제 (사용 기록, 사용 패턴 등)
            db.query(models.UsagePattern).filter(models.UsagePattern.contract_id == contract.id).delete()
            db.query(models.UsageAnalysis).filter(models.UsageAnalysis.contract_id == contract.id).delete()
            db.query(models.UsageLog).filter(models.UsageLog.contract_id == contract.id).delete()

            # 계약 삭제
            db.delete(contract)
            logging.info(f"Contract {contract.id} deleted due to expiration.")

        db.commit()
    except Exception as e:
        logging.error(f"Error deleting expired contracts: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_contracts, 'interval', days=1, next_run_time=datetime.now())
    scheduler.add_job(check_and_renew_contracts, 'interval', days=1, next_run_time=datetime.now())
    scheduler.start()