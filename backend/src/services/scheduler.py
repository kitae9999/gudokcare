from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.db.models import Contract
from src.db.crud import renew_contract
from datetime import date

def check_and_renew_contracts():
    db: Session = SessionLocal()
    today = date.today()

    # 만료일이 지난 계약 갱신
    contracts = db.query(Contract).filter(Contract.end_date <= today, Contract.auto_renew == True).all()
    for contract in contracts:
        renew_contract(db, contract.id)
    db.close()

# 스케줄러 초기화
scheduler = BackgroundScheduler()
scheduler.add_job(check_and_renew_contracts, 'interval', days=1)  # 하루에 한 번 실행
scheduler.start()