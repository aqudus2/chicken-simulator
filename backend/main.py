# Gm/backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from database import engine, get_db
from models import Base, Chicken, EggProduction
from schemas import (
    ChickenCreate, ChickenResponse, ChickenUpdate, 
    EggProductionCreate, EggProductionResponse, EggProductionUpdate,
    
)

app = FastAPI(title="Chicken Simulator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Create the database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Chicken Simulator API!"}

# CHICKEN ENDPOINTS
@app.post("/chickens/populate", response_model=list[ChickenResponse])
def populate_chickens(db: Session = Depends(get_db)):
    """Populate database with sample chickens (20 chickens across 4 coops)"""
    if db.query(Chicken).count() > 0:
        raise HTTPException(status_code=400, detail="Chickens already populated")
    
    chickens = [
        # Coop A: 5 chickens
        Chicken(coop="A", breed="Kampung", age=1.5, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="A", breed="Kampung", age=1.6, health_status="Sick", last_checked_time=datetime.now()),
        Chicken(coop="A", breed="Rhode", age=1.7, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="A", breed="Sussex", age=1.4, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="A", breed="Leghorn", age=1.5, health_status="Good", last_checked_time=datetime.now()),
        
        # Coop B: 5 chickens
        Chicken(coop="B", breed="Kampung", age=1.3, health_status="Sick", last_checked_time=datetime.now()),
        Chicken(coop="B", breed="Rhode", age=1.8, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="B", breed="Rhode", age=1.6, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="B", breed="Sussex", age=1.5, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="B", breed="Leghorn", age=1.4, health_status="Good", last_checked_time=datetime.now()),
        
        # Coop C: 5 chickens
        Chicken(coop="C", breed="Kampung", age=1.4, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="C", breed="Rhode", age=1.7, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="C", breed="Sussex", age=1.5, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="C", breed="Sussex", age=1.6, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="C", breed="Leghorn", age=1.5, health_status="Good", last_checked_time=datetime.now()),
        
        # Coop D: 5 chickens
        Chicken(coop="D", breed="Kampung", age=1.5, health_status="Sick", last_checked_time=datetime.now()),
        Chicken(coop="D", breed="Rhode", age=1.6, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="D", breed="Sussex", age=1.4, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="D", breed="Leghorn", age=1.5, health_status="Good", last_checked_time=datetime.now()),
        Chicken(coop="D", breed="Leghorn", age=1.7, health_status="Good", last_checked_time=datetime.now())
    ]
    
    db.add_all(chickens)
    db.commit()
    
    return chickens

@app.post("/chickens/", response_model=ChickenResponse)
def create_chicken(chicken_data: ChickenCreate, db: Session = Depends(get_db)):
    """Create a new chicken"""
    new_chicken = Chicken(**chicken_data.dict())
    db.add(new_chicken)
    db.commit()
    db.refresh(new_chicken)
    return new_chicken

@app.get("/chickens/", response_model=list[ChickenResponse])
def get_chickens(db: Session = Depends(get_db)):
    """Get all chickens"""
    return db.query(Chicken).all()

@app.get("/chickens/{chicken_id}", response_model=ChickenResponse)
def get_chicken(chicken_id: int, db: Session = Depends(get_db)):
    """Get a specific chicken by ID"""
    chicken = db.query(Chicken).filter(Chicken.chicken_id == chicken_id).first()
    if not chicken:
        raise HTTPException(status_code=404, detail="Chicken not found")
    return chicken

@app.put("/chickens/{chicken_id}", response_model=ChickenResponse)
def update_chicken(chicken_id: int, chicken_data: ChickenUpdate, db: Session = Depends(get_db)):
    """Update a chicken"""
    chicken = db.query(Chicken).filter(Chicken.chicken_id == chicken_id).first()
    if not chicken:
        raise HTTPException(status_code=404, detail="Chicken not found")
    
    update_data = chicken_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(chicken, field, value)
    
    db.commit()
    db.refresh(chicken)
    return chicken

@app.delete("/chickens/{chicken_id}")
def delete_chicken(chicken_id: int, db: Session = Depends(get_db)):
    """Delete a chicken"""
    chicken = db.query(Chicken).filter(Chicken.chicken_id == chicken_id).first()
    if not chicken:
        raise HTTPException(status_code=404, detail="Chicken not found")
    
    db.delete(chicken)
    db.commit()
    return {"message": "Chicken deleted successfully"}

# EGG PRODUCTION ENDPOINTS
@app.post("/egg-production/seed")
def seed_egg_production_data(db: Session = Depends(get_db)):
    """Seed egg production data for existing chickens (last 30 days)"""
    chickens = db.query(Chicken).all()
    
    egg_productions = []
    for chicken in chickens:
        for days_ago in range(30):
            if random.random() < 0.8:  # 80% chance of production per day
                production_date = datetime.now() - timedelta(days=days_ago)
                egg_count = random.randint(0, 3)
                
                egg_production = EggProduction(
                    chicken_id=chicken.chicken_id,
                    egg_count=egg_count,
                    production_date=production_date
                )
                egg_productions.append(egg_production)
    
    db.add_all(egg_productions)
    db.commit()
    
    return {
        "message": f"Created {len(egg_productions)} egg production records",
        "chickens_with_data": len(chickens)
    }

@app.post("/egg-production/", response_model=EggProductionResponse)
def create_egg_production(egg_data: EggProductionCreate, db: Session = Depends(get_db)):
    """Create a new egg production record"""
    chicken = db.query(Chicken).filter(Chicken.chicken_id == egg_data.chicken_id).first()
    if not chicken:
        raise HTTPException(status_code=404, detail="Chicken not found")
    
    new_egg_production = EggProduction(**egg_data.dict())
    db.add(new_egg_production)
    db.commit()
    db.refresh(new_egg_production)
    return new_egg_production

@app.get("/egg-production/", response_model=list[EggProductionResponse])
def get_egg_production(db: Session = Depends(get_db)):
    """Get all egg production records"""
    return db.query(EggProduction).all()

@app.get("/chickens/{chicken_id}/egg-production", response_model=list[EggProductionResponse])
def get_chicken_egg_production(chicken_id: int, db: Session = Depends(get_db)):
    """Get egg production records for a specific chicken"""
    chicken = db.query(Chicken).filter(Chicken.chicken_id == chicken_id).first()
    if not chicken:
        raise HTTPException(status_code=404, detail="Chicken not found")
    
    return db.query(EggProduction).filter(EggProduction.chicken_id == chicken_id).all()

# ANALYTICS ENDPOINTS


@app.get("/analytics/coop/{coop_name}")
def get_coop_summary(coop_name: str, db: Session = Depends(get_db)):
    """Get summary statistics for a specific coop"""
    chickens = db.query(Chicken).filter(Chicken.coop == coop_name).all()
    if not chickens:
        raise HTTPException(status_code=404, detail="No chickens found in this coop")
    
    total_chickens = len(chickens)
    total_eggs = sum(
        sum(ep.egg_count for ep in chicken.egg_productions) 
        for chicken in chickens
    )
    
    return {
        "coop_name": coop_name,
        "total_chickens": total_chickens,
        "total_eggs_produced": total_eggs,
        "chickens": [
            {
                "chicken_id": chicken.chicken_id,
                "breed": chicken.breed,
                "health_status": chicken.health_status,
                "total_eggs": sum(ep.egg_count for ep in chicken.egg_productions)
            }
            for chicken in chickens
        ]
    }

@app.get("/chickens/{chicken_id}/details")
def get_chicken_with_production_details(chicken_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a chicken including production history"""
    chicken = db.query(Chicken).filter(Chicken.chicken_id == chicken_id).first()
    if not chicken:
        raise HTTPException(status_code=404, detail="Chicken not found")
    
    return {
        "chicken": {
            "chicken_id": chicken.chicken_id,
            "coop": chicken.coop,
            "breed": chicken.breed,
            "age": chicken.age,
            "health_status": chicken.health_status,            
            "last_checked_time": chicken.last_checked_time
        },
        "production_history": [
            {
                "production_id": ep.production_id,
                "egg_count": ep.egg_count,
                "production_date": ep.production_date
            }
            for ep in chicken.egg_productions
        ],
        "total_productions": len(chicken.egg_productions),
        "total_eggs_produced": sum(ep.egg_count for ep in chicken.egg_productions)
    }