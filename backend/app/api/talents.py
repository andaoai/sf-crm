from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.talent import Talent, CertificateLevel, CertificateSpecialty, SocialSecurityStatus
from ..schemas.talent import TalentCreate, TalentUpdate, Talent as TalentSchema, TalentList

router = APIRouter()

@router.get("/", response_model=TalentList)
def get_talents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    certificate_level: Optional[CertificateLevel] = Query(None),
    certificate_specialty: Optional[CertificateSpecialty] = Query(None),
    social_security_status: Optional[SocialSecurityStatus] = Query(None),
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

    # 证书专业筛选
    if certificate_specialty:
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
    db_talent = Talent(**talent.dict())
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
