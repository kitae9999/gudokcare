#src/api/routes/contracts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db import crud, schemas, models
from src.core.dependencies import get_current_user
from typing import List,Optional
from fastapi import Query
from datetime import date

router = APIRouter()

# 1. 계약 생성
@router.post("/create", response_model=schemas.ContractResponse)
def create_contract(
    contract: schemas.ContractCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """
    새로운 계약(구독)을 생성합니다.
    """
    new_contract = crud.create_contract(db, contract, user_id=current_user.id)
    return new_contract


# 2. 특정 계약 조회
@router.get("/{contract_id}", response_model=schemas.ContractResponse)
def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """
    특정 계약 ID에 해당하는 계약 정보를 반환합니다.
    """
    contract = crud.get_contract_by_id(db, contract_id)
    if not contract or contract.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


# 3. 특정 사용자에 대한 모든 계약 조회
@router.get("/user/contracts", response_model=List[schemas.ContractResponse])
def get_user_contracts(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """
    로그인한 사용자의 모든 계약을 반환합니다.
    """
    contracts = crud.get_contracts_by_user(db, user_id=current_user.id)
    return contracts


# 4. 현재 구독료 총합 조회
@router.get("/user/contracts/total-cost", response_model=float)
def get_current_total_cost(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """
    로그인한 사용자의 현재 활성 상태인 계약의 monthly_cost 합산 반환.
    """
    from datetime import date
    today = date.today()

    # 현재 활성 상태인 계약만 가져옴
    active_contracts = db.query(models.Contract).filter(
        models.Contract.user_id == current_user.id,
        models.Contract.start_date <= today,  # 시작일이 오늘 이전
        (models.Contract.end_date == None) | (models.Contract.end_date >= today)  # 종료일이 없거나 오늘 이후
    ).all()

    # 활성 계약의 monthly_cost 합산
    total_cost = sum(contract.monthly_cost for contract in active_contracts)
    return total_cost

# 5. 계약 삭제
@router.delete("/{contract_id}")
def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """
    특정 계약 ID를 삭제합니다.
    """
    contract = crud.get_contract_by_id(db, contract_id)
    if not contract or contract.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contract not found")
    crud.delete_contract(db, contract_id)
    return {"message": "Contract deleted successfully"}


# 6. 계약 갱신
@router.put("/{contract_id}/renew", response_model=schemas.ContractResponse)
def renew_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """
    계약 갱신
    """
    contract = crud.get_contract_by_id(db, contract_id)
    if not contract or contract.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contract not found")
    renewed_contract = crud.renew_contract(db, contract_id)
    if not renewed_contract:
        raise HTTPException(status_code=400, detail="Unable to renew contract")
    return renewed_contract


# 7. 계약 사용 기록
@router.post("/{contract_id}/log-usage")
def log_contract_usage(
    contract_id: int,
    used: bool,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
    usage_date: Optional[date] = Query(default=date.today())  # 날짜를 쿼리 파라미터로 받음
):
    """
    계약의 사용 여부를 기록합니다. 날짜를 지정할 수 있으며, 기본값은 오늘 날짜입니다.
    """
    contract = crud.get_contract_by_id(db, contract_id)
    if not contract or contract.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contract not found")

    crud.log_usage(db, contract_id, used, usage_date)
    crud.update_usage_pattern(db, contract_id)  # 사용 패턴 업데이트
    return {"message": f"Usage logged successfully for date {usage_date}"}


@router.get("/user/usage-analysis", response_model=List[schemas.UsageAnalysisResponse])
def get_user_usage_analysis(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """
    사용자의 구독 효율성 분석 데이터를 반환합니다.
    """
    analysis = crud.get_usage_analysis(db, user_id=current_user.id)
    return analysis

@router.get("/user/usage-patterns", response_model=List[schemas.UsagePatternResponse])
def get_user_usage_patterns(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """
    사용자의 모든 계약에 대한 사용 패턴 데이터를 반환합니다.
    """
    patterns = crud.get_usage_patterns(db, user_id=current_user.id)
    return patterns