from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from ..models.certificate import Certificate, CertificateType
from ..models.talent import Talent
from ..schemas.certificate import (
    CertificateCreate, CertificateUpdate, CertificateQuery,
    CertificateTypeCreate, CertificateTypeUpdate,
    TalentCertificateSummary, CertificateSearchResult,
    CertificateStatusEnum
)

# 证书类型CRUD操作
def get_certificate_types(db: Session, skip: int = 0, limit: int = 100) -> List[CertificateType]:
    """获取证书类型列表"""
    return db.query(CertificateType).filter(CertificateType.is_active == True)\
             .order_by(CertificateType.sort_order, CertificateType.type_name)\
             .offset(skip).limit(limit).all()

def get_certificate_type_by_code(db: Session, type_code: str) -> Optional[CertificateType]:
    """根据类型代码获取证书类型"""
    return db.query(CertificateType).filter(CertificateType.type_code == type_code).first()

def get_certificate_type_by_name(db: Session, type_name: str) -> Optional[CertificateType]:
    """根据类型名称获取证书类型"""
    return db.query(CertificateType).filter(CertificateType.type_name == type_name).first()

def create_certificate_type(db: Session, certificate_type: CertificateTypeCreate) -> CertificateType:
    """创建证书类型"""
    db_certificate_type = CertificateType(**certificate_type.model_dump())
    db.add(db_certificate_type)
    db.commit()
    db.refresh(db_certificate_type)
    return db_certificate_type

def update_certificate_type(db: Session, type_code: str, certificate_type: CertificateTypeUpdate) -> Optional[CertificateType]:
    """更新证书类型"""
    db_certificate_type = get_certificate_type_by_code(db, type_code)
    if db_certificate_type:
        update_data = certificate_type.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_certificate_type, field, value)
        db.commit()
        db.refresh(db_certificate_type)
    return db_certificate_type

# 具体证书CRUD操作
def get_certificate(db: Session, certificate_id: str) -> Optional[Certificate]:
    """根据证书ID获取证书"""
    return db.query(Certificate).filter(Certificate.certificate_id == certificate_id).first()

def get_certificates_by_talent(db: Session, talent_id: int) -> List[Certificate]:
    """获取某个人才的所有证书"""
    return db.query(Certificate).filter(Certificate.talent_id == talent_id).all()

def get_certificates(db: Session, query: CertificateQuery, talent_name: str = None, skip: int = 0, limit: int = 100) -> List[Certificate]:
    """根据查询条件获取证书列表"""
    from ..models.talent import Talent

    db_query = db.query(Certificate)

    # 记录已经JOIN的表，避免重复JOIN
    joined_talent = False
    joined_cert_type = False

    # 如果需要按人才名称搜索，需要关联人才表
    if talent_name:
        db_query = db_query.join(Talent, Certificate.talent_id == Talent.id)
        db_query = db_query.filter(Talent.name.like(f"%{talent_name}%"))
        joined_talent = True

    if query.talent_id:
        db_query = db_query.filter(Certificate.talent_id == query.talent_id)
    if query.certificate_type:
        db_query = db_query.filter(Certificate.certificate_type == query.certificate_type)
    if query.status:
        db_query = db_query.filter(Certificate.status == query.status)
    if query.specialty:
        db_query = db_query.filter(Certificate.specialty.like(f"%{query.specialty}%"))
    if query.level:
        db_query = db_query.filter(Certificate.level == query.level)

    # 如果指定了证书大类，需要关联证书类型表
    if query.category:
        if not joined_cert_type:
            db_query = db_query.join(CertificateType, Certificate.certificate_type == CertificateType.type_name)
            joined_cert_type = True
        db_query = db_query.filter(CertificateType.category == query.category)

    return db_query.offset(skip).limit(limit).all()

def create_certificate(db: Session, certificate: CertificateCreate) -> Certificate:
    """创建证书"""
    db_certificate = Certificate(**certificate.model_dump())
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

def update_certificate(db: Session, certificate_id: str, certificate: CertificateUpdate) -> Optional[Certificate]:
    """更新证书"""
    db_certificate = get_certificate(db, certificate_id)
    if db_certificate:
        update_data = certificate.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_certificate, field, value)
        db.commit()
        db.refresh(db_certificate)
    return db_certificate

def delete_certificate(db: Session, certificate_id: str) -> bool:
    """删除证书"""
    db_certificate = get_certificate(db, certificate_id)
    if db_certificate:
        db.delete(db_certificate)
        db.commit()
        return True
    return False

# 高级查询功能
def search_talents_by_certificate_type(db: Session, certificate_type: str, status: str = "VALID") -> List[CertificateSearchResult]:
    """根据证书类型搜索人才"""
    results = db.query(
        Certificate.talent_id,
        Talent.name.label('talent_name'),
        Talent.phone,
        Certificate.certificate_type,
        Certificate.certificate_name,
        Certificate.specialty,
        Certificate.level,
        Certificate.status,
        Certificate.expiry_date
    ).join(Talent, Certificate.talent_id == Talent.id)\
     .filter(and_(Certificate.certificate_type == certificate_type, Certificate.status == status))\
     .all()
    
    return [CertificateSearchResult(
        talent_id=r.talent_id,
        talent_name=r.talent_name,
        phone=r.phone,
        certificate_type=r.certificate_type,
        certificate_name=r.certificate_name,
        specialty=r.specialty,
        level=r.level,
        status=r.status,
        expiry_date=r.expiry_date
    ) for r in results]

def search_talents_by_category(db: Session, category: str, status: str = "VALID") -> List[CertificateSearchResult]:
    """根据证书大类搜索人才"""
    results = db.query(
        Certificate.talent_id,
        Talent.name.label('talent_name'),
        Talent.phone,
        Certificate.certificate_type,
        Certificate.certificate_name,
        Certificate.specialty,
        Certificate.level,
        Certificate.status,
        Certificate.expiry_date
    ).join(Talent, Certificate.talent_id == Talent.id)\
     .join(CertificateType, Certificate.certificate_type == CertificateType.type_name)\
     .filter(and_(CertificateType.category == category, Certificate.status == status))\
     .all()
    
    return [CertificateSearchResult(
        talent_id=r.talent_id,
        talent_name=r.talent_name,
        phone=r.phone,
        certificate_type=r.certificate_type,
        certificate_name=r.certificate_name,
        specialty=r.specialty,
        level=r.level,
        status=r.status,
        expiry_date=r.expiry_date
    ) for r in results]

def get_talent_certificate_summary(db: Session, talent_id: int) -> Optional[TalentCertificateSummary]:
    """获取人才证书汇总信息"""
    talent = db.query(Talent).filter(Talent.id == talent_id).first()
    if not talent:
        return None
    
    certificates = db.query(Certificate.certificate_type)\
                    .filter(and_(Certificate.talent_id == talent_id, Certificate.status == "VALID"))\
                    .distinct().all()
    
    certificate_types = [cert.certificate_type for cert in certificates]
    
    return TalentCertificateSummary(
        talent_id=talent_id,
        talent_name=talent.name,
        certificates=certificate_types,
        certificate_count=len(certificate_types)
    )

def get_expiring_certificates(db: Session, days: int = 30) -> List[Certificate]:
    """获取即将到期的证书"""
    from datetime import date, timedelta
    expiry_threshold = date.today() + timedelta(days=days)
    
    return db.query(Certificate)\
             .filter(and_(
                 Certificate.expiry_date <= expiry_threshold,
                 Certificate.expiry_date >= date.today(),
                 Certificate.status == "VALID"
             ))\
             .order_by(Certificate.expiry_date)\
             .all()
