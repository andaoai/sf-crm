from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class CommunicationBase(BaseModel):
    content: str
    result: Optional[str] = None
    company_id: Optional[int] = None
    talent_id: Optional[int] = None
    communication_date: Optional[date] = None
    communication_type: Optional[str] = None  # 沟通方式：电话、微信、面谈、邮件等
    follow_up_required: Optional[bool] = False
    follow_up_date: Optional[date] = None

class CommunicationCreate(CommunicationBase):
    pass

class CommunicationUpdate(BaseModel):
    content: Optional[str] = None
    result: Optional[str] = None
    communication_date: Optional[date] = None
    communication_type: Optional[str] = None
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[date] = None

class Communication(CommunicationBase):
    id: int
    communication_time: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CommunicationList(BaseModel):
    communications: List[Communication]
    total: int
