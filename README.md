# NSW Year 6 Lesson Planner

A comprehensive, full-stack lesson planning platform for NSW Year 6 teachers. Create Learning Experiences, generate differentiated worksheets, log student evidence, and track progress—all in one place.

## Features

✅ **Learning Experience Management** - Create and organize Learning Experiences with NESA outcomes
✅ **Weekly Planner** - Drag-drop lesson scheduling with status tracking
✅ **Worksheet Generation** - Auto-generate 4-tier differentiated worksheets (Mild/Medium/Spicy/Enrichment)
✅ **Support Files** - Generate teacher guides, answer sheets, and exemplar work as .docx
✅ **Evidence Tracking** - Log student observations and learning evidence
✅ **Progress Dashboard** - Track mastery levels and success criteria achievement
✅ **Class Pacing** - Monitor progress through units
✅ **Professional Design** - KRPS green branding throughout

## Tech Stack

**Backend:**
- Flask with SQLAlchemy ORM
- PostgreSQL database
- Redis caching
- JWT authentication
- python-docx for file generation

**Frontend:**
- React 18
- React Router for navigation
- Axios for API calls
- CSS Grid/Flexbox responsive design

**Deployment:**
- Docker & Docker Compose
- Local development setup

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/davidryan84/nsw-lesson-planner.git
cd nsw-lesson-planner
```

2. Start the application:
```bash
docker-compose up
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api/v1
- Database: localhost:5432

### First Time Setup

1. Register a teacher account at http://localhost:3000/register
2. Create your first Learning Experience
3. Schedule lessons in the Weekly Planner
4. Generate worksheets for lessons
5. Log student evidence and track progress

## Project Structure
```
nsw-lesson-planner/
├── backend/
│   ├── models/              # Database models
│   ├── services/            # Business logic
│   ├── api/                 # API endpoints
│   ├── tests/               # Unit tests
│   ├── config/              # Configuration
│   └── main.py              # Flask app factory
├── frontend/
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable components
│   │   ├── api/             # API client services
│   │   ├── context/         # React context (auth)
│   │   ├── styles/          # CSS files
│   │   └── App.js           # Main app component
│   ├── public/              # Static files
│   └── package.json         # Dependencies
└── docker-compose.yml       # Docker configuration
```

## API Endpoints

### Authentication
- POST `/auth/register` - Register new teacher
- POST `/auth/login` - Login teacher
- POST `/auth/refresh` - Refresh JWT token

### Learning Experiences
- POST `/learning-experiences` - Create LE
- GET `/learning-experiences` - Get all LEs
- GET `/learning-experiences/<id>` - Get specific LE
- PUT `/learning-experiences/<id>` - Update LE
- DELETE `/learning-experiences/<id>` - Delete LE

### Lessons
- POST `/lessons` - Create lesson
- GET `/lessons` - Get all lessons
- GET `/lessons?week_number=1` - Get lessons by week
- POST `/lessons/<id>/publish` - Publish lesson
- POST `/lessons/<id>/mark-taught` - Mark lesson as taught

### Worksheets
- POST `/worksheets/generate/<lesson_id>` - Generate worksheets
- GET `/worksheets/lesson/<lesson_id>` - Get worksheets

### Evidence
- POST `/evidence` - Log evidence
- GET `/evidence/student/<student_id>` - Get student evidence
- GET `/evidence/progress/student/<student_id>` - Get student progress

### Support Files
- POST `/support-files/generate/<lesson_id>` - Generate all files
- POST `/support-files/teacher-guide/<lesson_id>` - Generate guide
- POST `/support-files/answer-sheet/<lesson_id>` - Generate answers
- POST `/support-files/exemplar/<lesson_id>` - Generate exemplar

## Testing

Run backend tests:
```bash
docker-compose exec backend python -m pytest backend/tests/ -v
```

## Development

### Backend Development
```bash
docker-compose exec backend bash
python -m pytest backend/tests/ -v  # Run tests
```

### Frontend Development
The frontend auto-reloads on file changes thanks to React's development server.

## Deployment

See DEPLOYMENT.md for production deployment instructions.

## Documentation

- **Architecture**: See ARCHITECTURE.md
- **API Docs**: See API.md
- **Setup Guide**: See SETUP.md

## Features Roadmap

- [ ] Phase 3.1 - Frontend UI (✅ COMPLETE)
- [ ] Phase 3.2 - Student/Class management
- [ ] Phase 4 - Real Claude API integration for question generation
- [ ] Phase 5 - Mobile app
- [ ] Phase 6 - Real-time collaboration
- [ ] Phase 7 - Advanced analytics

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: david@example.com

## Acknowledgments

- NSW Education Standards Authority (NESA)
- Kellyville Ridge Public School
- Open source community

---

**Built with ❤️ by David Ryan**

Last Updated: February 23, 2026
