# Setup Instructions for macOS

## Prerequisites

Ensure you have:
- macOS (Monterey or newer)
- Homebrew installed
- Terminal access

## Quick Start (Complete setup in 5 minutes)

### 1. Install Dependencies

\`\`\`bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Docker
brew install docker

# Or download Docker Desktop from https://www.docker.com/products/docker-desktop

# Start Docker (if installed via brew)
docker run --rm hello-world
\`\`\`

### 2. Setup Project

\`\`\`bash
# Navigate to project
cd /Users/ajaynegi/ai_wrapper

# Create environment file
cp backend/.env.example backend/.env

# Edit with your OpenAI API key
open backend/.env
# Edit OPENAI_API_KEY=sk-... (from https://platform.openai.com/api-keys)
\`\`\`

### 3. Start Everything

\`\`\`bash
# Start all services (Docker Compose)
cd docker
docker-compose up --build

# Wait for all services to be 'healthy'
# You should see:
# - postgres: accepting connections
# - redis: ready to accept connections  
# - backend: INFO:     Started server process
# - frontend: ready - started server on 0.0.0.0:3000
\`\`\`

### 4. Access Application

Open in browser:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/api/v1/health

---

## Manual Setup (Without Docker)

### Backend Setup

\`\`\`bash
# Navigate to backend
cd backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python -c "from app.database import init_db; init_db()"

# Start backend
python main.py
# Running at http://localhost:8000
\`\`\`

### Frontend Setup (New Terminal)

\`\`\`bash
# Navigate to frontend
cd frontend

# Install Node dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local

# Start frontend
npm run dev
# Running at http://localhost:3000
\`\`\`

### Database Setup (New Terminal - First time only)

\`\`\`bash
# Install PostgreSQL
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create database
createdb ai_tutor_dev

# Create database user
psql ai_tutor_dev << EOF
CREATE USER tutor_user WITH PASSWORD 'tutor_password';
GRANT ALL PRIVILEGES ON DATABASE ai_tutor_dev TO tutor_user;
EOF

# Verify connection
psql -U tutor_user -d ai_tutor_dev -c "SELECT version();"

# Install and start Redis
brew install redis
brew services start redis

# Verify Redis
redis-cli ping
# Should return: PONG
\`\`\`

---

## First Time Use

### 1. Get OpenAI API Key

1. Go to https://platform.openai.com/account/api-keys
2. Create new secret key
3. Copy it
4. Add to `backend/.env`: `OPENAI_API_KEY=sk-...`

### 2. Test the Application

\`\`\`bash
# In a terminal, test backend API
curl http://localhost:8000/api/v1/health

# Should return:
# {"status":"healthy","version":"1.0.0"}

# Open frontend in browser
open http://localhost:3000
\`\`\`

### 3. Try a Learning Session

1. Open http://localhost:3000
2. Enter topic: "Python Programming" (or any topic)
3. Select difficulty: "Beginner"
4. Click "Start Learning"
5. Type: "What is a variable?"
6. See AI tutor explain it!

---

## Managing Services

\`\`\`bash
# Using Docker Compose
cd docker

# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Reset everything (including data)
docker-compose down -v

# Without Docker - Using Homebrew services

# Start services at boot
brew services start postgresql
brew services start redis

# Check status
brew services list

# Stop services
brew services stop postgresql
brew services stop redis
\`\`\`

---

## Development Workflow

\`\`\`bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Database (if needed)
# Just keep PostgreSQL and Redis running via Homebrew

# Terminal 4: Useful commands
cd /Users/ajaynegi/ai_wrapper

# Test API
curl -X POST http://localhost:8000/api/v1/sessions \\
  -H "Content-Type: application/json" \\
  -d '{
    "topic": "Machine Learning",
    "difficulty_level": "beginner"
  }'
\`\`\`

---

## Common Issues on macOS

### Issue: "command not found: python3"
\`\`\`bash
brew install python3
\`\`\`

### Issue: PostgreSQL won't start
\`\`\`bash
brew services restart postgresql
# Or reinstall:
brew uninstall postgresql
brew install postgresql
initdb /usr/local/var/postgres
\`\`\`

### Issue: Port 3000 or 8000 already in use
\`\`\`bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change ports in code
\`\`\`

### Issue: "Cannot connect to Docker daemon"
\`\`\`bash
# Start Docker Desktop or daemon
open /Applications/Docker.app

# Or if installed via Homebrew
colima start  # or similar for your setup
\`\`\`

### Issue: OpenAI API key not working
1. Verify key is valid: https://platform.openai.com/account/api-keys
2. Check .env file has `OPENAI_API_KEY=sk-...` (exact key)
3. Restart backend: `python main.py`
4. Check logs for errors

---

## Useful Commands

\`\`\`bash
# Check what's running
ps aux | grep python
ps aux | grep node

# Database operations
psql ai_tutor_dev -U tutor_user

# Redis operations
redis-cli
> KEYS *
> FLUSHALL

# View logs
tail -f ~/Library/Logs/Homebrew/*

# Clean up
rm -rf backend/venv
rm -rf frontend/node_modules
npm cache clean --force
\`\`\`

---

## Next Steps

1. ✅ Setup complete
2. 📚 [Read Full Deployment Guide](./DEPLOYMENT_GUIDE.md)
3. 🚀 [Deploy to Production](./DEPLOYMENT_GUIDE.md#-deployment-options)
4. 📖 [Explore API Documentation](http://localhost:8000/docs)
5. 💡 [Customize & Extend](./DEVELOPMENT.md)

---

**You're all set! Start learning with AI Tutor! 🎓**
