from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db import crud, schemas
from src.core.security import get_password_hash

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = crud.create_user(db, schemas.UserCreate(email=user.email, password=hashed_password))
    return new_user

@router.post("/register-token")
def register_firebase_token(user_id: int, firebase_token: str, db: Session = Depends(get_db)):
    """
    사용자 디바이스 토큰 등록
    """
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.firebase_token = firebase_token
    db.commit()
    db.refresh(user)
    return {"message": "Firebase token registered successfully"}