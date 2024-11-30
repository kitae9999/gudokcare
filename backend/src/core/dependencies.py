#src/core/dependencies.py

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from src.core.security import decode_access_token
from src.db import crud
from src.db.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = crud.get_user_by_email(db, email=email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")