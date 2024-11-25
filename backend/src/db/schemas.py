from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Union 
from typing import Optional

# 사용자 스키마
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# 계약/구독 스키마
class ContractBase(BaseModel):
    service_name: str
    monthly_cost: float
    start_date: Union[date, None]  # 변경
    end_date: date
    auto_renew: bool = False
    renewal_period: Optional[int] = None  # 갱신 주기 추가
    used_today: bool  # 추가 필드
    notes: Union[str, None] = None  # 변경
    is_notification_enabled: bool = True  # 기본값: Truex

class ContractCreate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # orm_mode 대신 변경


# 알림 스키마
class NotificationBase(BaseModel):
    contract_id: int
    notification_date: date

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    status: bool

    class Config:
        orm_mode = True