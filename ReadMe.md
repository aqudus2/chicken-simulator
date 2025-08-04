# Chicken Simulator

A full-stack application for managing chicken coops and tracking egg production.

## Features
- Real-time monitoring of chicken coops
- Egg production tracking and analytics
- Health status monitoring
- Production statistics and reporting
- Interactive dashboard

## Tech Stack
### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

### Frontend
- Vue 3
- Vuetify 3
- Pinia
- TypeScript
- Vite

## Setup

### Backend
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```env
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chicken_db
```

3. Run server:
```bash
uvicorn main:app --reload
```

### Frontend
1. Install and run:
```bash
npm install
npm run dev
```

## API Endpoints

### Chickens
- `GET /chickens/` - List all chickens
- `POST /chickens/populate` - Populate sample data
- `GET /chickens/{chicken_id}` - Get chicken details

### Egg Production
- `GET /egg-production/` - List all production records
- `POST /egg-production/seed` - Seed production data
- `GET /chickens/{chicken_id}/egg-production` - Get production history

## Project Structure
```
Gm/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── models.py         # Database models
│   └── schemas.py        # Data schemas
└── frontend/
    └── chicken-simulator/
        ├── src/
        │   ├── pages/    # Vue components
        │   └── stores/   # Pinia stores
        └── package.json
```"# chicken-simulator" 
