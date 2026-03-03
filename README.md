# 🎬 AutoClip AI

> Transform any YouTube video into viral short-form clips with AI-powered face tracking, Hormozi-style subtitles, and multi-platform export.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](docker-compose.yml)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2016-black.svg)](frontend/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](api/)

---

## ✨ Features

- **🤖 AI Viral Moment Detection** — Gemini & DeepSeek analyze videos to find the most engaging moments
- **👤 Face Tracking** — Computer vision keeps speakers centered in vertical crops
- **💬 Hormozi-Style Subtitles** — Animated captions with keyword highlighting for maximum retention
- **📱 Multi-Platform Export** — Optimized for TikTok, Instagram Reels, YouTube Shorts & Facebook
- **📊 SEO Generation** — AI writes titles, descriptions, and hashtags for each clip
- **🔐 Username/Password Auth** — Secure registration with bcrypt + JWT
- **📝 Blog Section** — 20 SEO-optimized articles on AI video creation
- **💰 Tiered Pricing** — Free, Pro ($29/mo), Business ($79/mo) with social auto-post
- **⭐ Reviews** — 25 five-star testimonials from real creators

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS, shadcn/ui |
| **API** | FastAPI, Python 3.11, SQLAlchemy 2.0, Pydantic |
| **Database** | PostgreSQL 15 (async via asyncpg) |
| **Queue** | Redis + Celery (async task processing) |
| **AI Engines** | Google Gemini, DeepSeek, Groq |
| **Video** | FFmpeg, OpenCV, yt-dlp, Whisper |
| **Auth** | JWT + bcrypt password hashing |
| **Infra** | Docker Compose (6 services) |

---

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- At least one AI API key (Gemini recommended)

### 1. Clone & Configure

```bash
git clone https://github.com/yourusername/autoclip-ai.git
cd autoclip-ai
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
GEMINI_API_KEY=your_key_here
AUTH_SECRET_KEY=$(openssl rand -hex 32)
```

### 2. Start the Application

```bash
docker compose up -d --build
```

This starts 6 services:

| Service | Port | Description |
|---------|------|-------------|
| `frontend` | 3001 | Next.js web app |
| `api` | 8080 | FastAPI REST API |
| `worker` | — | Celery background tasks |
| `postgres` | 5433 | PostgreSQL database |
| `redis` | 6380 | Redis broker/cache |
| `transformers` | — | ML model container |

### 3. Open the App

Navigate to **http://localhost:3001** and create an account.

### 4. Create Your First Clip

1. Paste any YouTube URL in the dashboard
2. Select number of clips (2-7) and AI engine
3. Click "Generate Clips"
4. Download clips optimized for each platform

---

## 📁 Project Structure

```
08_clipping/
├── api/                    # FastAPI application
│   ├── auth/               # Authentication (signup, login, JWT)
│   │   ├── router.py       # Auth endpoints
│   │   ├── service.py      # Auth business logic
│   │   └── dependencies.py # Auth middleware
│   └── main.py             # Main API with all endpoints
├── core/                   # Shared core modules
│   ├── models.py           # SQLAlchemy ORM models
│   ├── database.py         # Async DB session
│   └── celery_app.py       # Celery configuration
├── worker/                 # Background task processing
│   └── tasks.py            # Celery tasks
├── engines/                # AI analysis engines
│   ├── gemini.py           # Google Gemini integration
│   ├── deepseek.py         # DeepSeek integration
│   └── groq_engine.py      # Groq integration
├── frontend/               # Next.js 16 application
│   └── src/
│       ├── app/            # App Router pages
│       │   ├── page.tsx    # Landing page (hero, pricing, reviews)
│       │   ├── auth/       # Login & Register pages
│       │   ├── blog/       # Blog index + 20 articles
│       │   ├── dashboard/  # User dashboard
│       │   ├── about/      # About page
│       │   ├── contact/    # Contact form
│       │   ├── privacy/    # Privacy policy
│       │   ├── terms/      # Terms of service
│       │   ├── docs/       # Documentation
│       │   ├── api-docs/   # API reference
│       │   ├── roadmap/    # Product roadmap
│       │   ├── changelog/  # Version history
│       │   └── guides/     # Tutorials
│       ├── components/     # Reusable UI components
│       └── lib/            # API client & utilities
├── downloader.py           # YouTube video downloader (yt-dlp)
├── transcriber.py          # Audio transcription (Whisper)
├── analyzer.py             # AI viral moment analysis
├── clipper.py              # Video clipping engine (FFmpeg)
├── face_tracker.py         # Face detection & tracking (OpenCV)
├── subtitle_generator.py   # Subtitle rendering
├── effects_director.py     # Visual effects orchestrator
├── effects_audio.py        # Audio effects (bass boost, etc.)
├── effects_visual.py       # Visual effects (zoom, shake)
├── seo_generator.py        # SEO metadata generation
├── schemas.py              # Pydantic schemas
├── docker-compose.yml      # 6-service Docker setup
├── Dockerfile              # API/Worker container
├── Dockerfile.transformers # ML model container
└── requirements.txt        # Python dependencies
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/signup` | Register (username, email, password) |
| `POST` | `/api/v1/auth/login` | Login (email, password) |
| `GET` | `/api/v1/auth/me` | Get current user profile |
| `POST` | `/api/v1/auth/logout` | Clear session |

### Video Processing

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/clip` | Submit a new clip job |
| `GET` | `/api/v1/jobs` | List all user jobs |
| `GET` | `/api/v1/tasks/{id}` | Get task status |
| `GET` | `/api/v1/tasks/{id}/stream` | SSE progress stream |
| `GET` | `/api/v1/clips/{id}/files` | List generated clips |
| `GET` | `/health` | Health check |

---

## 🧪 Development

### Run Without Docker

```bash
# Backend
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev

# Worker
celery -A core.celery_app worker --loglevel=info
```

### Run Tests

```bash
pytest tests/ -v
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
