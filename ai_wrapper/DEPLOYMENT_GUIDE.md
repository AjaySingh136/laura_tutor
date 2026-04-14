# AI Tutor - Complete Setup & Deployment Guide

## 📋 Overview

This is a complete end-to-end implementation of an AI tutoring platform. The stack includes:

- **Backend**: FastAPI (Python) with LangChain for AI orchestration
- **Frontend**: Next.js 14 (React/TypeScript)
- **Database**: PostgreSQL
- **Cache**: Redis
- **LLM**: OpenAI GPT-4 Turbo
- **Deployment**: Docker, can be deployed to AWS, Heroku, Railway, Vercel

---

## 🚀 Quick Start (5 minutes)

### Prerequisites

- macOS with Homebrew (or any Unix-like system)
- Docker & Docker Compose installed
- OpenAI API key

### Step 1: Clone & Setup

\`\`\`bash
cd /Users/ajaynegi/ai_wrapper

# Create .env file with your OpenAI API key
cp backend/.env.example backend/.env

# Edit .env and add your OpenAI API key
nano backend/.env
# Add: OPENAI_API_KEY=your_key_here
\`\`\`

### Step 2: Start with Docker Compose (All services in one command)

\`\`\`bash
cd docker
docker-compose up --build
\`\`\`

Wait for all services to be healthy. You'll see:
- Backend ready at: http://localhost:8000
- Frontend ready at: http://localhost:3000
- PostgreSQL at: localhost:5432
- Redis at: localhost:6379

### Step 3: Test

Open http://localhost:3000 in your browser and start learning!

---

## 🏗️ Manual Setup (For Development)

### Backend Setup

\`\`\`bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database (PostgreSQL must be running)
# Create .env first
cp .env.example .env
nano .env  # Add your credentials

# Run migrations (creates tables)
python -c "from app.database import init_db; init_db()"

# Start backend
python main.py
# Backend running at http://localhost:8000
\`\`\`

### Frontend Setup

\`\`\`bash
# In another terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local

# Start frontend
npm run dev
# Frontend running at http://localhost:3000
\`\`\`

### Database Setup (if not using Docker)

\`\`\`bash
# Install PostgreSQL (macOS)
brew install postgresql

# Start PostgreSQL
brew services start postgresql

# Create database and user
createdb ai_tutor_dev
psql ai_tutor_dev -c "CREATE USER tutor_user WITH PASSWORD 'tutor_password';"
psql ai_tutor_dev -c "GRANT ALL PRIVILEGES ON DATABASE ai_tutor_dev TO tutor_user;"

# For Redis
brew install redis
brew services start redis
\`\`\`

---

## 📁 Project Structure

\`\`\`
ai_wrapper/
├── backend/
│   ├── main.py               # FastAPI app entry
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   └── app/
│       ├── config.py         # Configuration
│       ├── database.py       # Database setup
│       ├── models.py         # SQLAlchemy models
│       ├── schemas.py        # Pydantic schemas
│       ├── services/
│       │   ├── llm_service.py      # AI tutoring logic
│       │   └── youtube_service.py  # YouTube integration
│       └── api/
│           └── routes.py     # API endpoints
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── src/
│   │   ├── app/              # Next.js pages
│   │   ├── components/       # React components
│   │   └── lib/              # Utilities, API client
│   └── Dockerfile
└── docker/
    ├── Dockerfile.backend
    ├── docker-compose.yml
    └── README.md (this file)
\`\`\`

---

## 🔌 API Endpoints

### Sessions
- `POST /api/v1/sessions` - Create new tutoring session
- `GET /api/v1/sessions/{session_id}` - Get session details
- `GET /api/v1/sessions/{session_id}/messages` - Get chat history

### Chat
- `POST /api/v1/sessions/{session_id}/chat` - Send message to tutor

### Assessment
- `POST /api/v1/sessions/{session_id}/assessment/{question_id}/answer` - Submit quiz answer

### YouTube
- `POST /api/v1/youtube/transcript` - Extract transcript from YouTube URL

### Health
- `GET /api/v1/health` - Check API status

---

## 🧪 Testing the API with cURL

\`\`\`bash
# Create a session
curl -X POST http://localhost:8000/api/v1/sessions \\
  -H "Content-Type: application/json" \\
  -d '{
    "topic": "Photosynthesis",
    "difficulty_level": "beginner",
    "enable_assessment": true
  }'

# Response will include session_id, copy it and use below:

# Send a message
curl -X POST http://localhost:8000/api/v1/sessions/YOUR_SESSION_ID/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "What is photosynthesis? Explain like I am 5."}'

# Get chat history
curl http://localhost:8000/api/v1/sessions/YOUR_SESSION_ID/messages
\`\`\`

---

## 🚀 Deployment Options

### Option 1: Deploy to Railway (Recommended for MVP - $5/month)

1. **Sign up** at railway.app
2. **Connect GitHub** repo
3. **Create services**:
   - PostgreSQL (built-in)
   - Backend (from backend/Dockerfile)
   - Frontend (from frontend/Dockerfile)
4. **Set environment variables**:
   - OPENAI_API_KEY
   - DATABASE_URL (auto-set by Railway)
   - REDIS_URL (Railway Redis plugin)

### Option 2: Deploy to AWS (More complex but scalable)

\`\`\`bash
# 1. Create ECR repositories
aws ecr create-repository --repository-name ai-tutor-backend
aws ecr create-repository --repository-name ai-tutor-frontend

# 2. Build and push images
docker build -t ai-tutor-backend -f docker/Dockerfile.backend .
docker tag ai-tutor-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-tutor-backend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-tutor-backend:latest

# 3. Create RDS PostgreSQL instance
# 4. Create ElastiCache Redis cluster
# 5. Deploy using ECS or Kubernetes
\`\`\`

### Option 3: Deploy with Vercel + Heroku (Quick & Free tier option)

\`\`\`bash
# Frontend: Vercel (free)
cd frontend
vercel --prod

# Backend: Heroku (free tier ending but can use alternatives)
# Or use Railway/Render instead
\`\`\`

### Option 4: Deploy on Your Own Server

\`\`\`bash
# 1. SSH into your server
ssh user@your-server.com

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Clone repository
git clone <your-repo-url>
cd ai_wrapper

# 4. Create .env
nano backend/.env

# 5. Start with compose
cd docker
docker-compose up -d

# 6. Setup reverse proxy (nginx)
# Install nginx and configure to forward to localhost:3000 and :8000
\`\`\`

---

## 🔒 Environment Variables Checklist

### Backend (.env)
- [ ] OPENAI_API_KEY - from openai.com
- [ ] DATABASE_URL - PostgreSQL connection string
- [ ] REDIS_URL - Redis connection string
- [ ] SECRET_KEY - Generate: `openssl rand -hex 32`
- [ ] ALLOWED_ORIGINS - Frontend URL

### Frontend (.env.local)
- [ ] NEXT_PUBLIC_API_URL - Backend URL

---

## 📊 Monitoring & Logs

\`\`\`bash
# View backend logs
docker logs ai_tutor_backend -f

# View frontend logs
docker logs ai_tutor_frontend -f

# View database logs
docker logs ai_tutor_db -f

# Check running services
docker ps

# Stop services
docker-compose down

# Remove all data (careful!)
docker-compose down -v
\`\`\`

---

## 🐛 Troubleshooting

### Issue: "Connection refused" to OpenAI
**Solution**: Check your OPENAI_API_KEY is valid and set correctly in .env

### Issue: Database connection fails
**Solution**: 
- Ensure PostgreSQL is running: `brew services list`
- Check DATABASE_URL in .env
- Verify credentials: `psql -U tutor_user -d ai_tutor_dev`

### Issue: Frontend can't reach backend
**Solution**: Check NEXT_PUBLIC_API_URL matches backend host/port

### Issue: YouTube transcript fails
**Solution**: Video must have captions enabled. Try different videos.

---

## 📈 Optimization & Scaling

### For Production:
1. Enable HTTPS/SSL
2. Add rate limiting
3. Implement caching with Redis
4. Use connection pooling
5. Add monitoring (Sentry, New Relic)
6. Implement user authentication properly
7. Add image caching strategy
8. Use CDN for frontend
9. Implement API versioning
10. Add comprehensive logging

### Performance Improvements:
- Add conversation summarization for long sessions
- Cache common topics
- Use WebSockets for real-time updates  
- Implement streaming responses
- Add database indexing

---

## 💡 Next Steps

1. **Add User Authentication** - Implement proper JWT auth
2. **Add Social Features** - Leaderboards, friend learning sessions
3. **Mobile App** - React Native version
4. **Multimodal Output** - Generate images/graphs with DALL-E
5. **Analytics Dashboard** - Track learning progress
6. **Admin Panel** - Manage sessions, analytics, users
7. **Internationalization** - Support multiple languages
8. **Voice Input/Output** - Speech-to-text and text-to-speech

---

## 📞 Support & Questions

For issues or questions:
1. Check existing GitHub issues
2. Review the documentation
3. Test with provided cURL examples
4. Check logs with `docker logs <service>`

---

## 📜 License

MIT License - Feel free to use and modify!

---

**Happy Learning! 🎓**
