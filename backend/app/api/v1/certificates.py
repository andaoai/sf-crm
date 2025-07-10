from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ...crud import certificate as crud_certificate
from ...schemas.certificate import (
    Certificate, CertificateCreate, CertificateUpdate, CertificateQuery,
    CertificateType, CertificateTypeCreate, CertificateTypeUpdate,
    TalentCertificateSummary, CertificateSearchResult, CertificateStatusEnum
)

router = APIRouter()

# 证书类型管理
@router.get("/types", response_model=List[CertificateType])
def get_certificate_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取证书类型列表"""
    return crud_certificate.get_certificate_types(db, skip=skip, limit=limit)

@router.post("/types", response_model=CertificateType)
def create_certificate_type(
    certificate_type: CertificateTypeCreate,
    db: Session = Depends(get_db)
):
    """创建证书类型"""
    # 检查类型代码是否已存在
    existing = crud_certificate.get_certificate_type_by_code(db, certificate_type.type_code)
    if existing:
        raise HTTPException(status_code=400, detail="证书类型代码已存在")
    
    # 检查类型名称是否已存在
    existing_name = crud_certificate.get_certificate_type_by_name(db, certificate_type.type_name)
    if existing_name:
        raise HTTPException(status_code=400, detail="证书类型名称已存在")
    
    return crud_certificate.create_certificate_type(db, certificate_type)

@router.put("/types/{type_code}", response_model=CertificateType)
def update_certificate_type(
    type_code: str,
    certificate_type: CertificateTypeUpdate,
    db: Session = Depends(get_db)
):
    """更新证书类型"""
    db_certificate_type = crud_certificate.update_certificate_type(db, type_code, certificate_type)
    if not db_certificate_type:
        raise HTTPException(status_code=404, detail="证书类型不存在")
    return db_certificate_type

@router.get("/types/{type_code}", response_model=CertificateType)
def get_certificate_type(
    type_code: str,
    db: Session = Depends(get_db)
):
    """获取单个证书类型"""
    certificate_type = crud_certificate.get_certificate_type_by_code(db, type_code)
    if not certificate_type:
        raise HTTPException(status_code=404, detail="证书类型不存在")
    return certificate_type

# 具体证书管理
@router.get("/")
def get_certificates(
    talent_id: Optional[int] = Query(None, description="人才ID"),
    certificate_type: Optional[str] = Query(None, description="证书类型"),
    category: Optional[str] = Query(None, description="证书大类"),
    status: Optional[CertificateStatusEnum] = Query(None, description="证书状态"),
    specialty: Optional[str] = Query(None, description="专业方向"),
    level: Optional[str] = Query(None, description="等级"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    talent_name: Optional[str] = Query(None, description="人才姓名"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取证书列表"""
    from ...models.talent import Talent

    query = CertificateQuery(
        talent_id=talent_id,
        certificate_type=certificate_type,
        category=category,
        status=status,
        specialty=specialty,
        level=level
    )

    # 获取证书列表，支持人才名称搜索
    certificates = crud_certificate.get_certificates(db, query, talent_name=talent_name, skip=skip, limit=limit)

    # 为每个证书添加人才信息
    result = []
    for cert in certificates:
        cert_dict = {
            'certificate_id': cert.certificate_id,
            'talent_id': cert.talent_id,
            'certificate_type': cert.certificate_type,
            'certificate_name': cert.certificate_name,
            'certificate_number': cert.certificate_number,
            'issue_date': cert.issue_date,
            'expiry_date': cert.expiry_date,
            'issuing_authority': cert.issuing_authority,
            'specialty': cert.specialty,
            'level': cert.level,
            'status': cert.status,
            'notes': cert.notes,
            'created_at': cert.created_at,
            'updated_at': cert.updated_at
        }

        if cert.talent_id:
            talent = db.query(Talent).filter(Talent.id == cert.talent_id).first()
            if talent:
                cert_dict['talent_name'] = talent.name
                cert_dict['talent_phone'] = talent.phone
            else:
                cert_dict['talent_name'] = '未知'
                cert_dict['talent_phone'] = ''
        else:
            cert_dict['talent_name'] = '未关联'
            cert_dict['talent_phone'] = ''

        result.append(cert_dict)

    return result

@router.get("/stats")
def get_certificate_stats(
    talent_id: Optional[int] = Query(None, description="人才ID"),
    certificate_type: Optional[str] = Query(None, description="证书类型"),
    category: Optional[str] = Query(None, description="证书大类"),
    status: Optional[CertificateStatusEnum] = Query(None, description="证书状态"),
    specialty: Optional[str] = Query(None, description="专业方向"),
    level: Optional[str] = Query(None, description="等级"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    talent_name: Optional[str] = Query(None, description="人才姓名"),
    db: Session = Depends(get_db)
):
    """获取证书统计信息"""
    from ...models.talent import Talent
    from datetime import datetime, timedelta

    query = CertificateQuery(
        talent_id=talent_id,
        certificate_type=certificate_type,
        category=category,
        status=status,
        specialty=specialty,
        level=level
    )

    # 获取所有符合条件的证书（不分页）
    all_certificates = crud_certificate.get_certificates(db, query, talent_name=talent_name, skip=0, limit=10000)

    # 统计数据
    total = len(all_certificates)

    # 导入枚举类型
    from ...models.certificate import CertificateStatus

    valid = len([cert for cert in all_certificates if cert.status == CertificateStatus.VALID])
    expired = len([cert for cert in all_certificates if cert.status == CertificateStatus.EXPIRED])

    # 计算即将过期的证书（30天内过期）
    expiring_soon = 0
    current_date = datetime.now().date()
    for cert in all_certificates:
        if cert.expiry_date and cert.status == CertificateStatus.VALID:
            expiry_date = cert.expiry_date
            if isinstance(expiry_date, str):
                try:
                    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
                except:
                    continue

            days_until_expiry = (expiry_date - current_date).days
            if 0 <= days_until_expiry <= 30:
                expiring_soon += 1

    return {
        "total": total,
        "valid": valid,
        "expired": expired,
        "expiring": expiring_soon
    }

@router.post("/", response_model=Certificate)
def create_certificate(
    certificate: CertificateCreate,
    db: Session = Depends(get_db)
):
    """创建证书"""
    import uuid
    from datetime import datetime

    # 自动生成证书ID
    # 格式：CERT_YYYYMMDD_随机字符串
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = str(uuid.uuid4())[:8].upper()
    certificate_id = f"CERT_{timestamp}_{random_suffix}"

    # 确保证书ID唯一
    while crud_certificate.get_certificate(db, certificate_id):
        random_suffix = str(uuid.uuid4())[:8].upper()
        certificate_id = f"CERT_{timestamp}_{random_suffix}"

    # 检查证书类型是否存在
    certificate_type = crud_certificate.get_certificate_type_by_name(db, certificate.certificate_type)
    if not certificate_type:
        raise HTTPException(status_code=400, detail="证书类型不存在")

    # 创建带有自动生成ID的证书数据
    certificate_data = certificate.model_dump()
    certificate_data['certificate_id'] = certificate_id

    # 创建新的CertificateCreate对象
    from ...schemas.certificate import CertificateCreate
    certificate_with_id = CertificateCreate(**certificate_data)

    return crud_certificate.create_certificate(db, certificate_with_id)

@router.get("/{certificate_id}", response_model=Certificate)
def get_certificate(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    """获取单个证书"""
    certificate = crud_certificate.get_certificate(db, certificate_id)
    if not certificate:
        raise HTTPException(status_code=404, detail="证书不存在")
    return certificate

@router.put("/{certificate_id}", response_model=Certificate)
def update_certificate(
    certificate_id: str,
    certificate: CertificateUpdate,
    db: Session = Depends(get_db)
):
    """更新证书"""
    db_certificate = crud_certificate.update_certificate(db, certificate_id, certificate)
    if not db_certificate:
        raise HTTPException(status_code=404, detail="证书不存在")
    return db_certificate

@router.delete("/{certificate_id}")
def delete_certificate(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    """删除证书"""
    success = crud_certificate.delete_certificate(db, certificate_id)
    if not success:
        raise HTTPException(status_code=404, detail="证书不存在")
    return {"message": "证书删除成功"}

# 人才证书查询
@router.get("/talent/{talent_id}", response_model=List[Certificate])
def get_talent_certificates(
    talent_id: int,
    db: Session = Depends(get_db)
):
    """获取某个人才的所有证书"""
    return crud_certificate.get_certificates_by_talent(db, talent_id)

@router.get("/talent/{talent_id}/summary", response_model=TalentCertificateSummary)
def get_talent_certificate_summary(
    talent_id: int,
    db: Session = Depends(get_db)
):
    """获取人才证书汇总信息"""
    summary = crud_certificate.get_talent_certificate_summary(db, talent_id)
    if not summary:
        raise HTTPException(status_code=404, detail="人才不存在")
    return summary

# 证书搜索功能
@router.get("/search/by-type", response_model=List[CertificateSearchResult])
def search_talents_by_certificate_type(
    certificate_type: str = Query(..., description="证书类型"),
    status: str = Query("VALID", description="证书状态"),
    db: Session = Depends(get_db)
):
    """根据证书类型搜索人才"""
    return crud_certificate.search_talents_by_certificate_type(db, certificate_type, status)

@router.get("/search/by-category", response_model=List[CertificateSearchResult])
def search_talents_by_category(
    category: str = Query(..., description="证书大类"),
    status: str = Query("VALID", description="证书状态"),
    db: Session = Depends(get_db)
):
    """根据证书大类搜索人才"""
    return crud_certificate.search_talents_by_category(db, category, status)

@router.get("/expiring", response_model=List[Certificate])
def get_expiring_certificates(
    days: int = Query(30, description="多少天内到期"),
    db: Session = Depends(get_db)
):
    """获取即将到期的证书"""
    return crud_certificate.get_expiring_certificates(db, days)
