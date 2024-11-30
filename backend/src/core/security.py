#src/core/security.py


from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 설정
SECRET_KEY = "your-secret-key"  # 비밀키는 환경 변수로 관리하는 것이 좋습니다.
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 비밀번호 해싱 함수
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """JWT 액세스 토큰 생성"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT 토큰 검증 함수
def decode_access_token(token: str) -> dict:
    """JWT 액세스 토큰 디코딩 및 검증"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e