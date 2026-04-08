# IntervYou

AI-powered interview practice platform with real-time feedback. Practice with curated questions, get scored on fluency, relevance and confidence, track your progress, and chat with an AI interview coach.

**Live:** https://intervyou.uk
**API:** https://api.intervyou.uk

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Angular 17, Angular Material, Chart.js |
| Backend | Python Flask, Gunicorn |
| Database | SQLite |
| Speech-to-Text | OpenAI Whisper (base) |
| NLP | Sentence-BERT (all-MiniLM-L6-v2) |
| Audio Analysis | Librosa |
| ML Model | scikit-learn Random Forest (confidence prediction) |
| AI Coach | Ollama (qwen3:1.7b) |
| Hosting | Vercel (frontend), AWS EC2 m7i-flex.large (backend) |
| SSL | Let's Encrypt via Certbot |

## Local Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
python app.py
```
Runs on http://localhost:5000

### Frontend
```bash
cd intervyou-frontend
npm install
npx ng serve
```
Runs on http://localhost:4200

### Ollama (AI Coach)
```bash
ollama pull qwen3:1.7b
ollama serve
```

## Project Structure

```
backend/
  app.py                        # Flask app factory, CORS, JWT config, blueprint registration
  models.py                     # SQLAlchemy models (User, Session, Response, Question, TokenBlocklist)
  seed_questions.py             # 58 interview questions across 4 categories × 3 difficulty levels
  train_confidence_model.py     # Trains Random Forest confidence classifier on synthetic data
  requirements.txt              # Python dependencies
  routes/
    auth.py                     # Register, login, logout, token refresh, email verify, password reset
    questions.py                # Get filtered questions by level/category
    sessions.py                 # Session lifecycle (start, list, get, complete)
    analysis.py                 # Audio/text analysis pipeline (Whisper + Librosa + BERT + ML)
    chatbot.py                  # AI coach chat and session feedback via Ollama
    user.py                     # Dashboard stats, profile update, password change, account deletion
    misc.py                     # Health check, contact form
  services/
    transcription.py            # Whisper speech-to-text with ffmpeg setup
    audio_analysis.py           # Librosa audio feature extraction + transcript analysis
    nlp_analysis.py             # Sentence-BERT cosine similarity for relevance scoring
    feedback.py                 # Rule-based feedback generation + overall score computation
    confidence_model.py         # ML confidence prediction (24 audio+text features → low/medium/high)
    chatbot.py                  # Ollama LLM wrapper with 3 prompt templates (chat, session, analysis)
  ml_models/
    confidence_model.pkl        # Trained Random Forest model
    confidence_scaler.pkl       # Feature scaler
  uploads/                      # Stored audio recordings
  instance/
    intervyou.db                # SQLite database (auto-created)

intervyou-frontend/
  src/
    environments/
      environment.ts            # Dev config (localhost:5000)
      environment.prod.ts       # Production config (api.intervyou.uk)
    app/
      app.component.ts          # Root component with navbar and chatbot widget
      app.routes.ts             # Route definitions with lazy loading and auth guards
      app.config.ts             # Providers (router, HTTP client, JWT interceptor, animations)
      core/
        api.service.ts          # HTTP client for all backend API calls
        auth.service.ts         # Auth state management (login, register, logout, token storage)
        auth.guard.ts           # Route guard redirecting unauthenticated users
        jwt.interceptor.ts      # Attaches JWT Bearer token to requests, auto-logout on 401
      pages/
        home/                   # Landing page (hero, features, levels, how-it-works)
        auth/signin/            # Login page
        auth/signup/            # Registration page with password strength validation
        dashboard/              # User dashboard (stats, recent sessions, quick actions)
        practice/
          practice-setup/       # Session config (role, level, category, question count)
          practice-session/     # Live interview (voice/text input, scoring, AI feedback)
          practice-results/     # Results page with radar chart and per-question breakdown
        history/                # Session history with score trend line chart
        settings/               # Profile editing and password change
        contact/                # Contact form
      shared/components/
        audio-recorder/         # Microphone recording widget (MediaRecorder API)
        chatbot/                # Floating AI coach chat widget
        score-card/             # Reusable colour-coded score display card

deploy/
  aws-setup.sh                  # Automated EC2 setup (Python, ffmpeg, Nginx, Ollama, venv, systemd)
  intervyou-aws.service         # Systemd service for Gunicorn (2 workers, 120s timeout)
  nginx-aws.conf                # Nginx reverse proxy config (SSL, /api/ proxy to :5000)
  DEPLOYMENT.md                 # Step-by-step deployment guide
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/register | No | Create account |
| POST | /api/auth/login | No | Authenticate user |
| POST | /api/auth/logout | JWT | Revoke token |
| POST | /api/auth/refresh | JWT | Refresh access token |
| GET | /api/auth/me | JWT | Get current user |
| POST | /api/auth/verify-email | No | Verify email token |
| POST | /api/auth/forgot-password | No | Request password reset |
| POST | /api/auth/reset-password | No | Reset password |
| GET | /api/questions/ | JWT | Get filtered questions |
| GET | /api/questions/categories | JWT | Get category breakdown |
| POST | /api/sessions/start | JWT | Create new session |
| GET | /api/sessions/ | JWT | List user sessions |
| GET | /api/sessions/:id | JWT | Get session details |
| POST | /api/sessions/:id/complete | JWT | Complete and score session |
| POST | /api/analysis/submit | JWT | Submit audio for full AI pipeline |
| POST | /api/analysis/submit-text | JWT | Submit text for NLP analysis |
| POST | /api/analysis/ai-feedback/:id | JWT | Generate LLM deep feedback |
| POST | /api/chatbot/message | JWT | Send chat message to AI coach |
| POST | /api/chatbot/session-feedback | JWT | Generate session coaching summary |
| GET | /api/user/dashboard-stats | JWT | Get user statistics |
| PUT | /api/user/profile | JWT | Update profile |
| POST | /api/user/change-password | JWT | Change password |
| DELETE | /api/user/delete-account | JWT | Delete account and all data |
| POST | /api/contact | No | Submit contact form |
| GET | /api/health | No | Health check |

## AI/ML Pipeline

```
Audio (.webm) → Whisper (transcription) → Librosa (audio features) + Text Analysis (fluency)
                                        → Sentence-BERT (relevance scoring vs ideal answer)
                                        → Random Forest (confidence: low/medium/high)
                                        → Rule-based feedback generation
                                        → Ollama LLM (deep analytical coaching, on-demand)
```

**Scoring:**
- Relevance (0–1): Cosine similarity between Sentence-BERT embeddings of answer vs ideal answer
- Fluency (0–1): Based on filler word ratio and speaking rate deviation from 130 WPM
- Overall (0–100): relevance × 50 + fluency × 50
- Confidence: 24-feature Random Forest classifier (pitch, energy, pauses, fillers, hedging words, etc.)

## Deployment

### Architecture
```
Vercel (intervyou.uk) ←→ HTTPS ←→ AWS EC2 (api.intervyou.uk)
                                    ├── Nginx (SSL via Let's Encrypt)
                                    ├── Gunicorn + Flask
                                    ├── SQLite
                                    └── Ollama (qwen3:1.7b)
```

### Deploy to EC2
```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
curl -fsSL https://raw.githubusercontent.com/tawhidnabin/Intervyou/main/deploy/aws-setup.sh | bash
```

### DNS Records (Fasthosts)
| Type | Name | Value |
|------|------|-------|
| A | @ | 216.198.79.1 (Vercel) |
| A | api | 13.51.162.43 (EC2) |
| CNAME | www | 23f8714f007756fb.vercel-dns-017.com |

### SSL Setup
```bash
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx -d api.intervyou.uk --non-interactive --agree-tos -m your@email.com
```

### Useful EC2 Commands
```bash
sudo systemctl status intervyou          # Check backend status
sudo journalctl -u intervyou -f          # View logs
sudo systemctl restart intervyou         # Restart backend
curl https://api.intervyou.uk/api/health # Health check
cd /home/ubuntu/Intervyou && git pull origin main && sudo systemctl restart intervyou  # Update code
```

## Bug Fixes Applied

1. **502 Bad Gateway** — Gunicorn log files not created with correct permissions. Fixed by adding `touch` and `chown` in setup script.
2. **Interactive apt prompts** — Ubuntu kernel upgrade dialog blocked automated setup. Fixed with `DEBIAN_FRONTEND=noninteractive`.
3. **Mixed content (HTTPS/HTTP)** — Frontend on HTTPS calling backend on HTTP. Fixed by setting up SSL via Let's Encrypt on EC2.
4. **CORS** — Updated to allow multiple production domains (intervyou.uk, www, Vercel preview URLs).
5. **Slow LLM** — qwen3:8b too slow on CPU. Switched to qwen3:1.7b for faster inference.
6. **Duplicate route file** — Removed uppercase `Chatbot.py` conflicting with `chatbot.py` on Linux.
7. **JWT interceptor** — Fixed dead logic that always attached token regardless of condition.
8. **DNS resolution** — Fasthosts DNS returning wrong IP for api subdomain. Resolved by flushing caches and verifying A records.

## Security

- Password hashing: PBKDF2-SHA256 (Werkzeug)
- Password policy: 8+ chars, uppercase, lowercase, number
- JWT: Access tokens expire 1 hour, refresh tokens 30 days
- Token revocation via blocklist table
- CORS whitelist-based origin policy
- HTTPS everywhere (Let's Encrypt)
- 50MB upload limit
- SQLAlchemy ORM (parameterised queries)
