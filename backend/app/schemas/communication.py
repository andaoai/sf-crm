from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommunicationBase(BaseModel):
    content: str
    result: Optional[str] = None
    company_id: Optional[int] = None
    talent_id: Optional[int] = None

class CommunicationCreate(CommunicationBase):
    pass

class CommunicationUpdate(BaseModel):
    content: Optional[str] = None
    result: Optional[str] = None

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
