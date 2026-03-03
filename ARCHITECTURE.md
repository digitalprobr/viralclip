# �️ Architecture — AutoClip AI

## Overview

AutoClip AI is a full-stack SaaS platform built with a microservices architecture. The system is fully containerized with Docker Compose (6 services) and uses asynchronous processing for video tasks.

---

## System Architecture

```mermaid
graph TB
    subgraph "Client"
        Browser["🌐 Browser"]
    end

    subgraph "Docker Network"
        subgraph "Frontend (Port 3001)"
            NextJS["Next.js 16<br/>React 19 + TypeScript<br/>Tailwind CSS + shadcn/ui"]
        end

        subgraph "API (Port 8080)"
            FastAPI["FastAPI<br/>Python 3.11<br/>Uvicorn"]
            Auth["Auth Module<br/>JWT + bcrypt"]
            Endpoints["REST Endpoints<br/>Clip, Jobs, Tasks"]
        end

        subgraph "Worker"
            Celery["Celery Worker<br/>Background Tasks"]
            Pipeline["Video Pipeline"]
        end

        subgraph "Data Layer"
            PG["PostgreSQL 15<br/>Users, Jobs, Tokens"]
            Redis["Redis<br/>Task Queue + Cache"]
        end

        subgraph "ML Container"
            Whisper["Whisper<br/>Speech-to-Text"]
        end
    end

    subgraph "External APIs"
        Gemini["Google Gemini"]
        DeepSeek["DeepSeek"]
        YouTube["YouTube<br/>(yt-dlp)"]
    end

    Browser -->|"HTTP/SSE"| NextJS
    NextJS -->|"REST API"| FastAPI
    FastAPI --> Auth
    FastAPI --> Endpoints
    FastAPI -->|"async"| PG
    FastAPI -->|"enqueue"| Redis
    Redis -->|"dequeue"| Celery
    Celery --> Pipeline
    Pipeline -->|"download"| YouTube
    Pipeline -->|"transcribe"| Whisper
    Pipeline -->|"analyze"| Gemini
    Pipeline -->|"analyze"| DeepSeek
    Pipeline -->|"update status"| PG
    Pipeline -->|"progress"| Redis

    style NextJS fill:#0070f3,color:#fff
    style FastAPI fill:#009688,color:#fff
    style Celery fill:#37b24d,color:#fff
    style PG fill:#336791,color:#fff
    style Redis fill:#dc382d,color:#fff
    style Whisper fill:#7c3aed,color:#fff
```

---

## Video Processing Pipeline

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant R as Redis
    participant W as Worker
    participant YT as YouTube
    participant AI as AI Engine
    participant FF as FFmpeg

    U->>F: Paste YouTube URL
    F->>A: POST /api/v1/clip
    A->>A: Validate URL & credits
    A->>R: Enqueue task
    A->>F: Return task_id
    F->>A: GET /tasks/{id}/stream (SSE)

    W->>R: Pick up task
    W->>YT: Download video + audio
    W->>W: Transcribe (Whisper)
    W->>AI: Analyze transcript
    AI->>W: Viral moments JSON
    
    loop For each clip
        W->>FF: Extract segment
        W->>FF: Face tracking crop
        W->>FF: Apply subtitles
        W->>FF: Add effects
        W->>FF: Export (9:16, 1:1)
    end

    W->>A: Update job status
    W->>R: Push progress events
    A->>F: SSE: clips ready
    F->>U: Display download links
```

---

## Database Schema

```mermaid
erDiagram
    USERS {
        int id PK
        varchar email UK
        varchar username UK
        varchar password_hash
        varchar name
        boolean email_verified
        int credits
        timestamp created_at
        timestamp updated_at
    }

    JOBS {
        int id PK
        int user_id FK
        varchar youtube_url
        varchar status
        varchar celery_task_id
        json result
        timestamp created_at
    }

    VERIFICATION_TOKENS {
        int id PK
        int user_id FK
        varchar token UK
        timestamp expires_at
        boolean used
    }

    USERS ||--o{ JOBS : "creates"
    USERS ||--o{ VERIFICATION_TOKENS : "owns"
```

---

## Authentication Flow

```mermaid
flowchart LR
    A["Register Page"] -->|"POST /signup"| B["Validate<br/>Password Rules"]
    B -->|"✅ Valid"| C["Hash Password<br/>(bcrypt)"]
    C --> D["Create User<br/>(50 credits)"]
    D --> E["Generate JWT"]
    E --> F["Set HTTPOnly<br/>Cookie"]
    F --> G["Redirect to<br/>Dashboard"]

    H["Login Page"] -->|"POST /login"| I["Find User<br/>by Email"]
    I -->|"✅ Found"| J["Verify Password<br/>(bcrypt)"]
    J -->|"✅ Match"| E
    J -->|"❌ No match"| K["401 Error"]
    I -->|"❌ Not found"| K
```

### Password Requirements
- Minimum 8 characters
- At least 1 uppercase letter (A-Z)
- At least 1 lowercase letter (a-z)
- At least 1 digit (0-9)
- At least 1 special character (!@#$%^&*)

---

## Docker Services

```mermaid
graph LR
    subgraph "docker-compose.yml"
        FE["frontend<br/>:3001"]
        API["api<br/>:8080"]
        WK["worker"]
        PG["postgres<br/>:5433"]
        RD["redis<br/>:6380"]
        TR["transformers"]
    end

    FE -->|"depends_on"| API
    API -->|"depends_on"| PG
    API -->|"depends_on"| RD
    WK -->|"depends_on"| PG
    WK -->|"depends_on"| RD

    style FE fill:#0070f3,color:#fff
    style API fill:#009688,color:#fff
    style WK fill:#37b24d,color:#fff
    style PG fill:#336791,color:#fff
    style RD fill:#dc382d,color:#fff
    style TR fill:#7c3aed,color:#fff
```

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `frontend` | Node 20 + Next.js 16 | 3001 → 3000 | Web application |
| `api` | Python 3.11 + FastAPI | 8080 → 8000 | REST API server |
| `worker` | Python 3.11 + Celery | — | Background processing |
| `postgres` | PostgreSQL 15 | 5433 → 5432 | Persistent storage |
| `redis` | Redis 7 Alpine | 6380 → 6379 | Task queue & cache |
| `transformers` | Python 3.11 | — | ML models (Whisper) |

---

## Frontend Architecture

```mermaid
graph TB
    subgraph "Next.js App Router"
        LP["/ Landing Page<br/>Hero, Features, Pricing, Reviews"]
        DB["/ Dashboard<br/>Job management"]
        Auth["/ Auth<br/>Login, Register"]
        Blog["/ Blog<br/>20 SEO articles"]
        Pages["/ Footer Pages<br/>About, Contact, Privacy,<br/>Terms, Docs, API, Roadmap,<br/>Changelog, Guides"]
    end

    subgraph "Components"
        Nav["Navbar"]
        UI["shadcn/ui<br/>Card, Button, Input"]
    end

    subgraph "API Client"
        Lib["lib/api.ts<br/>signup, login, createJob,<br/>getJobs, streamTask"]
    end

    LP --> Nav
    DB --> Nav
    Auth --> Lib
    DB --> Lib
    LP --> UI

    style LP fill:#0070f3,color:#fff
    style DB fill:#0070f3,color:#fff
    style Auth fill:#0070f3,color:#fff
    style Blog fill:#0070f3,color:#fff
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Celery for video tasks** | Video processing is CPU-intensive (5-10 min); async processing avoids blocking API |
| **SSE for progress** | Server-Sent Events provide real-time updates without WebSocket complexity |
| **bcrypt for passwords** | Industry standard, resistant to brute-force and rainbow table attacks |
| **Multiple AI engines** | Gemini, DeepSeek, Groq offer different analysis quality; user can choose |
| **Docker Compose** | Single-command deployment, consistent environments, easy scaling |
| **Next.js App Router** | File-based routing, server components, SEO metadata generation |
| **PostgreSQL async** | asyncpg provides non-blocking DB access matching FastAPI's async nature |
