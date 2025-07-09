from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.company import IntentionLevel

class CompanyBase(BaseModel):
    name: str
    contact_info: Optional[str] = None
    communication_notes: Optional[str] = None
    intention: Optional[str] = None
    intention_level: Optional[IntentionLevel] = IntentionLevel.C
    price: Optional[str] = None
    certificate_requirements: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None
    communication_notes: Optional[str] = None
    intention: Optional[str] = None
    intention_level: Optional[IntentionLevel] = None
    price: Optional[str] = None
    certificate_requirements: Optional[str] = None

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CompanyList(BaseModel):
    companies: List[Company]
    total: int
