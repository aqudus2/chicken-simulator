# Gm/backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema for creating a new chicken
class ChickenCreate(BaseModel):
    coop: str
    breed: str
    age: float
    health_status: str
    last_checked_time: datetime

# Schema for updating an existing chicken
class ChickenUpdate(BaseModel):
    coop: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[float] = None
    health_status: Optional[str] = None    
    last_checked_time: Optional[datetime] = None

# Schema for returning chicken data
class ChickenResponse(BaseModel):
    chicken_id: int
    coop: str
    breed: str
    age: float
    health_status: str    
    last_checked_time: datetime
    
    class Config:
        from_attributes = True

# Schema for creating a new egg production record
class EggProductionCreate(BaseModel):
    chicken_id: int
    egg_count: int
    production_date: datetime

# Schema for updating an existing egg production record
class EggProductionUpdate(BaseModel):
    chicken_id: Optional[int] = None
    egg_count: Optional[int] = None
    production_date: Optional[datetime] = None

# Schema for returning egg production data
class EggProductionResponse(BaseModel):
    production_id: int
    chicken_id: int
    egg_count: int
    production_date: datetime
    
    class Config:
        from_attributes = True

# Schema for simplified chicken info (for nested responses)
class ChickenBasic(BaseModel):
    chicken_id: int
    breed: str
    coop: str
    health_status: str
    egg_count: int
    age: float
    
    class Config:
        from_attributes = True

