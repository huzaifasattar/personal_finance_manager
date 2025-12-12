# Quick Start Guide

## First Time Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
SECRET_KEY=your-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=personal_finance
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF

# Create PostgreSQL database (run in psql)
# CREATE DATABASE personal_finance;

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser
```

### 2. Frontend Setup

```bash
cd frontend

# Dependencies are already installed, but if needed:
yarn install
```

### 3. Run the Application

From the root directory:

```bash
yarn dev
```

This starts both:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Next Steps

1. **Create a user account**: Go to http://localhost:3000/register
2. **Login**: Use your credentials at http://localhost:3000/login
3. **Start using**: The dashboard will show options for Transactions, Budgets, and Savings Goals

## Troubleshooting

### Database Connection Error
- Make sure PostgreSQL is running
- Check your database credentials in `backend/.env`
- Ensure the database exists: `CREATE DATABASE personal_finance;`

### Port Already in Use
- Change frontend port: `cd frontend && PORT=3001 yarn dev`
- Change backend port: `cd backend && python manage.py runserver 8001`

### Module Not Found Errors
- Backend: Make sure virtual environment is activated and dependencies are installed
- Frontend: Run `yarn install` in the frontend directory

