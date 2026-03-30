# IntervYou — MVP Documentation

## Project Overview

IntervYou is an AI-powered interview practice platform where users answer interview questions via voice or text, receive real-time AI analysis on fluency, relevance and delivery, and track their progress over time. It includes a local LLM-powered AI coaching chatbot for personalised interview advice.

---

## Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | Angular | 17.3.12 | Standalone SPA with lazy-loaded routes |
| UI Styling | Custom SCSS | — | Design system (primary #4f46e5, dark #0f172a) |
| UI Components | Angular Material | 17.3.10 | Form fields, cards, toolbar |
| Charts | Chart.js + ng2-charts | 4.4.7 / 5.0.4 | Radar + line score charts |
| Backend | Flask | 3.x | REST API server |
| Auth | Flask-JWT-Extended | 4.7.1 | Access + refresh tokens, token blocklist |
| ORM | Flask-SQLAlchemy | 3.1.1 | Database models |
| Database | SQLite | — | Local persistent storage (intervyou.db) |
| Speech-to-Text | OpenAI Whisper | base model | Audio transcription |
| Audio Analysis | Librosa | — | Speaking rate, pause detection |
| NLP Scoring | Sentence-BERT | all-MiniLM-L6-v2 | Semantic relevance scoring |
| AI Chatbot | Ollama + LangChain | qwen3:8b | Local LLM interview coach |
| Process Runner | concurrently | 9.x | Run backend + frontend together |

---

## How to Run

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama installed with qwen3:8b model (`ollama pull qwen3:8b`)

### Quick Start (both servers)
```bash
npm run dev
```
This starts:
- **Backend** on http://localhost:5000
- **Frontend** on http://localhost:4200

### Individual Commands
```bash
# Backend only
cd backend && python app.py

# Frontend only
cd intervyou-frontend && npm start

# Ollama (if not already running)
ollama serve
```

### First-Time Setup
```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd intervyou-frontend
npm install
```

---

## Project Structure

```
intervYou/
├── package.json                  # Root scripts (npm run dev)
├── mvp.md                        # This file
├── README.md                     # Quick reference
│
├── backend/
│   ├── app.py                    # Flask app factory, seed data, JWT config
│   ├── models.py                 # SQLAlchemy models (User, Question, Session, Response, TokenBlocklist)
│   ├── requirements.txt          # Python dependencies
│   ├── routes/
│   │   ├── auth.py               # Register, login, logout, refresh, verify email, forgot/reset password
│   │   ├── questions.py          # GET questions filtered by difficulty level
│   │   ├── sessions.py           # Start, list, get, complete sessions
│   │   ├── analysis.py           # Submit audio (full AI pipeline) + submit text (NLP only)
│   │   ├── user.py               # Dashboard stats, profile, change password, delete account
│   │   ├── chatbot.py            # AI coach message + session feedback via Ollama
│   │   └── misc.py               # Contact form, health check
│   ├── services/
│   │   ├── transcription.py      # Whisper speech-to-text (lazy-loaded)
│   │   ├── audio_analysis.py     # Librosa duration/pause + transcript filler/rate analysis
│   │   ├── nlp_analysis.py       # Sentence-BERT cosine similarity scoring (lazy-loaded)
│   │   ├── feedback.py           # Rule-based feedback generator + overall score computation
│   │   └── chatbot.py            # Ollama LLM integration (InterviewCoach class)
│   └── uploads/                  # Saved audio recordings (.webm)
│
└── intervyou-frontend/
    ├── package.json              # Angular 17 dependencies (pinned versions)
    ├── angular.json              # Build config
    ├── src/
    │   ├── index.html            # Entry HTML with Inter font
    │   ├── styles.scss           # Global styles, CSS variables, Material theme
    │   └── app/
    │       ├── app.component.*   # App shell: navbar (all pages) + router-outlet + chatbot widget
    │       ├── app.config.ts     # Providers: router, HTTP client, JWT interceptor, animations
    │       ├── app.routes.ts     # All routes with lazy loading + auth guards
    │       ├── core/
    │       │   ├── auth.service.ts    # Login, register, logout, refresh, verify, forgot/reset password
    │       │   ├── api.service.ts     # All HTTP calls to Flask API
    │       │   ├── jwt.interceptor.ts # Attaches Bearer token, handles 401 → logout
    │       │   └── auth.guard.ts      # CanActivate guard → redirects to /auth/signin
    │       ├── shared/components/
    │       │   ├── audio-recorder/    # MediaRecorder component (mic button, timer, blob output)
    │       │   ├── score-card/        # Colour-coded score display (green/amber/red)
    │       │   └── chatbot/           # Floating AI coach widget (Ollama-powered)
    │       └── pages/
    │           ├── home/              # Landing page: hero, levels, features, how-it-works, CTA, footer
    │           ├── auth/signin/       # Sign in with email + password
    │           ├── auth/signup/       # Sign up with validation + confirm password
    │           ├── contact/           # Contact form
    │           ├── dashboard/         # Welcome, stats, quick actions, recent sessions
    │           ├── practice/
    │           │   ├── practice-setup/    # Job role + difficulty level selection
    │           │   ├── practice-session/  # Live interview: question → record/type → AI analysis → feedback
    │           │   └── practice-results/  # Session results: radar chart, score breakdown, per-question detail
    │           ├── history/           # All sessions table + score progress line chart
    │           └── settings/          # Profile edit, change password
```

---

## Database Schema

### users
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| email | VARCHAR(120) | Unique, indexed |
| password_hash | VARCHAR(256) | werkzeug pbkdf2 |
| name | VARCHAR(100) | |
| email_verified | BOOLEAN | Default false |
| verification_token | VARCHAR(128) | Nullable |
| reset_token | VARCHAR(128) | Nullable |
| reset_token_expires | DATETIME | Nullable, 1-hour expiry |
| created_at | DATETIME | Auto |
| updated_at | DATETIME | Auto on update |

### token_blocklist
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| jti | VARCHAR(36) | Indexed, revoked JWT ID |
| created_at | DATETIME | |

### questions
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| text | TEXT | Question text |
| category | VARCHAR(50) | general / behavioural / motivational |
| ideal_answer | TEXT | Used for NLP similarity scoring |
| difficulty | VARCHAR(20) | easy / medium / hard |

21 questions seeded: 7 easy (beginner), 7 medium (intermediate), 7 hard (master)

### sessions
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| user_id | INTEGER FK→users | |
| job_role | VARCHAR(100) | |
| level | VARCHAR(20) | beginner / intermediate / master |
| started_at | DATETIME | |
| completed_at | DATETIME | Nullable |
| overall_score | FLOAT | Nullable, avg of response scores |

### responses
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| session_id | INTEGER FK→sessions | |
| question_id | INTEGER FK→questions | |
| audio_path | VARCHAR(256) | Nullable (null for text mode) |
| transcript | TEXT | Whisper output or typed text |
| speaking_rate | FLOAT | Words per minute |
| filler_count | INTEGER | um, uh, like, etc. |
| pause_count | INTEGER | 0 for text mode |
| relevance_score | FLOAT | 0.0–1.0 (Sentence-BERT) |
| fluency_score | FLOAT | 0.0–1.0 |
| overall_score | FLOAT | 0–100 (relevance×50 + fluency×50) |
| feedback_text | TEXT | Generated feedback |
| created_at | DATETIME | |

---

## API Endpoints

### Authentication (`/api/auth`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /register | No | Register with name/email/password validation |
| POST | /login | No | Login, returns access + refresh tokens |
| POST | /logout | JWT | Revokes token via blocklist |
| POST | /refresh | Refresh | Issue new access token |
| GET | /me | JWT | Current user profile |
| POST | /verify-email | No | Verify email with token |
| POST | /resend-verification | JWT | Resend verification email |
| POST | /forgot-password | No | Request password reset (doesn't reveal if email exists) |
| POST | /reset-password | No | Reset password with token (1-hour expiry) |

### Questions (`/api/questions`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /?level=beginner | JWT | List 5 shuffled questions filtered by difficulty |

### Sessions (`/api/sessions`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /start | JWT | Create session with job_role + level |
| GET | / | JWT | List all user sessions with responses |
| GET | /:id | JWT | Single session with all responses |
| POST | /:id/complete | JWT | Mark complete, calculate average score |

### Analysis (`/api/analysis`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /submit | JWT | Voice: upload audio → Whisper → Librosa → BERT → feedback |
| POST | /submit-text | JWT | Text: typed answer → filler analysis → BERT → feedback |

### User (`/api/user`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /dashboard-stats | JWT | Sessions count, avg score, completed count |
| PUT | /profile | JWT | Update name/email (email change resets verification) |
| POST | /change-password | JWT | Change password with strength validation |
| DELETE | /delete-account | JWT | Delete account + all data cascade |

### AI Chatbot (`/api/chatbot`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /message | JWT | Send message to Ollama AI coach, returns response |
| POST | /session-feedback | JWT | Generate personalised coaching for completed session |

### Misc (`/api`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /contact | No | Contact form submission |
| GET | /health | No | Health check |

---

## AI Pipeline

### Voice Mode
```
Audio (.webm)
  ├──► Whisper (base model) ──► Transcript text
  └──► Librosa ──► duration_seconds, pause_count
                        │
Transcript ──► Word count, speaking_rate (WPM), filler_count, fluency_score
Transcript + ideal_answer ──► Sentence-BERT (all-MiniLM-L6-v2) ──► relevance_score (0–1)
All metrics ──► Feedback Generator ──► feedback_text + overall_score (0–100)
```

### Text Mode
```
Typed answer ──► Word count, filler_count, fluency_score (estimated rate)
Answer + ideal_answer ──► Sentence-BERT ──► relevance_score (0–1)
Metrics ──► Feedback Generator ──► feedback_text + overall_score (0–100)
(No audio analysis — pause_count = 0)
```

### Scoring Formula
- **Fluency score** = max(0, min(1, 1.0 - filler_ratio×2 - rate_penalty×0.5))
  - rate_penalty = abs(speaking_rate - 130) / 130
- **Relevance score** = cosine_similarity(BERT_encode(answer), BERT_encode(ideal_answer))
- **Overall score** = relevance_score × 50 + fluency_score × 50

### Feedback Rules
- Speaking rate < 100 WPM → "pace too slow"
- Speaking rate > 170 WPM → "too fast"
- Filler count > 10 → strong warning
- Filler count > 5 → mild warning
- Relevance < 0.35 → suggest STAR method
- Relevance < 0.6 → "partially relevant"
- Pause count > 15 → suggest more practice

### Filler Words Detected
um, uh, er, ah, like, you know, basically, literally, kind of, sort of

---

## AI Chatbot (Ollama Integration)

### Architecture
- **Model**: qwen3:8b running locally via Ollama
- **Framework**: LangChain (langchain-ollama + langchain-core)
- **Pattern**: Lazy-loaded singleton with ChatPromptTemplate

### Features
- Floating chat widget (bottom-right, visible when logged in)
- Conversation context maintained (last 10 messages sent to LLM)
- Interview-specific system prompt (STAR method, delivery tips, answer structures)
- Quick suggestion chips for first-time users
- Session feedback generation from practice results

### Prompt Design
The system prompt instructs the LLM to:
- Act as an expert interview preparation advisor
- Suggest STAR method for behavioural questions
- Provide tips on delivery, body language, confidence
- Give constructive feedback on user's answers
- Stay focused on interview/career topics
- Keep responses concise (2-4 paragraphs)

---

## Frontend Pages

### Public Pages
| Route | Component | Description |
|-------|-----------|-------------|
| / | HomeComponent | Landing: hero, 3 difficulty level cards, feature grid, how-it-works steps, CTA, footer |
| /auth/signin | SigninComponent | Email + password login |
| /auth/signup | SignupComponent | Name + email + password + confirm password with real-time validation |
| /contact | ContactComponent | Email + message form |

### Protected Pages (require login)
| Route | Component | Description |
|-------|-----------|-------------|
| /dashboard | DashboardComponent | Welcome banner, 3 stat cards (SVG icons), quick actions, recent sessions |
| /practice | PracticeSetupComponent | Job role dropdown + 3 difficulty level cards (Beginner/Intermediate/Master) |
| /practice/:id | PracticeSessionComponent | Live session: question card → voice/text toggle → record or type → AI processing animation → score cards + feedback |
| /practice/:id/results | PracticeResultsComponent | Overall score ring, radar chart, per-question score bars, expandable detail panels |
| /history | HistoryComponent | Score progress line chart + sessions table with score badges |
| /settings | SettingsComponent | Profile edit (name/email) + change password |

### Global Components
| Component | Description |
|-----------|-------------|
| Navbar | Fixed top, dark (#0f172a), IntervYou logo (white+red), nav links, user dropdown |
| ChatbotWidget | Floating purple FAB → chat panel with AI coach (Ollama-powered) |
| AudioRecorder | Mic button, recording timer, stop button, emits Blob |
| ScoreCard | Colour-coded score display (green ≥70, amber ≥40, red <40) |

---

## Authentication System

### Registration Validation
- Name: 2–100 characters
- Email: RFC-compliant regex validation
- Password: min 8 chars, must contain uppercase + lowercase + number
- Confirm password: must match
- Duplicate email check (409 response)

### Token System
- **Access token**: 1-hour expiry, used for all API calls
- **Refresh token**: 30-day expiry, used to get new access tokens
- **Token blocklist**: revoked tokens stored in DB (logout support)
- **JWT interceptor**: auto-attaches Bearer header, handles 401 → logout

### Email Verification Flow
1. Register → verification_token generated (secrets.token_urlsafe)
2. POST /api/auth/verify-email with token → email_verified = true
3. POST /api/auth/resend-verification → new token generated

### Password Reset Flow
1. POST /api/auth/forgot-password with email → reset_token generated (1-hour expiry)
2. POST /api/auth/reset-password with token + new_password → password updated
3. Security: forgot-password always returns 200 (doesn't reveal if email exists)

### Password Change (authenticated)
- Requires current password verification
- New password must meet strength requirements
- POST /api/user/change-password

---

## Design System

| Token | Value | Usage |
|-------|-------|-------|
| Primary | #4f46e5 | Buttons, links, active states |
| Primary Dark | #4338ca | Hover states |
| Accent | #7c3aed | Gradients, secondary highlights |
| Dark | #0f172a | Navbar, footer, hero backgrounds |
| Success | #059669 | Good scores (≥70), positive states |
| Warning | #d97706 | Medium scores (40–69) |
| Error | #dc2626 / #e53e3e | Low scores (<40), errors, "You" in logo |
| Text | #1e293b | Body text |
| Muted | #64748b | Labels, hints, secondary text |
| Border | #e2e8f0 | Card borders, dividers |
| Background | #f8fafc | Page backgrounds |
| Font | Inter 400/500/600/700/800 | All text |
| Border Radius | 8px buttons, 12px cards, 16px panels | |
| Logo | "Interv" white + "You" red (#e53e3e) | Navbar, footer, auth cards |

---

## Key Decisions

1. **Angular 17 standalone** — no NgModules, all components standalone with lazy loading
2. **SQLite** — zero-config local database, sufficient for MVP/dissertation
3. **Whisper base model** — good accuracy/speed tradeoff for CPU (5–20s per audio)
4. **Sentence-BERT all-MiniLM-L6-v2** — lightweight, fast semantic similarity
5. **Ollama local LLM** — no API keys needed, runs entirely offline
6. **Dual input mode** — voice (full pipeline) + text (NLP only) for accessibility
7. **JWT with blocklist** — proper logout support without token expiry waiting
8. **Pinned Angular versions** — prevents npm from upgrading to incompatible v21
9. **No emojis** — professional SVG icons throughout for clean UI
10. **concurrently** — single `npm run dev` starts both servers
