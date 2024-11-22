from src.db.database import Base, engine
from src.db.models import *

# 데이터베이스 테이블 생성
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")