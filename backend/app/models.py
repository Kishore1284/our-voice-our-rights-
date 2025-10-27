"""
SQLAlchemy ORM Models for MGNREGA Dashboard
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP, JSONB, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from .database import Base


class District(Base):
    """District model - stores geographic district information"""
    
    __tablename__ = "districts"
    
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, nullable=False, index=True)
    district_name = Column(String, nullable=False)
    district_code = Column(String, unique=True, nullable=False, index=True)
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationship to snapshots
    snapshots = relationship("MGNREGASnapshot", back_populates="district", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<District(id={self.id}, code='{self.district_code}', name='{self.district_name}')>"


class MGNREGASnapshot(Base):
    """MGNREGA performance snapshot model - monthly data per district"""
    
    __tablename__ = "mgnrega_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    people_benefited = Column(Integer, default=0)
    workdays_created = Column(Integer, default=0)
    wages_paid = Column(Numeric(15, 2), default=0)
    payments_on_time_percent = Column(Numeric(5, 2), default=0)
    works_completed = Column(Integer, default=0)
    raw_json = Column(JSONB)
    fetched_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationship to district
    district = relationship("District", back_populates="snapshots")
    
    # Add constraint for month range
    __table_args__ = (
        CheckConstraint('month >= 1 AND month <= 12', name='check_month_range'),
    )
    
    def __repr__(self):
        return f"<MGNREGASnapshot(id={self.id}, district_id={self.district_id}, {self.year}/{self.month:02d})>"

