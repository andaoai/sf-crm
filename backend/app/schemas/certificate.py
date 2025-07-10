from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class CertificateStatusEnum(str, Enum):
    VALID = "VALID"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"

# 证书类型相关Schema
class CertificateTypeBase(BaseModel):
    type_code: str = Field(..., description="证书类型代码")
    type_name: str = Field(..., description="证书类型名称")
    category: Optional[str] = Field(None, description="证书大类")
    description: Optional[str] = Field(None, description="证书描述")
    is_active: bool = Field(True, description="是否启用")
    sort_order: int = Field(0, description="排序")

class CertificateTypeCreate(CertificateTypeBase):
    pass

class CertificateTypeUpdate(BaseModel):
    type_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class CertificateType(CertificateTypeBase):
    created_at: datetime

    class Config:
        from_attributes = True

# 具体证书相关Schema
class CertificateBase(BaseModel):
    talent_id: Optional[int] = Field(None, description="人才ID")
    certificate_type: str = Field(..., description="证书类型")
    certificate_name: Optional[str] = Field(None, description="证书全称")
    certificate_number: Optional[str] = Field(None, description="证书编号")
    issue_date: Optional[date] = Field(None, description="颁发日期")
    expiry_date: Optional[date] = Field(None, description="到期日期")
    issuing_authority: Optional[str] = Field(None, description="发证机构")
    specialty: Optional[str] = Field(None, description="专业方向")
    level: Optional[str] = Field(None, description="等级")
    status: CertificateStatusEnum = Field(CertificateStatusEnum.VALID, description="证书状态")
    notes: Optional[str] = Field(None, description="备注")

class CertificateCreate(CertificateBase):
    certificate_id: Optional[str] = Field(None, description="证书ID（自动生成）")

class CertificateUpdate(BaseModel):
    talent_id: Optional[int] = None
    certificate_type: Optional[str] = None
    certificate_name: Optional[str] = None
    certificate_number: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    issuing_authority: Optional[str] = None
    specialty: Optional[str] = None
    level: Optional[str] = None
    status: Optional[CertificateStatusEnum] = None
    notes: Optional[str] = None

class Certificate(CertificateBase):
    certificate_id: str = Field(..., description="证书ID")
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# 查询相关Schema
class CertificateQuery(BaseModel):
    talent_id: Optional[int] = Field(None, description="人才ID")
    certificate_type: Optional[str] = Field(None, description="证书类型")
    category: Optional[str] = Field(None, description="证书大类")
    status: Optional[CertificateStatusEnum] = Field(None, description="证书状态")
    specialty: Optional[str] = Field(None, description="专业方向")
    level: Optional[str] = Field(None, description="等级")

class TalentCertificateSummary(BaseModel):
    """人才证书汇总信息"""
    talent_id: int
    talent_name: str
    certificates: List[str] = Field(description="拥有的证书类型列表")
    certificate_count: int = Field(description="证书总数")

class CertificateSearchResult(BaseModel):
    """证书搜索结果"""
    talent_id: int
    talent_name: str
    phone: Optional[str] = None
    certificate_type: str
    certificate_name: Optional[str] = None
    specialty: Optional[str] = None
    level: Optional[str] = None
    status: CertificateStatusEnum
    expiry_date: Optional[date] = None
