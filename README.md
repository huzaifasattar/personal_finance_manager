# Personal Finance Manager

A full-stack personal finance management application built with Next.js (frontend) and Django (backend).

## Features

- **Income & Expense Management**: Track your income and expenses with detailed transactions
- **Categories & Tags**: Organize transactions with custom categories and tags
- **Budgets**: Set and track monthly/yearly budgets for expense categories
- **Savings Goals**: Create and monitor savings goals with progress tracking
- **User Authentication**: Secure JWT-based authentication system

## Tech Stack

### Frontend
- Next.js 16 with TypeScript
- Material-UI (MUI) for components
- Tailwind CSS for styling
- Axios for API calls
- Recharts for data visualization

### Backend
- Django 5.2
- Django REST Framework
- PostgreSQL database
- JWT authentication (djangorestframework-simplejwt)
- CORS headers for cross-origin requests

## Prerequisites

Before you begin, ensure you have the following installed:

- Node.js (v18 or higher)
- Yarn package manager
- Python (3.10 or higher)
- PostgreSQL database
- pip (Python package manager)

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
cd personal-finance-manager
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env
# Edit .env with your database credentials

# Create PostgreSQL database
# (Run this in PostgreSQL)
# CREATE DATABASE personal_finance;

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (already done if you ran yarn install from root)
yarn install

# Create .env.local file (optional, for custom API URL)
# NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 4. Environment Variables

#### Backend (.env file in backend/ directory)
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=personal_finance
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### Frontend (.env.local file in frontend/ directory - optional)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Running the Application

### Option 1: Run Both Servers Together (Recommended)

From the root directory:

```bash
yarn dev
```

This will start:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Option 2: Run Servers Separately

**Frontend:**
```bash
cd frontend
yarn dev
```

**Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python manage.py runserver
```

## Available Scripts

### Root Level
- `yarn dev` - Run both frontend and backend
- `yarn install:all` - Install all dependencies
- `yarn setup:backend` - Set up backend virtual environment

### Frontend
- `yarn dev` - Start development server
- `yarn build` - Build for production
- `yarn start` - Start production server

### Backend
- `python manage.py runserver` - Start development server
- `python manage.py makemigrations` - Create migration files
- `python manage.py migrate` - Apply migrations
- `python manage.py createsuperuser` - Create admin user

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/update/` - Update user profile

### Transactions
- `GET /api/transactions/` - List transactions
- `POST /api/transactions/` - Create transaction
- `GET /api/transactions/{id}/` - Get transaction
- `PATCH /api/transactions/{id}/` - Update transaction
- `DELETE /api/transactions/{id}/` - Delete transaction
- `GET /api/transactions/summary/` - Get transaction summary

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category
- `GET /api/categories/{id}/` - Get category
- `PATCH /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Budgets
- `GET /api/budgets/` - List budgets
- `POST /api/budgets/` - Create budget
- `GET /api/budgets/{id}/` - Get budget
- `PATCH /api/budgets/{id}/` - Update budget
- `DELETE /api/budgets/{id}/` - Delete budget

### Savings Goals
- `GET /api/savings-goals/` - List savings goals
- `POST /api/savings-goals/` - Create savings goal
- `GET /api/savings-goals/{id}/` - Get savings goal
- `PATCH /api/savings-goals/{id}/` - Update savings goal
- `DELETE /api/savings-goals/{id}/` - Delete savings goal
- `POST /api/savings-goals/{id}/add_amount/` - Add amount to goal

## Project Structure

```
personal-finance-manager/
├── frontend/              # Next.js frontend
│   ├── pages/             # Next.js pages
│   ├── lib/               # Utilities and API clients
│   │   ├── api/           # API client functions
│   │   └── theme.ts       # Material-UI theme
│   └── styles/            # CSS styles
├── backend/               # Django backend
│   ├── config/            # Django project settings
│   ├── accounts/          # Authentication app
│   ├── api/               # Main API app
│   │   ├── models.py      # Database models
│   │   ├── serializers.py # DRF serializers
│   │   ├── views.py       # API viewsets
│   │   └── urls.py        # API URLs
│   └── requirements.txt   # Python dependencies
├── scripts/               # Utility scripts
└── package.json           # Root package.json for running both servers
```

## Development

### Database Migrations

After making changes to models:

```bash
cd backend
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### Creating Admin User

```bash
cd backend
source venv/bin/activate
python manage.py createsuperuser
```

Then access Django admin at: http://localhost:8000/admin/

## License

This project is private and proprietary.

