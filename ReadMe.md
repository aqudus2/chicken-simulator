# Chicken Simulator

A full-stack application for managing chicken coops and tracking egg production.

## Setup and Run Instructions

### Backend Setup
1. Navigate to backend directory:
```bash
cd Gm/backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the FastAPI server:
```bash
uvicorn main:app --reload
```

### Frontend Setup
1. Navigate to frontend directory:
```bash
cd Gm/frontend/chicken-simulator
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

## System Components

### Backend Components
- **FastAPI Server**: Handles HTTP requests and business logic
- **PostgreSQL Database**: Stores chicken and production data
- **SQLAlchemy ORM**: Manages database operations
- **Pydantic Models**: Handles data validation

### Frontend Components
- **Vue 3**: Frontend framework with Composition API
- **Vuetify**: UI component library
- **Pinia**: State management for chicken data
- **Vue Router**: Navigation between views

## System Logic Flow
1. User accesses dashboard (chicken-sim.vue)
2. System displays:
   - Coop statistics
   - Egg production metrics
   - Health status indicators
3. User can:
   - View detailed chicken information
   - Track egg production
   - Monitor health status
   - Generate reports

## Screenshots

### Dashboard View
![Dashboard](screenshots/dashboard.png)
- Real-time coop monitoring
- Production statistics
- Health status indicators

### Coop Details
![Coop Details](screenshots/coop-details.png)
- Individual chicken tracking
- Production history
- Health monitoring

## Live Demo
[Chicken Simulator Demo](https://your-demo-link.com)

## Project Structure
```
Gm/
├── backend/
│   ├── main.py           # FastAPI endpoints
│   ├── models.py         # Database models
│   └── schemas.py        # Data validation
└── frontend/
    └── chicken-simulator/
        ├── src/
        │   ├── pages/    # Vue components
        │   └── stores/   # State management
        └── package.json
```

## Development Stack
- Backend: FastAPI, PostgreSQL, SQLAlchemy
- Frontend: Vue 3, Vuetify 3, TypeScript
- Tools: Vite, npm, Python 3.8+
