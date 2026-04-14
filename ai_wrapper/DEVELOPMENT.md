# Development Guide

This guide explains how to develop and extend the AI Tutor platform.

## Project Structure Overview

### Backend Structure
```
backend/
├── main.py                    # FastAPI app entry point
├── app/
│   ├── config.py             # Settings & configuration
│   ├── database.py           # Database setup
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas (validation)
│   ├── api/
│   │   └── routes.py         # All API endpoints
│   └── services/
│       ├── llm_service.py    # AI tutoring logic
│       └── youtube_service.py # YouTube integration
└── requirements.txt          # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx        # Root layout
│   │   └── page.tsx          # Home page
│   ├── components/
│   │   ├── SessionStart.tsx  # Start tutorial form
│   │   ├── ChatInterface.tsx # Main chat UI
│   │   └── Providers.tsx     # App providers
│   └── lib/
│       ├── api.ts           # API client (axios)
│       └── store.ts         # State management (Zustand)
└── package.json            # Dependencies
```

---

## 🔧 Common Development Tasks

### 1. Adding a New API Endpoint

**File**: `backend/app/api/routes.py`

```python
from fastapi import APIRouter

# Add to existing router or create new one
@router.post("/v1/your-endpoint")
async def your_endpoint(request_data: YourSchema, db: Session = Depends(get_db)):
    """Your endpoint description"""
    # Your logic here
    return {"result": "success"}
```

### 2. Adding a Database Model

**File**: `backend/app/models.py`

```python
from sqlalchemy import Column, String, Integer
from app.database import Base

class YourModel(Base):
    __tablename__ = "your_table"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    # Add your fields
```

Schema (validation):

**File**: `backend/app/schemas.py`

```python
from pydantic import BaseModel

class YourSchema(BaseModel):
    name: str
    # Add your fields
```

### 3. Modifying AI Behavior

**File**: `backend/app/services/llm_service.py`

```python
def create_system_prompt(self, topic: str, difficulty_level: str) -> str:
    """Customize how the AI tutor responds"""
    base_prompt = f"""You are a tutor for {topic}...
    [Customize your prompt here]
    """
    return base_prompt
```

### 4. Adding Frontend Components

**File**: `frontend/src/components/YourComponent.tsx`

```typescript
'use client';

import { useState } from 'react';

export function YourComponent() {
  const [state, setState] = useState('');
  
  return (
    <div className="p-4">
      {/* Your JSX */}
    </div>
  );
}
```

Use in page:

**File**: `frontend/src/app/page.tsx`

```typescript
import { YourComponent } from '@/components/YourComponent';

export default function Home() {
  return <YourComponent />;
}
```

### 5. Making API Calls from Frontend

**Using the API client**:

```typescript
import { tutorApi } from '@/lib/api';

// In your component
const response = await tutorApi.sendMessage(sessionId, message);
```

**Or add new endpoint**:

**File**: `frontend/src/lib/api.ts`

```typescript
export const tutorApi = {
  // Existing endpoints...
  
  yourNewEndpoint: (param: string) =>
    api.post('/v1/your-endpoint', { param }),
};
```

---

## 🧪 Testing

### Backend Testing

**Create test file**: `backend/tests/test_routes.py`

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_session():
    response = client.post("/api/v1/sessions", json={
        "topic": "Test Topic",
        "difficulty_level": "beginner"
    })
    assert response.status_code == 200
    assert "id" in response.json()
```

**Run tests**:
```bash
cd backend
pip install pytest
pytest
```

### Frontend Testing

**Create test file**: `frontend/src/components/YourComponent.test.tsx`

```typescript
import { render, screen } from '@testing-library/react';
import { YourComponent } from './YourComponent';

test('renders component', () => {
  render(<YourComponent />);
  expect(screen.getByText(/expected text/i)).toBeInTheDocument();
});
```

**Run tests**:
```bash
cd frontend
npm test
```

---

## 🎨 Styling & UI

### TailwindCSS Classes

Already configured. Use class names:

```jsx
<div className="bg-blue-500 p-4 rounded-lg hover:bg-blue-600 transition-colors">
  Styled with TailwindCSS
</div>
```

### Custom Styles

**File**: `frontend/src/globals.css`

```css
.custom-class {
  @apply bg-white rounded-lg shadow-md p-4;
}
```

---

## 🚀 Performance Optimization

### Backend
1. Add database indexing on frequently queried fields
2. Use pagination for large datasets
3. Cache responses with Redis
4. Profile with `cProfile`

### Frontend
1. Use lazy loading for components
2. Optimize images
3. Code splitting with Next.js dynamic imports
4. Minimize bundle size

---

## 🔐 Security

### Backend
- Always validate input (Pydantic schemas)
- Use parameterized queries (SQLAlchemy ORM)
- Implement rate limiting
- Add authentication middleware

### Frontend
- Never store sensitive data in localStorage
- Use HTTPS in production
- Sanitize user input before display
- Implement CSRF tokens

---

## 🐛 Debugging

### Backend Debugging

```bash
# Print logs
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")

# Use debugger
import pdb
pdb.set_trace()

# FastAPI interactive docs
# Go to http://localhost:8000/docs
```

### Frontend Debugging

```typescript
// Console logging
console.log('Debug:', value);

// React DevTools extension
// Install from Chrome/Firefox extension store

// VS Code debugger config (.vscode/launch.json)
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js",
      "type": "node",
      "request": "launch",
      "skipFiles": ["<node_internals>/**"],
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"]
    }
  ]
}
```

---

## 📦 Adding Dependencies

### Python Packages

```bash
cd backend

# Add to requirements.txt
pip install package_name
pip freeze > requirements.txt
```

### NPM Packages

```bash
cd frontend

# Install and add to package.json
npm install package_name
```

---

## 🔄 Version Control

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes, commit
git add .
git commit -m "feat: description of changes"

# Push and create pull request
git push origin feature/your-feature
```

### Commit Messages
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code restructuring
- `perf:` Performance improvements
- `test:` Test additions/changes

---

## 📝 Database Migrations

If you add new models, you need migrations:

```bash
# Use Alembic (add to requirements.txt later)
# For MVP, just delete the old DB and let it recreate:

cd backend
rm -f database.db  # SQLite if using that
python -c "from app.database import init_db; init_db()"
```

---

## 🌐 Environment Variables

Add to `.env` file:

```env
# Backend (backend/.env)
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
DEBUG=True

# Frontend (frontend/.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

## 📚 Additional Resources

- FastAPI: https://fastapi.tiangolo.com/tutorial/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Next.js: https://nextjs.org/learn
- React: https://react.dev/
- TailwindCSS: https://tailwindcss.com/docs
- TypeScript: https://www.typescriptlang.org/docs/

---

## 🆘 Common Issues

### Import errors in Python
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Hot reload not working
```bash
# Frontend
# Restart: Ctrl+C and run again
npm run dev

# Backend
# Restart: Ctrl+C and run again
python main.py
```

### Database errors
```bash
# Check connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

---

Happy coding! 🚀
