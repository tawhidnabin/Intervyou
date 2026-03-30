# IntervYou — AI Interview Practice Platform

## Setup

### Backend
```bash
cd backend
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

## Project Structure
```
backend/
  app.py              # Flask app factory + seed data
  models.py           # SQLAlchemy models (User, Question, Session, Response)
  routes/
    auth.py           # POST /api/auth/register, /login
    questions.py      # GET /api/questions/
    sessions.py       # POST /start, GET /, GET /:id, POST /:id/complete
    analysis.py       # POST /api/analysis/submit (full AI pipeline)
  services/
    transcription.py  # Whisper STT
    audio_analysis.py # Librosa audio + transcript analysis
    nlp_analysis.py   # Sentence-BERT relevance scoring
    feedback.py       # Rule-based feedback + score computation
  uploads/            # Saved audio files
  test_backend.py     # Smoke test script

intervyou-frontend/
  src/app/
    core/             # AuthService, ApiService, JWT interceptor, Auth guard
    pages/            # login, register, dashboard, interview, feedback, history
    shared/           # AudioRecorderComponent, ScoreCardComponent
```

## API Endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/register | None | Register, returns JWT |
| POST | /api/auth/login | None | Login, returns JWT |
| GET | /api/questions/ | JWT | List all questions |
| POST | /api/sessions/start | JWT | Create session |
| GET | /api/sessions/ | JWT | List user sessions |
| GET | /api/sessions/:id | JWT | Single session detail |
| POST | /api/sessions/:id/complete | JWT | Mark complete |
| POST | /api/analysis/submit | JWT | Upload audio, run AI pipeline |
