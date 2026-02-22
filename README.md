# NSW Lesson Planner Platform

Professional lesson planning platform for NSW teachers.

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Setup (5 minutes)

1. **Clone and navigate:**
```bash
cd nsw-lesson-planner
```

2. **Start services:**
```bash
docker-compose up
```

3. **Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Database: localhost:5432

4. **Test API:**
```bash
# Register
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## Architecture

- **Backend:** Flask + SQLAlchemy + PostgreSQL
- **Frontend:** React + Axios
- **Database:** PostgreSQL
- **Cache:** Redis
- **Containerization:** Docker

## Features

- Teacher authentication
- Worksheet creation and management
- Student management
- Evidence/observation logging
- Weekly lesson planning
- Support files generation

## Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Environment Variables

See `.env.example` files in backend/ and frontend/ directories.

## Next Steps

1. Customize for your school
2. Add your branding
3. Extend with additional features
4. Deploy to AWS or preferred platform
