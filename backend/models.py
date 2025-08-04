# Gm/backend/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

# Model for Chicken
class Chicken(Base):
    __tablename__ = 'chickens'
    
    chicken_id = Column(Integer, primary_key=True, autoincrement=True)
    coop = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    age = Column(Float, nullable=False)
    health_status = Column(String, nullable=False)
    last_checked_time = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Relationship to access egg production records
    egg_productions = relationship("EggProduction", back_populates="chicken", cascade="all, delete-orphan")

# Model for tracking egg production history
class EggProduction(Base):
    __tablename__ = 'egg_production'
    
    production_id = Column(Integer, primary_key=True, autoincrement=True)
    chicken_id = Column(Integer, ForeignKey('chickens.chicken_id'), nullable=False)
    egg_count = Column(Integer, nullable=False)  # Eggs produced on a specific date
    production_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Relationship to access chicken details
    chicken = relationship("Chicken", back_populates="egg_productions")