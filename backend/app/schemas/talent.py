from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from ..models.talent import IntentionLevel, CertificateLevel, CertificateSpecialty, SocialSecurityStatus

class TalentBase(BaseModel):
    name: str
    gender: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    wechat_note: Optional[str] = None
    contract_price: Optional[Decimal] = None
    intention_level: Optional[IntentionLevel] = IntentionLevel.C

    # 地区信息
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None

    # 新增字段
    communication_content: Optional[str] = None
    social_security_status: Optional[str] = None  # 改为字符串类型



    @field_validator('contract_price', mode='before')
    @classmethod
    def validate_contract_price(cls, v):
        if v == '' or v is None:
            return None
        return v

    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, v):
        if v == '' or v is None:
            return None
        return v

class TalentCreate(TalentBase):
    pass

class TalentUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    wechat_note: Optional[str] = None
    contract_price: Optional[Decimal] = None
    intention_level: Optional[IntentionLevel] = None

    # 地区信息
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None

    # 新增字段
    communication_content: Optional[str] = None
    social_security_status: Optional[str] = None  # 改为字符串类型

class Talent(TalentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TalentList(BaseModel):
    talents: List[Talent]
    total: int
