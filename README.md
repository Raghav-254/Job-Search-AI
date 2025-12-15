# 🎯 AI Job Search Assistant

An AI-powered job search assistant that aggregates job listings from multiple sources and ranks them based on your profile.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![React](https://img.shields.io/badge/React-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![LangChain](https://img.shields.io/badge/LangChain-0.1-purple)

## ✨ Features

- **AI-Powered Profile Analysis**: Enter minimal information, get comprehensive job recommendations
- **Multi-Source Aggregation**: Fetches jobs from Greenhouse and Lever job boards
- **Smart Matching**: AI ranks jobs by match score (0-100%)
- **Deduplication**: No duplicate job listings
- **Company Selection**: Choose specific companies to search
- **Beautiful UI**: Modern, responsive design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with:
# OPENAI_API_KEY=sk-your-api-key-here

# Run the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at `http://localhost:5173`

## 📁 Project Structure

```
job-search/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration
│   ├── api/
│   │   ├── routes.py        # API endpoints
│   │   └── schemas.py       # Pydantic models
│   ├── agent/
│   │   ├── job_search_agent.py  # Main AI agent
│   │   └── tools/
│   │       ├── profile_expander.py
│   │       └── job_ranker.py
│   ├── scrapers/
│   │   ├── greenhouse.py
│   │   └── lever.py
│   └── services/
│       └── job_aggregator.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── ProfileForm.jsx
│   │   │   ├── JobResults.jsx
│   │   │   ├── JobCard.jsx
│   │   │   └── MatchScore.jsx
│   │   └── services/
│   │       └── api.js
│   └── package.json
└── README.md
```

## 🔌 API Endpoints

### `POST /api/analyze`

Analyze user profile and return matched jobs.

**Request:**
```json
{
  "role": "Frontend Engineer",
  "company": "Google",
  "years_of_experience": 5,
  "skills": ["React", "TypeScript"],
  "expected_salary": 200000,
  "location": "Remote",
  "target_companies": ["stripe", "vercel"]
}
```

**Response:**
```json
{
  "profile": {
    "original_role": "Frontend Engineer",
    "seniority_level": "Senior",
    "inferred_skills": ["React", "TypeScript", ...],
    "target_titles": ["Senior Frontend Engineer", ...]
  },
  "jobs": [
    {
      "id": "gh_stripe_123",
      "title": "Senior Frontend Engineer",
      "company": "Stripe",
      "match_score": 95,
      "insight": "Great match! Your Google experience...",
      "url": "https://..."
    }
  ],
  "total_jobs": 15
}
```

### `GET /api/companies`

Get list of available companies to search.

### `GET /api/health`

Health check endpoint.

## 🏢 Supported Companies

### Greenhouse
- Stripe, OpenAI, Figma, Discord, Netflix, Airbnb, Spotify, Coinbase, Instacart, DoorDash, Robinhood, Airtable, Canva, Databricks, Plaid

### Lever
- Vercel, Anthropic, Netlify, Postman, Retool, Linear, Loom, Mercury, Watershed, Notion

## 🧠 How It Works

1. **Profile Input**: User enters role, company, and experience
2. **AI Expansion**: GPT-4 expands minimal input to rich profile
3. **Job Fetching**: Scrapers fetch jobs from Greenhouse & Lever
4. **Deduplication**: Removes duplicate listings
5. **AI Ranking**: GPT-4 ranks jobs by match score
6. **Results**: User sees ranked jobs with insights

## 🛠️ Tech Stack

**Backend:**
- FastAPI (REST API)
- LangChain (AI orchestration)
- OpenAI GPT-4 (LLM)
- httpx (Async HTTP)
- Pydantic (Validation)

**Frontend:**
- React 18
- Vite
- TailwindCSS
- Framer Motion
- Lucide Icons

## 📝 Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...

# Optional
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

## 🔮 Future Enhancements

- [ ] Database for caching and tracking
- [ ] Application status tracking
- [ ] Email notifications for new jobs
- [ ] Resume parsing
- [ ] More job sources (RemoteOK, HN Hiring)

## 📄 License

MIT License


