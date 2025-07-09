from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.communication import Communication
from ..schemas.communication import CommunicationCreate, CommunicationUpdate, Communication as CommunicationSchema, CommunicationList

router = APIRouter()

@router.get("/", response_model=CommunicationList)
def get_communications(skip: int = 0, limit: int = 100, company_id: int = None, talent_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Communication)
    
    if company_id:
        query = query.filter(Communication.company_id == company_id)
    if talent_id:
        query = query.filter(Communication.talent_id == talent_id)
    
    communications = query.offset(skip).limit(limit).all()
    total = query.count()
    return CommunicationList(communications=communications, total=total)

@router.get("/{communication_id}", response_model=CommunicationSchema)
def get_communication(communication_id: int, db: Session = Depends(get_db)):
    communication = db.query(Communication).filter(Communication.id == communication_id).first()
    if not communication:
        raise HTTPException(status_code=404, detail="Communication not found")
    return communication

@router.post("/", response_model=CommunicationSchema)
def create_communication(communication: CommunicationCreate, db: Session = Depends(get_db)):
    db_communication = Communication(**communication.dict())
    db.add(db_communication)
    db.commit()
    db.refresh(db_communication)
    return db_communication

@router.put("/{communication_id}", response_model=CommunicationSchema)
def update_communication(communication_id: int, communication: CommunicationUpdate, db: Session = Depends(get_db)):
    db_communication = db.query(Communication).filter(Communication.id == communication_id).first()
    if not db_communication:
        raise HTTPException(status_code=404, detail="Communication not found")
    
    update_data = communication.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_communication, field, value)
    
    db.commit()
    db.refresh(db_communication)
    return db_communication

@router.delete("/{communication_id}")
def delete_communication(communication_id: int, db: Session = Depends(get_db)):
    db_communication = db.query(Communication).filter(Communication.id == communication_id).first()
    if not db_communication:
        raise HTTPException(status_code=404, detail="Communication not found")
    
    db.delete(db_communication)
    db.commit()
    return {"message": "Communication deleted successfully"}
