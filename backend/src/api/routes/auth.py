#src/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db import crud, schemas
from src.core.security import verify_password, create_access_token,get_password_hash

router = APIRouter()

@router.post("/login")
def login_user(response: Response, user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 이메일로 사용자 조회
    existing_user = crud.get_user_by_email(db, email=user.email)
    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # 토큰 생성
    access_token = create_access_token(data={"sub": existing_user.email})
    response.set_cookie(key="token", value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = crud.create_user(db, schemas.UserCreate(email=user.email, password=hashed_password))
    return new_user
