from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db import crud, schemas
from typing import List
router = APIRouter()

# 1. 계약 생성
@router.post("/", response_model=schemas.ContractResponse)
def create_contract(
    contract: schemas.ContractCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    새로운 계약(구독)을 생성합니다.
    """
    new_contract = crud.create_contract(db=db, contract=contract, user_id=user_id)
    return new_contract


# 2. 특정 계약 조회
@router.get("/{contract_id}", response_model=schemas.ContractResponse)
def get_contract(contract_id: int, db: Session = Depends(get_db)):
    """
    특정 계약 ID에 해당하는 계약 정보를 반환합니다.
    """
    contract = crud.get_contract_by_id(db=db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

# 특정 사용자에 대한 모든 계약 조회
@router.get("/user/{user_id}", response_model=List[schemas.ContractResponse])  # 수정
def get_user_contracts(user_id: int, db: Session = Depends(get_db)):
    """
    특정 사용자 ID에 해당하는 모든 계약을 반환합니다.
    """
    contracts = crud.get_contracts_by_user(db=db, user_id=user_id)
    return contracts
@router.get("/user/{user_id}/total-cost", response_model=float)
def get_total_cost(user_id: int, db: Session = Depends(get_db)):
    """
    특정 사용자의 모든 계약의 monthly_cost 합산 반환.
    """
    total_cost = crud.get_total_monthly_cost(db=db, user_id=user_id)
    return total_cost

# 4. 계약 삭제
@router.delete("/{contract_id}")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    """
    특정 계약 ID를 삭제합니다.
    """
    contract = crud.get_contract_by_id(db=db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    crud.delete_contract(db=db, contract_id=contract_id)
    return {"message": "Contract deleted successfully"}
