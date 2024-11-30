#src/db/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class ContractBase(BaseModel):
    service_name: str
    monthly_cost: float
    start_date: Optional[date]
    end_date: Optional[date]
    auto_renew: bool = False

class ContractCreate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: int
    user_id: int
    used_today: bool = False
    renewal_period: Optional[int] = None
    class Config:
        orm_mode = True

class UsageAnalysisResponse(BaseModel):
    contract_id: int
    service_name: str
    total_days: int
    used_days: int
    usage_percentage: float
    cost_per_use: Optional[float]

    class Config:
        from_attributes = True

class UsagePatternResponse(BaseModel):
    contract_id: int
    service_name: str
    total_used_days: int
    daily_average: float
    weekly_average: float
    monthly_average: float
    last_used_date: Optional[date]
    most_used_weekday: Optional[str]  # 주로 사용하는 요일 추가
    
    class Config:
        from_attributes = True