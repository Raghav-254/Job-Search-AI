# 🎯 AI Job Search Assistant

An AI-powered job search assistant that aggregates job listings from top companies and ranks them based on your profile.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![React](https://img.shields.io/badge/React-18-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-purple)

## 🎬 Demo


https://github.com/user-attachments/assets/f4557c34-a84d-43bf-8194-7902c167155a



## ✨ Features

- 🤖 **AI-Powered Matching** - GPT-4 ranks jobs by relevance to your profile
- 🏢 **150+ Companies** - Aggregates from Greenhouse & Lever job boards
- 🎯 **Smart Filtering** - Filters by experience, location, and skills
- 🌍 **Location Priority** - Preferred location jobs appear first
- ⚡ **Real-time Results** - Fast scraping with async processing

## 🚀 Quick Start

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Add your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key" > .env

uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` 🎉

## 🛠️ Tech Stack

| Backend | Frontend |
|---------|----------|
| FastAPI | React 18 |
| LangChain | Vite |
| OpenAI GPT-4 | TailwindCSS |
| httpx | Framer Motion |

## 📁 Structure

```
├── backend/
│   ├── agent/          # AI agent & tools
│   ├── scrapers/       # Greenhouse, Lever scrapers
│   ├── services/       # Job aggregation & filtering
│   └── api/            # FastAPI routes
└── frontend/
    └── src/components/ # React components
```

## 🔮 Roadmap

- [ ] More job sources (LinkedIn, Indeed)
- [ ] Resume parsing
- [ ] Application tracking
- [ ] Email notifications

---

Built with ❤️ for job seekers
