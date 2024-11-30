#src/db/crud.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.db import models, schemas
from src.db.models import Contract, UsageLog
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

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
    """
    새로운 계약(구독)을 생성하고 월별 데이터를 업데이트합니다.
    """
    if contract.end_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="만료일은 현재 날짜보다 이후여야 합니다."
        )
    # crud.py의 create_contract 함수에서 추가
    if contract.end_date < contract.start_date:
        raise HTTPException(
            status_code=400,
            detail="만료일은 시작일보다 이후여야 합니다."
        )
    renewal_period = (contract.end_date - contract.start_date).days
    db_contract = Contract(
        user_id=user_id,
        service_name=contract.service_name,
        monthly_cost=contract.monthly_cost,
        start_date=contract.start_date,
        end_date=contract.end_date,
        auto_renew=contract.auto_renew,
        renewal_period=renewal_period,
        used_today=False,
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)

    return db_contract


def get_contract_by_id(db: Session, contract_id: int):
    return db.query(models.Contract).filter(models.Contract.id == contract_id).first()

def get_contracts_by_user(db: Session, user_id: int):
    return db.query(models.Contract).filter(models.Contract.user_id == user_id).all()

def delete_contract(db: Session, contract_id: int):
    """
    특정 계약을 삭제하기 전에 관련 데이터를 정리합니다.
    """
    # 참조 데이터 삭제
    db.query(models.UsagePattern).filter(models.UsagePattern.contract_id == contract_id).delete()
    db.query(models.UsageAnalysis).filter(models.UsageAnalysis.contract_id == contract_id).delete()
    db.query(models.UsageLog).filter(models.UsageLog.contract_id == contract_id).delete()

    # 계약 삭제
    contract = get_contract_by_id(db, contract_id)
    if contract:
        db.delete(contract)
        db.commit()

    return {"message": f"Contract {contract_id} and related data deleted successfully"}

def renew_contract(db: Session, contract_id: int):
    """
    특정 계약의 종료일을 갱신합니다.
    - 계약이 자동 갱신 설정(auto_renew)인 경우에만 동작.
    - 갱신 주기(renewal_period)가 설정되어 있어야 함.
    """
    # 계약 정보 가져오기
    contract = db.query(Contract).filter(Contract.id == contract_id).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # 자동 갱신 설정 및 갱신 주기 확인
    if not contract.auto_renew or not contract.renewal_period:
        raise HTTPException(status_code=400, detail="Contract cannot be renewed")
    
    # 갱신 처리: 종료일을 갱신 주기만큼 연장
    contract.start_date = contract.end_date
    contract.end_date = contract.end_date + timedelta(days=contract.renewal_period)

    # 데이터베이스 커밋
    db.commit()
    db.refresh(contract)

    # 갱신된 기간에 맞게 사용 분석 및 패턴 데이터 업데이트
    reset_usage_analysis_and_pattern(db, contract_id)

    return contract

def log_usage(db: Session, contract_id: int, used: bool, usage_date: date):
    """
    특정 날짜의 사용 기록을 추가하거나 삭제합니다.
    """
    existing_log = db.query(UsageLog).filter(
        UsageLog.contract_id == contract_id,
        UsageLog.date == usage_date
    ).first()

    if used:
        if existing_log:
            existing_log.used = True  # 혹시나 기존에 False로 되어 있을 수 있으므로
        else:
            new_log = UsageLog(contract_id=contract_id, date=usage_date, used=True)
            db.add(new_log)
    else:
        if existing_log:
            db.delete(existing_log)  # 사용 기록 삭제
        # 사용 기록이 없으면 아무 작업도 하지 않음

    db.commit()

    # 사용 분석 및 패턴 데이터 업데이트
    update_usage_analysis(db, contract_id)
    update_usage_pattern(db, contract_id)

def calculate_used_days(db: Session, contract_id: int):
    """
    사용 일수를 반환합니다.
    """
    used_days = db.query(func.count()).filter(
        UsageLog.contract_id == contract_id,
        UsageLog.used == True
    ).scalar()

    return used_days

# update_usage_analysis 수정
def update_usage_analysis(db: Session, contract_id: int):
    """
    계약의 효율성 분석 데이터를 업데이트합니다.
    """
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        return None

    # 갱신된 기간에 해당하는 사용 기록 가져오기
    usage_logs = db.query(UsageLog).filter(
        UsageLog.contract_id == contract_id,
        UsageLog.date >= contract.start_date,  # 갱신된 시작일 이후 데이터만 포함
        UsageLog.date <= contract.end_date     # 갱신된 종료일까지 데이터만 포함
    ).all()

    total_days = (contract.end_date - contract.start_date).days if contract.end_date else 0
    used_days = sum(1 for log in usage_logs if log.used)

    usage_rate = used_days / total_days if total_days else 0
    cost_per_use = contract.monthly_cost / used_days if used_days else None

    analysis = db.query(models.UsageAnalysis).filter(models.UsageAnalysis.contract_id == contract_id).first()
    if analysis:
        analysis.total_days = total_days
        analysis.used_days = used_days
        analysis.usage_rate = usage_rate
        analysis.cost_per_use = cost_per_use
    else:
        new_analysis = models.UsageAnalysis(
            user_id=contract.user_id,
            contract_id=contract_id,
            total_days=total_days,
            used_days=used_days,
            usage_rate=usage_rate,
            cost_per_use=cost_per_use
        )
        db.add(new_analysis)

    db.commit()

def update_usage_pattern(db: Session, contract_id: int):
    """
    갱신된 계약 기간을 기준으로 사용 기록을 분석하고 패턴 데이터를 저장합니다.
    """
    # 계약 정보 가져오기
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        return

    # 갱신된 기간 내 사용 기록 가져오기
    usage_logs = db.query(UsageLog).filter(
        UsageLog.contract_id == contract_id,
        UsageLog.date >= contract.start_date,
        UsageLog.date <= contract.end_date
    ).all()

    if not usage_logs:
        # 사용 기록이 없으면 패턴 데이터 초기화 또는 생성
        pattern = db.query(models.UsagePattern).filter(models.UsagePattern.contract_id == contract_id).first()
        if pattern:
            pattern.total_used_days = 0
            pattern.daily_average = 0
            pattern.weekly_average = 0
            pattern.monthly_average = 0
            pattern.last_used_date = None
            pattern.most_used_weekday = None  # 초기화
        else:
            db.add(models.UsagePattern(
                contract_id=contract_id,
                user_id=contract.user_id,
                total_used_days=0,
                daily_average=0,
                weekly_average=0,
                monthly_average=0,
                last_used_date=None,
                most_used_weekday=None
            ))
        db.commit()
        return

    # 사용 기록 분석
    total_used_days = sum(1 for log in usage_logs if log.used)
    total_days = (contract.end_date - contract.start_date).days if contract.end_date else 0
    daily_average = total_used_days / total_days if total_days else 0
    weekly_average = total_used_days / (total_days / 7) if total_days >= 7 else 0
    monthly_average = total_used_days / (total_days / 30) if total_days >= 30 else 0
    last_used_date = max(log.date for log in usage_logs if log.used)

    # 요일별 사용 횟수 계산
    from collections import Counter

    weekdays = [log.date.strftime('%A') for log in usage_logs if log.used]
    weekday_counts = Counter(weekdays)

    if weekday_counts:
        most_used_weekday = weekday_counts.most_common(1)[0][0]
    else:
        most_used_weekday = None

    # 패턴 데이터 업데이트 또는 생성
    pattern = db.query(models.UsagePattern).filter(models.UsagePattern.contract_id == contract_id).first()
    if pattern:
        pattern.total_used_days = total_used_days
        pattern.daily_average = daily_average
        pattern.weekly_average = weekly_average
        pattern.monthly_average = monthly_average
        pattern.last_used_date = last_used_date
        pattern.most_used_weekday = most_used_weekday  # 업데이트
    else:
        new_pattern = models.UsagePattern(
            contract_id=contract_id,
            user_id=contract.user_id,
            total_used_days=total_used_days,
            daily_average=daily_average,
            weekly_average=weekly_average,
            monthly_average=monthly_average,
            last_used_date=last_used_date,
            most_used_weekday=most_used_weekday  # 추가
        )
        db.add(new_pattern)

    db.commit()


def get_usage_analysis(db: Session, user_id: int):
    analysis_data = db.query(models.UsageAnalysis).filter(models.UsageAnalysis.user_id == user_id).all()

    result = []
    for analysis in analysis_data:
        contract = db.query(models.Contract).filter(models.Contract.id == analysis.contract_id).first()
        if not contract:
            continue

        result.append({
            "contract_id": analysis.contract_id,
            "service_name": contract.service_name,
            "total_days": analysis.total_days,
            "used_days": analysis.used_days,
            "usage_percentage": analysis.usage_rate * 100,  # 백분율로 변환
            "cost_per_use": analysis.cost_per_use,
        })

    return result

def get_usage_patterns(db: Session, user_id: int):
    patterns = db.query(models.UsagePattern).filter(models.UsagePattern.user_id == user_id).all()

    result = []
    for pattern in patterns:
        contract = db.query(models.Contract).filter(models.Contract.id == pattern.contract_id).first()
        if not contract:
            continue

        result.append({
            "contract_id": pattern.contract_id,
            "service_name": contract.service_name,
            "total_used_days": pattern.total_used_days,
            "daily_average": pattern.daily_average,
            "weekly_average": pattern.weekly_average,
            "monthly_average": pattern.monthly_average,
            "last_used_date": pattern.last_used_date,
            "most_used_weekday": pattern.most_used_weekday  # 추가
        })

    return result

def reset_usage_analysis_and_pattern(db: Session, contract_id: int):
    """
    계약 갱신 후 사용 분석 및 패턴 데이터를 초기화하고 새 기간에 맞게 업데이트합니다.
    """
    # 사용 분석 데이터 재설정
    update_usage_analysis(db, contract_id)

    # 사용 패턴 데이터 재설정
    update_usage_pattern(db, contract_id)