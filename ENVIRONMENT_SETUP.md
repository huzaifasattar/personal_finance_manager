# Personal Finance Manager - Environment Setup Plan

## Overview
This document outlines the complete environment setup for the Personal Finance Manager application before we begin creating the project files.

## Technology Stack

### Frontend
- **Framework**: Next.js with TypeScript (Pages Router)
- **Package Manager**: Yarn
- **UI Library**: Material-UI (MUI)
- **Styling**: Tailwind CSS (utility-first CSS framework) + Material-UI
- **State Management**: React Context API / Zustand (lightweight)
- **Form Handling**: React Hook Form
- **Charts/Visualization**: Recharts or Chart.js
- **API Client**: Axios or fetch API

### Backend
- **Framework**: Django with Django REST Framework
- **Language**: Python (3.10 or higher)
- **Database**: PostgreSQL
- **ORM**: Django ORM (built-in)
- **Authentication**: Django REST Framework JWT or djangorestframework-simplejwt

### Development Tools
- **Frontend Package Manager**: Yarn
- **Backend Package Manager**: pip (Python package manager)
- **Virtual Environment**: venv or virtualenv (Python)
- **Code Quality**: ESLint, Prettier (frontend), Black, Flake8 (backend)
- **Process Manager**: concurrently (for running frontend and backend together)

## Environment Setup Steps

### 1. Prerequisites Check
- [ ] Node.js (v18 or higher) installed
- [ ] npm or yarn installed
- [ ] Python (3.10 or higher) installed
- [ ] pip (Python package manager) installed
- [ ] PostgreSQL installed and running

### 2. Project Structure
```
personal-finance-manager/
├── frontend/          # Next.js frontend application
│   ├── pages/         # Next.js Pages Router
│   ├── components/    # React components
│   ├── lib/           # Utilities and API clients
│   ├── public/        # Static assets
│   └── styles/        # CSS/Tailwind styles
├── backend/           # Django backend API
│   ├── manage.py      # Django management script
│   ├── config/        # Django project settings
│   ├── apps/          # Django apps (api, accounts, etc.)
│   ├── requirements.txt
│   └── .env           # Environment variables
├── package.json       # Root package.json for running both servers
├── README.md          # Project documentation
└── .gitignore         # Git ignore rules
```

### 3. Frontend Setup
- Initialize Next.js project with TypeScript and Pages Router: `yarn create next-app frontend --typescript --tailwind`
- Install additional dependencies:
  - `@mui/material @mui/icons-material @emotion/react @emotion/styled` (Material-UI)
  - `react-hook-form` (form handling)
  - `recharts` or `chart.js` (for financial charts)
  - `axios` (for API calls)
  - `date-fns` (for date handling)
  - `zustand` (optional, for state management)

### 4. Backend Setup
- Create Python virtual environment: `python -m venv venv`
- Activate virtual environment:
  - macOS/Linux: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- Initialize Django project: `django-admin startproject config .`
- Install dependencies (requirements.txt):
  - Django (latest stable version)
  - djangorestframework (Django REST Framework)
  - djangorestframework-simplejwt (JWT authentication)
  - psycopg2-binary (PostgreSQL adapter)
  - python-decouple (environment variables)
  - django-cors-headers (CORS middleware)
  - Pillow (if handling file uploads)
- Create Django apps:
  - `python manage.py startapp accounts` (user authentication)
  - `python manage.py startapp api` (main API endpoints)

### 5. Database Schema (Django Models)
- **User Model**: Django's built-in User model (or custom user model)
- **Transaction Model**: Income & Expenses
  - Fields: amount, type (income/expense), date, description, category, tags, user
- **Category Model**: Transaction categories
  - Fields: name, type (income/expense), color, icon, user
- **Tag Model**: Transaction tags
  - Fields: name, user
- **Budget Model**: Monthly/periodic budgets
  - Fields: category, amount, period (month/year), user
- **SavingsGoal Model**: Savings goals
  - Fields: name, target_amount, current_amount, deadline, user

### 6. Environment Variables
- Backend `.env` file for:
  - `SECRET_KEY` (Django secret key)
  - `DEBUG` (True/False)
  - `DATABASE_NAME` (PostgreSQL database name)
  - `DATABASE_USER` (PostgreSQL username)
  - `DATABASE_PASSWORD` (PostgreSQL password)
  - `DATABASE_HOST` (PostgreSQL host, default: localhost)
  - `DATABASE_PORT` (PostgreSQL port, default: 5432)
  - `ALLOWED_HOSTS` (comma-separated list)
  - `CORS_ALLOWED_ORIGINS` (frontend URL, e.g., http://localhost:3000)

### 7. Development Scripts

#### Root Level (Run Both Servers)
- `yarn dev` or `npm run dev` - **Run both frontend and backend together** (recommended)
- `yarn build` or `npm run build` - Build frontend for production
- `yarn start` or `npm run start` - Start both servers in production mode

#### Frontend Only (from frontend/ directory)
- `yarn dev` - Start Next.js development server (http://localhost:3000)
- `yarn build` - Build for production
- `yarn start` - Start production server

#### Backend Only (from backend/ directory)
- `python manage.py runserver` - Start Django development server (http://localhost:8000)
- `python manage.py makemigrations` - Create migration files
- `python manage.py migrate` - Apply database migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py collectstatic` - Collect static files (production)

## Next Steps (After Approval)
Once you approve this setup, I will:
1. Create the project directory structure
2. Initialize both frontend and backend projects
3. Set up all configuration files
4. Create the database schema
5. Set up basic routing and API structure
6. Create initial components for the main features

## User Preferences (Confirmed)
- ✅ **Package Manager**: Yarn for frontend
- ✅ **UI Library**: Material-UI (MUI)
- ✅ **Authentication**: Full authentication/user management system
- ✅ **Next.js Router**: Pages Router (pages/)
- ✅ **Django REST Framework**: Use Django models and querysets

## Single Command Setup

The project includes a root-level `package.json` with `concurrently` to run both frontend and backend servers with a single command.

### Quick Start
1. **Install root dependencies**: `yarn install` (installs concurrently)
2. **Run both servers**: `yarn dev`
   - Frontend: http://localhost:3000 (Next.js)
   - Backend: http://localhost:8000 (Django)

### How It Works
- **Root `package.json`**: Contains scripts to run both servers
- **`concurrently`**: Runs multiple commands simultaneously with colored output
- **`scripts/run-backend.js`**: Cross-platform script that automatically uses the correct Python executable from the virtual environment
  - macOS/Linux: Uses `backend/venv/bin/python`
  - Windows: Uses `backend/venv/Scripts/python.exe`

### Available Commands (from root directory)
- `yarn dev` - Start both frontend and backend in development mode
- `yarn build` - Build frontend for production
- `yarn start` - Start both servers in production mode
- `yarn install:all` - Install all dependencies (root + frontend)
- `yarn setup:backend` - Set up Python virtual environment and install backend dependencies

### Notes
- Make sure the backend virtual environment is created and activated before running `yarn dev`
- The script will automatically detect and use the correct Python executable
- Both servers will run in the same terminal with color-coded output (blue for frontend, green for backend)

---

**Ready to proceed?** Please review this plan and let me know if you'd like any changes before I create the files.

