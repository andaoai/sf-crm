from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import re
from ..database import get_db
from ..models.talent import Talent, CertificateLevel, CertificateSpecialty, SocialSecurityStatus
from ..schemas.talent import TalentCreate, TalentUpdate, Talent as TalentSchema, TalentList

router = APIRouter()

def auto_classify_certificate(cert_info: str, comm_content: str = None):
    """自动分类证书信息"""
    if not cert_info and not comm_content:
        return None, None, None, None

    # 合并证书信息和沟通内容
    full_text = ""
    if cert_info:
        full_text += cert_info
    if comm_content and comm_content != cert_info:
        full_text += " " + comm_content

    if not full_text:
        return None, None, None, None

    text_lower = full_text.lower()

    # 提取证书等级
    certificate_level = None
    if any(keyword in text_lower for keyword in ["一建", "一级建造师", "考一建", "备考一建", "增项一建"]):
        certificate_level = "一级"
    elif any(keyword in text_lower for keyword in ["二建", "二级建造师", "2建", "二级"]):
        certificate_level = "二级"
    elif any(keyword in text_lower for keyword in ["高级工程师", "高工", "正高级工程师"]):
        certificate_level = "高级工程师"
    elif any(keyword in text_lower for keyword in ["中级工程师", "中工", "工程师"]) and "高级" not in text_lower and "初级" not in text_lower:
        certificate_level = "中级工程师"
    elif any(keyword in text_lower for keyword in ["初级工程师", "助理工程师", "技术员"]):
        certificate_level = "初级工程师"
    elif any(keyword in text_lower for keyword in ["三类人员a", "a类", "企业主要负责人", "法定代表人"]):
        certificate_level = "三类人员A类"
    elif any(keyword in text_lower for keyword in ["三类人员b", "b类", "项目负责人", "项目经理"]):
        certificate_level = "三类人员B类"
    elif any(keyword in text_lower for keyword in ["三类人员c", "c类", "安全员", "专职安全", "c1", "c2", "c3"]):
        certificate_level = "三类人员C类"

    # 提取证书专业
    certificate_specialty = None
    specialty_mapping = [
        # 建造师专业
        ("建筑工程", "建筑工程"),
        ("市政公用工程", "市政公用工程"),
        ("机电工程", "机电工程"),
        ("公路工程", "公路工程"),
        ("水利水电工程", "水利水电工程"),
        ("矿业工程", "矿业工程"),
        ("铁路工程", "铁路工程"),
        ("民航机场工程", "民航机场工程"),
        ("港口与航道工程", "港口与航道工程"),
        ("通信与广电工程", "通信与广电工程"),
        # 建造师简称
        ("房建", "建筑工程"),
        ("建筑", "建筑工程"),
        ("市政", "市政公用工程"),
        ("机电", "机电工程"),
        ("公路", "公路工程"),
        ("水利水电", "水利水电工程"),
        ("水利", "水利水电工程"),
        ("矿业", "矿业工程"),
        ("铁路", "铁路工程"),
        ("民航", "民航机场工程"),
        ("港口", "港口与航道工程"),
        ("航道", "港口与航道工程"),
        ("通信", "通信与广电工程"),
        ("广电", "通信与广电工程"),
        # 工程师专业
        ("建筑工程师", "建筑工程师"),
        ("结构工程师", "结构工程师"),
        ("电气工程师", "电气工程师"),
        ("给排水工程师", "给排水工程师"),
        ("暖通工程师", "暖通工程师"),
        ("建筑设计工程师", "建筑设计工程师"),
        ("工程造价工程师", "工程造价工程师"),
        ("造价工程师", "工程造价工程师"),
        ("测绘工程师", "测绘工程师"),
        ("岩土工程师", "岩土工程师"),
        ("建筑材料工程师", "建筑材料工程师"),
        # 三类人员
        ("安全员", "安全管理"),
        ("安全管理", "安全管理"),
        ("专职安全", "安全管理")
    ]

    for keyword, specialty in specialty_mapping:
        if keyword in full_text:
            certificate_specialty = specialty
            break

    # 提取社保情况
    social_security_status = None
    if any(keyword in text_lower for keyword in ["无社保", "没有社保", "社保不配合", "不配合", "社保公积金"]):
        social_security_status = "无社保"
    elif any(keyword in text_lower for keyword in ["唯一社保", "独立社保", "单独社保"]):
        social_security_status = "唯一社保"

    # 提取合同价格
    contract_price = None
    price_patterns = [
        r'挂了(\d+\.?\d*)[万w]',
        r'挂.*?(\d+\.?\d*)[万w]',
        r'报价.*?(\d+\.?\d*)[万w]?',
        r'价格.*?(\d+\.?\d*)[万w]?',
        r'(\d+\.?\d*)[万w]',
        r'(\d+\.?\d*)w',
    ]

    for pattern in price_patterns:
        match = re.search(pattern, full_text)
        if match:
            try:
                price = float(match.group(1))
                if 'w' in full_text.lower() or '万' in full_text or price < 100:
                    price = price * 10000
                contract_price = price
                break
            except:
                continue

    return certificate_level, certificate_specialty, social_security_status, contract_price

@router.get("/", response_model=TalentList)
def get_talents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    certificate_level: Optional[str] = Query(None),  # 改为字符串类型
    certificate_specialty: Optional[str] = Query(None),  # 改为字符串类型
    social_security_status: Optional[str] = Query(None),  # 改为字符串类型
    db: Session = Depends(get_db)
):
    query = db.query(Talent)

    if search:
        query = query.filter(
            Talent.name.contains(search) |
            Talent.phone.contains(search) |
            Talent.certificate_info.contains(search) |
            Talent.communication_content.contains(search)
        )

    # 证书等级筛选
    if certificate_level:
        query = query.filter(Talent.certificate_level == certificate_level)

    # 证书专业筛选（支持多选）
    if certificate_specialty:
        if ',' in certificate_specialty:
            # 多选情况，分割字符串
            specialties = [s.strip() for s in certificate_specialty.split(',')]
            query = query.filter(Talent.certificate_specialty.in_(specialties))
        else:
            # 单选情况
            query = query.filter(Talent.certificate_specialty == certificate_specialty)

    # 社保情况筛选
    if social_security_status:
        query = query.filter(Talent.social_security_status == social_security_status)

    total = query.count()
    talents = query.offset(skip).limit(limit).all()

    return TalentList(talents=talents, total=total)

@router.get("/{talent_id}", response_model=TalentSchema)
def get_talent(talent_id: int, db: Session = Depends(get_db)):
    talent = db.query(Talent).filter(Talent.id == talent_id).first()
    if not talent:
        raise HTTPException(status_code=404, detail="Talent not found")
    return talent

@router.post("/", response_model=TalentSchema)
def create_talent(talent: TalentCreate, db: Session = Depends(get_db)):
    talent_data = talent.dict()

    # 处理空字符串，将其转换为None
    for field in ['certificate_level', 'certificate_specialty', 'social_security_status',
                  'gender', 'phone', 'wechat_note', 'certificate_info', 'communication_content']:
        if talent_data.get(field) == '':
            talent_data[field] = None

    # 设置默认意向等级
    if not talent_data.get('intention_level'):
        talent_data['intention_level'] = 'C'

    db_talent = Talent(**talent_data)
    db.add(db_talent)
    db.commit()
    db.refresh(db_talent)
    return db_talent

@router.put("/{talent_id}", response_model=TalentSchema)
def update_talent(talent_id: int, talent: TalentUpdate, db: Session = Depends(get_db)):
    db_talent = db.query(Talent).filter(Talent.id == talent_id).first()
    if not db_talent:
        raise HTTPException(status_code=404, detail="Talent not found")

    update_data = talent.dict(exclude_unset=True)

    # 处理空字符串，将其转换为None
    for field, value in update_data.items():
        if value == '':
            update_data[field] = None

    for field, value in update_data.items():
        setattr(db_talent, field, value)

    db.commit()
    db.refresh(db_talent)
    return db_talent

@router.delete("/{talent_id}")
def delete_talent(talent_id: int, db: Session = Depends(get_db)):
    db_talent = db.query(Talent).filter(Talent.id == talent_id).first()
    if not db_talent:
        raise HTTPException(status_code=404, detail="Talent not found")
    
    db.delete(db_talent)
    db.commit()
    return {"message": "Talent deleted successfully"}
