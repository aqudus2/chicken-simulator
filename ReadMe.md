# Chicken Farm Management System

A full-stack application for managing chicken coops and tracking egg production.

## Environment Setup

### Database Configuration

1. Create a PostgreSQL database named `chicken_db`
2. Create `.env`:

3. Update the `.env` file with your database credentials:
```properties
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chicken_db
```

4. Install PostgreSQL if not already installed:
   - Download from [PostgreSQL Official Website](https://www.postgresql.org/download/windows/)
   - Run the installer and note your superuser password
   - Add PostgreSQL bin directory to PATH: `C:\Program Files\PostgreSQL\{version}\bin`

5. Create the database:
```bash
psql -U postgres -c "CREATE DATABASE chicken_db"
```

### Backend Setup
1. Navigate to backend directory:
```bash
cd Gm/backend
```

2. Create and activate virtual environment:
```bash
py -m venv venv
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
1. User accesses dashboard (index.vue)
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
