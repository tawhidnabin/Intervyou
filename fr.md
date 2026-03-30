InterviewAI.io
Deep Research · Angular + Flask Full-Stack MVP Blueprint
Complete Frontend Structure · Feature Inventory · API Design · Angular Components · Flask Routes
Generated March 2026 · AI-Agent Ready
1. Technology Stack
Layer Technology Purpose
Frontend Framework Angular 17+ SPA with routing, modules, lazy loading
UI Library Angular Material + Tailwind CSS Components, theming, utility classes
State Management NgRx or BehaviorSubject services Auth state, session data, user profile
HTTP Client Angular HttpClient REST calls to Flask API
Real-time WebSockets (socket.io-client or native WS) Interview Copilot live streaming
Audio / Speech Browser Web Speech API / MediaRecorder API Voice input for Copilot & practice
Auth Tokens JWT stored in HttpOnly cookie or localStorageAuth guard on protected routes
Backend Python Flask 3.x REST API, AI orchestration, auth
AI Provider OpenAI GPT-4o or Anthropic Claude API Question gen, scoring, resume AI
Database PostgreSQL + SQLAlchemy ORM Users, sessions, questions, resumes
File Storage AWS S3 or local uploads Resume PDFs, cover letters
Auth Backend Flask-JWT-Extended or Flask-Login Token issuance & refresh
Email SendGrid / SMTP via Flask-Mail Verify account, notifications
Deployment Angular on Vercel/Nginx · Flask on Render/Railway Seprate frontend + backend deploys
2. Complete Site Map & Angular Routes
Angular Route Page / Component Auth? User Type
/ HomeComponent (landing) No Public
/async AsyncHiringComponent No Public
/education EducationComponent No Public
/contact ContactComponent No Public
/about AboutComponent No Public
/faq FaqComponent No Public
/terms TermsComponent No Public
/privacy PrivacyComponent No Public
/auth/signin SignInComponent No Public
/auth/signup SignUpComponent No Public
/auth/forgot-password ForgotPasswordComponent No Public
/dashboard DashboardComponent YES Candidate
/practice InterviewPracticeComponent YES Candidate
/practice/:sessionId InterviewSessionComponent YES Candidate
/practice/:sessionId/results SessionResultsComponent YES Candidate
/resume ResumeBuilderComponent YES Candidate
/resume/:id ResumeEditorComponent YES Candidate
/cover-letter CoverLetterComponent YES Candidate
/thank-you ThankYouNoteComponent YES Candidate
/copilot CopilotComponent YES Candidate
/pre-screen PreScreenDashboard YES Employer
/pre-screen/create CreateJobComponent YES Employer
/pre-screen/:jobId JobDetailComponent YES Employer
/pre-screen/:jobId/candidate/:cid CandidateReviewComponent YES Employer
/settings AccountSettingsComponent YES All
Angular Module Structure
Module Contains Lazy Loaded?
AppModule Root module, AppRoutingModule, SharedModule No
AuthModule SignIn, SignUp, ForgotPassword components Yes
DashboardModule Dashboard, Settings components Yes
PracticeModule Interview Practice, Session, Results components Yes
ResumeModule Resume Builder, Editor, Preview components Yes
GeneratorModule Cover Letter, Thank You Note components Yes
CopilotModule Live Copilot, Transcript, Overlay components Yes
PreScreenModule Employer portal — Job mgmt, Candidate review Yes
PublicModule Home, Async, Education, Contact, FAQ pages Yes
SharedModule Navbar, Footer, Button, Modal, Card, LoadingSpinner No
CoreModule AuthService, ApiService, JwtInterceptor, AuthGuard No
3. Public Pages — Deep Feature Analysis
3.1 Home Page (/)
Section Content & Behaviour
Navbar Fixed top · Logo SVG left · Nav links (hidden mobile) · 'Sign In' ghost btn + 'Sign Up' filled btn · HamburgHero H1: 'Supercharge Your Interviews With AI' · Subheading targets job seekers, companies, institutions · FeFeature Tabs Tabs: Interview Practice | AI Resumes | Cover Letters | Thank You Notes | Interview Copilot | AI Pre-ScrFeature Cards Grid 3-column grid · Card 1: 'Streamline interviews with AI questions & candidate tracking' · Card 2: 'Boost intMid CTA "It's that easy! What are you waiting for? Sign Up Now!" banner · Full-width indigo bg · Button → /auth/siCompany Logos Strip Heading: 'Get Ready for Jobs at Leading Firms' · Logos: Meta, Google, Amazon, Netflix, Apple, Infosys, Feature List H2: 'Join a growing community!' · 6 features in 2-col definition grid: Real-time AI Questions, Question LibCompanies & Colleges H2: 'Revolutionize Your Interviewing Process' · 6 benefit cards: Efficient Hiring, Customized Questions, SJob Seekers H2: 'Unlock Your Interview Potential' · 6 benefit cards: Personalized Practice, Insights for Improvement, AFinal CTA Banner H2: 'Ready to dive in?' · Subhead: 'Get started and transform your interviews today!' · Body copy · 'Try ItFooter Links: About · FAQ · Terms · Privacy · Blog · Feedback · Copyright · Twitter/X icon
3.2 Async Hiring Page (/async)
Section Content & Behaviour
Hero H1: 'Accelerate Your Hiring with InterviewAI Async' · Subhead: 'Automated candidate screenings with acPricing Plans 3 cards side by side · Essential $19/mo: 1 job, unlimited candidates · Growth $39/mo: 5 jobs · Pro $99/mWhy Choose Section 4 stat-backed points: Cut time-to-hire 50%, Identify talent without bias, Reduce initial interviews 70%, LeKey Features 6 feature description list: AI Question Generation, Customizable Questions, Async Candidate InterviewsValue Statement Paragraph: 'helps companies make smarter hiring decisions faster… reducing time to hire by up to 50%'
Bottom CTA "Ready to Hire Smarter, Not Harder?" · Sign up CTA + Contact Us link
3.3 Education Page (/education)
Section Content & Behaviour
Hero H1: 'Career Counselors Equip Students for Interviews' · Description of modern AI tools for student intervPartner Section H2: 'Partner with us today!' · Subhead: 'Supercharge Your Graduating Student Interview Prep' · TestimoFeature List 6 features: Improved Interview Outcomes, Competitive Edge, Real-time AI Questions, AI Follow-Up QueCTA "Ready to elevate your graduating students? Get in touch to partner with us today!" · Contact Us button →Images highered3.svg (hero top) · highered1.svg (bottom decoration)
3.4 Contact Page (/contact)
Element Detail
Heading "Contact Us"
Subtext "Please use the form below to contact our team. We'll get back to you as soon as possible!"
Form Fields Email (input type=email, required) · Message (textarea, required)
Submit Button "Send" — primary button · POST to Flask /api/contact
Success State Show confirmation message after successful send
Error State Inline error if email invalid or server error
4. Authentication Pages
Page / Route Fields & Behaviour
Sign Up (/auth/signup) Name (text) · Email (email) · Password (password, min 8 chars) · Confirm Password · 'Create Account' bSign In (/auth/signin) Email · Password · 'Sign In' btn · Google OAuth btn · 'Forgot Password?' link → /auth/forgot-password · Forgot Password (/auth/forgot-password)Email field · 'Send Reset Link' btn · POST /api/auth/forgot-password · Success: 'Check your email' messReset Password (/auth/reset-password?token=) New Password · Confirm Password · 'Reset Password' btn · POST /api/auth/reset-password with token
Auth Guard Angular CanActivate guard on all /dashboard, /practice, /resume, /cover-letter, /thank-you, /copilot, /pre-sJWT Interceptor Angular HttpInterceptor adds 'Authorization: Bearer <token>' header to every API call · Handles 401 → a5. Dashboard (/dashboard)
Widget / Section Content & Data
Welcome Banner Greeting: 'Welcome back, [Name]!' · Quick stats row
Stats Row 4 stat cards: Interviews Practiced · Average Score · Resumes Created · Streak Days
Quick Actions 6 shortcut cards with icon + label: Start Practice · Build Resume · Cover Letter · Thank You Note · LauncRecent Activity List of last 5 practice sessions: job title, date, score, 'View Results' link
Progress Chart Line chart: Practice scores over time (last 30 days)
Sidebar / Top Nav User avatar, name, subscription plan badge, Settings link, Logout
6. Interview Practice (/practice)
Step / View Content & Behaviour
Setup Form (/practice) Job Title (text input) · Job Category (dropdown: Tech, Finance, Marketing, HR, etc.) · Seniority Level (drSession Screen (/practice/:sessionId) Top: Job title + question counter (Q3 of 10) + timer · Main: AI question displayed prominently · Answer aAI Follow-Up After submitting answer: AI generates 1–2 follow-up questions · User answers follow-ups before moving In-Session Feedback After each answer: Score badge (1–10) · Feedback text · Model answer (expandable) · 'Next Question' bResults Screen (/practice/:sessionId/results) Overall score with visual ring chart · Table: Question | Answer | Score | Feedback for each Q · StrengthsHistory List (/practice — tab) All past sessions table: Date, Job Title, Score, # Questions, 'View Results' link
7. AI Resume Builder (/resume)
View / Panel Content & Behaviour
Resume List (/resume) Grid of saved resumes with preview thumbnail · '+ New Resume' btn · Each card: title, last updated, 'EdiEditor (/resume/:id) Split layout: left panel (form) + right panel (live preview)
Left Form Sections Personal Info (name, email, phone, location, LinkedIn, portfolio) · Summary (textarea + AI Generate btn)AI Generate Summary 'Generate Summary' btn → POST /api/ai/resume/summary → streams text into textarea
AI Enhance Bullets 'Enhance' btn on each work block → POST /api/ai/resume/enhance → rewrites bullet points with action vTailor to Job Paste job description textarea + 'Tailor Resume' btn → AI highlights missing keywords, rewrites summarRight Preview Live PDF-style preview updates as user types · Template selector (3–5 templates) · Colour scheme pickExport 'Download PDF' btn → Flask generates PDF server-side → file download · 'Download DOCX' optional
ATS Score Side panel shows ATS compatibility score % + list of missing keywords from job description
8. Cover Letter Generator (/cover-letter)
Section Content & Behaviour
Inputs (left pane) Job Title (text) · Company Name (text) · Job Description (large textarea, paste JD here) · Your Name · TGenerate Button 'Generate Cover Letter' btn → POST /api/ai/cover-letter → streams AI response into output pane
Output Pane (right) Rich text editor (contenteditable or Quill) with generated letter · User can freely edit · Word count indicatoActions 'Regenerate' (new variation) · 'Copy to Clipboard' · 'Download as DOCX' · 'Save to Account'
History Tab List of previously generated/saved cover letters with date and job title
9. Thank You Note Generator (/thank-you)
Section Content & Behaviour
Inputs Interviewer Name · Their Role/Title · Company Name · Interview Date · Key Topics Discussed (bullet listGenerate Button 'Generate Thank You Note' → POST /api/ai/thank-you → AI outputs email
Output Editable text area with generated email · Subject line suggestion included
Actions 'Copy Email' btn · 'Regenerate' btn · 'Save' btn
Use Case Post-interview professional courtesy email to interviewer within 24h
10. Interview Copilot (/copilot) [Real-Time AI Assistance]
The Copilot feature provides real-time AI guidance DURING a live interview. It listens via microphone, detects questions
asked by the interviewer, and instantly suggests structured answers on screen — invisibly to the interviewer.
Component / Step Content & Behaviour
Setup Screen Job Title & Description inputs · 'Upload your resume' (pre-fill context) · Mic permission prompt · 'Start CoPrivacy Disclosure Prominent banner: 'Audio is processed locally / on our servers. Not recorded.' · User must acknowledge Live Session UI Top bar: Job title + elapsed timer + 'End Session' btn · Left panel: Live transcript (rolling, auto-scroll, reaQuestion Detection Browser Web Speech API captures audio → transcript sent via WebSocket to Flask backend → AI detecSuggestion Display Formatted answer with STAR structure or bullet points (user-configurable) · 'Regenerate' small btn · 'NexWebSocket Flow Angular WS client → Flask-SocketIO server → OpenAI/Claude streaming → streamed tokens back to AnEnd Session 'End Session' btn → show session summary: number of questions detected, list of Q+A pairs · 'Downloa
Keyboard Shortcut Optional: Cmd/Ctrl+Space to manually trigger suggestion from current transcript line
11. AI Pre-Screen Portal (/pre-screen) [Employer Feature]
View Content & Behaviour
Employer Dashboard List of created job postings · Stats: Total candidates, Avg score, Completion rate · '+ Create New Job' btCreate Job (/pre-screen/create) Job Title · Job Description (textarea) · 'AI Generate Questions' btn · Question list (editable, add/remove) Candidate Link Flow Employer shares URL to candidates · Candidate opens link (no account needed) · Sees job title + intro ·Candidate Recording UI Question displayed fullscreen · Countdown timer · 'Record Answer' btn (uses MediaRecorder API) · PlayEmployer Review (/pre-screen/:jobId) Table of candidates: Name, Email, Submitted date, AI Score, Status · Click row to view full review
Candidate Review Detail Candidate info · Per-question panel: video playback + auto-transcript + AI score (1–10) + AI feedback + AI Scoring Logic POST /api/ai/pre-screen/score with transcript → returns score + feedback per question + overall summaPricing Tiers Essential $19/mo: 1 job · Growth $39/mo: 5 jobs · Pro $99/mo: 15 jobs + CSM + early access
12. Flask Backend API — Complete Endpoint Reference
12.1 Auth Endpoints
Method Endpoint Body / Params Response
POST /api/auth/register name, email, password 201: {user, token}
POST /api/auth/login email, password 200: {user, access_token, refresh_token}
POST /api/auth/logout — (JWT header) 200: {message}
POST /api/auth/refresh refresh_token 200: {access_token}
POST /api/auth/forgot-password email 200: {message}
POST /api/auth/reset-password token, new_password 200: {message}
GET /api/auth/me — (JWT header) 200: {user profile}
12.2 Interview Practice Endpoints
Method Endpoint Body / Params Response
POST /api/practice/session/start job_title, category, seniority, company, num_questions 201: {session_id, first_question}
POST /api/practice/session/:id/answer question_id, answer_text 200: {score, feedback, follow_up_questiPOST /api/practice/session/:id/next — 200: {question} or {session_complete: trGET /api/practice/session/:id/results — 200: {overall_score, questions[], answerGET /api/practice/sessions — (JWT) 200: [{session list}]
POST /api/practice/questions/generate job_title, category, seniority, num 200: {questions[]}
12.3 Resume Builder Endpoints
Method Endpoint Body / Params Response
GET /api/resume — (JWT) 200: [{resume list}]
POST /api/resume resume data (JSON) 201: {resume_id, resume}
GET /api/resume/:id — 200: {resume}
PUT /api/resume/:id updated fields 200: {resume}
DELETE /api/resume/:id — 204
POST /api/ai/resume/summary work_history, job_title, skills 200: {summary} (streamed)
POST /api/ai/resume/enhance bullet_points, job_title 200: {enhanced_bullets} (streamed)
POST /api/ai/resume/tailor resume_data, job_description 200: {tailored_resume, ats_score, missing_keyGET /api/resume/:id/pdf — 200: application/pdf file download
12.4 Cover Letter Endpoints
Method Endpoint Body / Params Response
POST /api/ai/cover-letter job_title, company, job_description, resume_data, tone200: {cover_letter} (streamed)
GET /api/cover-letter — (JWT) 200: [{saved cover letters}]
POST /api/cover-letter/save title, content, job_title 201: {id}
DELETE /api/cover-letter/:id — 204
12.5 Thank You Note Endpoints
Method Endpoint Body / Params Response
POST /api/ai/thank-you interviewer_name, role, company, topics[], tone 200: {subject, body} (streamed)
POST /api/thank-you/save content, interviewer, company 201: {id}
12.6 Copilot (WebSocket) Endpoints
Type Event / Endpoint Payload Description
HTTP POST /api/copilot/session/start job_title, job_description, resume_id Init session, return session_id
WS EMIT transcript_chunk {session_id, text, timestamp} Client sends live transcript chunk
WS ON ai_suggestion {suggestion, format, confidence} Server pushes AI answer suggestion
WS ON question_detected {question_text} Server signals question was detected in transHTTP POST /api/copilot/session/:id/end — Finalise session, return summary
HTTP GET /api/copilot/session/:id/transcript — Return full session transcript PDF
12.7 Pre-Screen (Employer) Endpoints
Method Endpoint Body / Params Response
GET /api/pre-screen/jobs — (JWT, employer) 200: [{job list}]
POST /api/pre-screen/jobs title, description, questions[], time_limit 201: {job_id, candidate_link}
GET /api/pre-screen/jobs/:id — 200: {job + candidate submissions}
DELETE /api/pre-screen/jobs/:id — 204
POST /api/ai/pre-screen/questions job_title, job_description 200: {questions[]}
POST /api/pre-screen/submit job_id, candidate_name, email, answers[] 201: {submission_id} (public route)
POST /api/ai/pre-screen/score submission_id, transcripts[] 200: {per_question_scores, overall}
PUT /api/pre-screen/submission/:id/status status: good_fit|not_fit|review 200: {updated submission}
12.8 Misc Endpoints
Method Endpoint Body / Params Response
POST /api/contact email, message 200: {message: 'Sent'}
GET /api/user/dashboard-stats — (JWT) 200: {sessions_count, avg_score, resumes_PUT /api/user/profile name, email, preferences 200: {user}
POST /api/user/change-password old_password, new_password 200: {message}
POST /api/billing/subscribe plan_id, payment_token 201: {subscription}
GET /api/billing/plans — 200: [{plan list with pricing}]
13. Angular Component Specifications
Component Inputs / Outputs Key Methods
NavbarComponent @Input: isLoggedIn, userName / @Output: logout toggleMobileMenu(), scrollToTop()
FooterComponent — —
HeroSectionComponent @Input: tabs[], activeTab / @Output: tabChange, ctaClick setActiveTab(tab)
FeatureTabBarComponent @Input: tabs[], selected / @Output: tabSelect onTabClick(tab)
CompanyLogoStripComponent @Input: logos[] startMarquee() in ngAfterViewInit
InterviewSetupComponent @Output: sessionStart(config) validateForm(), startSession()
InterviewSessionComponent @Input: sessionId / @Output: sessionEnd submitAnswer(), nextQuestion(), recordVoice()
ScoreCardComponent @Input: question, answer, score, feedback toggleModelAnswer()
SessionResultsComponent @Input: sessionId loadResults(), downloadReport()
ResumeSplitPaneComponent @Input: resumeId / @Output: saved generateSummary(), enhanceBullets(), downloadPdf()
CoverLetterComponent @Output: saved generateLetter(), copyToClipboard(), saveLetter()
CopilotSessionComponent @Output: sessionEnd startRecording(), stopRecording(), connectWebSocket(), oPreScreenDashboardComponent — loadJobs(), createJob()
CandidateReviewComponent @Input: submissionId loadSubmission(), updateStatus(), addNote()
AuthFormComponent @Input: mode: 'signin'|'signup' / @Output: authSuccessonSubmit(), googleLogin()
DashboardStatsComponent @Input: stats renderChart()
LoadingSpinnerComponent @Input: size, message —
AlertComponent @Input: type, message / @Output: closed close()
ModalComponent @Input: title, isOpen / @Output: closed, confirmed open(), close()
14. Angular Services
Service Responsibility Key Methods
AuthService Login, register, logout, JWT storage, currentUser$ login(), register(), logout(), getToken(), isLoggedIn()
ApiService Base HttpClient wrapper with auth interceptor get(), post(), put(), delete(), stream()
PracticeService Interview session lifecycle startSession(), submitAnswer(), getResults(), getSessions()
ResumeService CRUD for resumes + AI calls getResumes(), createResume(), updateResume(), generateSummaCoverLetterService Generate + save cover letters generate(), save(), getAll(), delete()
CopilotService WebSocket connection, mic input, AI suggestions connect(), sendTranscript(), onSuggestion$, endSession()
PreScreenService Employer job + submission management getJobs(), createJob(), getSubmissions(), scoreSubmission()
NotificationService Toast / alert messages success(), error(), info(), warn()
StorageService LocalStorage/SessionStorage abstraction setItem(), getItem(), removeItem(), clear()
SpeechService Browser Web Speech API wrapper startListening(), stopListening(), transcript$
15. Flask Project Structure
backend/
■■■ app/
■ ■■■ __init__.py # App factory, register blueprints, init extensions
■ ■■■ config.py # Config classes (Dev, Prod, Test)
■ ■■■ extensions.py # db, jwt, mail, socketio, cors
■ ■■■ models/
■ ■ ■■■ user.py # User model (id, name, email, password_hash, plan)
■ ■ ■■■ interview.py # Session, Question, Answer, Score models
■ ■ ■■■ resume.py # Resume model (JSON blob + metadata)
■ ■ ■■■ document.py # CoverLetter, ThankYouNote models
■ ■ ■■■ pre_screen.py # Job, Submission, QuestionResponse models
■ ■ ■■■ billing.py # Subscription, Plan models
■ ■■■ routes/
■ ■ ■■■ auth.py # Blueprint: /api/auth/*
■ ■ ■■■ practice.py # Blueprint: /api/practice/*
■ ■ ■■■ resume.py # Blueprint: /api/resume/*
■ ■ ■■■ cover_letter.py # Blueprint: /api/ai/cover-letter, /api/cover-letter/*
■ ■ ■■■ thank_you.py # Blueprint: /api/ai/thank-you, /api/thank-you/*
■ ■ ■■■ copilot.py # Blueprint: /api/copilot/* + SocketIO events
■ ■ ■■■ pre_screen.py # Blueprint: /api/pre-screen/*
■ ■ ■■■ user.py # Blueprint: /api/user/*
■ ■ ■■■ billing.py # Blueprint: /api/billing/*
■ ■ ■■■ misc.py # Blueprint: /api/contact, /api/health
■ ■■■ services/
■ ■ ■■■ ai_service.py # OpenAI / Anthropic API calls, streaming
■ ■ ■■■ auth_service.py # Password hashing, token generation
■ ■ ■■■ pdf_service.py # Resume PDF generation (WeasyPrint / ReportLab)
■ ■ ■■■ email_service.py # Transactional emails via SendGrid
■ ■ ■■■ scoring_service.py # AI scoring logic, prompt engineering
■ ■■■ utils/
■ ■■■ decorators.py # @jwt_required wrapper, @employer_required
■ ■■■ validators.py # Request schema validators
■■■ migrations/ # Alembic / Flask-Migrate migrations
■■■ tests/ # Pytest test suite
■■■ requirements.txt
■■■ .env # SECRET_KEY, DATABASE_URL, OPENAI_API_KEY, etc.
■■■ run.py # Entry point: app.run()
16. Angular Project Structure
frontend/
■■■ src/
■ ■■■ app/
■ ■ ■■■ core/ # Singleton services + guards
■ ■ ■ ■■■ services/ # AuthService, ApiService, StorageService
■ ■ ■ ■■■ guards/ # AuthGuard, RoleGuard
■ ■ ■ ■■■ interceptors/ # JwtInterceptor, ErrorInterceptor
■ ■ ■ ■■■ models/ # TypeScript interfaces (User, Session, Resume...)
■ ■ ■■■ shared/ # Reusable UI components
■ ■ ■ ■■■ navbar/
■ ■ ■ ■■■ footer/
■ ■ ■ ■■■ loading-spinner/
■ ■ ■ ■■■ alert/
■ ■ ■ ■■■ modal/
■ ■ ■■■ features/ # Feature modules (all lazy loaded)
■ ■ ■ ■■■ public/ # Home, Async, Education, Contact, FAQ
■ ■ ■ ■■■ auth/ # SignIn, SignUp, ForgotPassword
■ ■ ■ ■■■ dashboard/ # Dashboard, Settings
■ ■ ■ ■■■ practice/ # Setup, Session, Results, History
■ ■ ■ ■■■ resume/ # List, Editor, Preview
■ ■ ■ ■■■ generators/ # CoverLetter, ThankYouNote
■ ■ ■ ■■■ copilot/ # Setup, LiveSession, Transcript
■ ■ ■ ■■■ pre-screen/ # EmployerDashboard, JobCreate, Review
■ ■ ■■■ app-routing.module.ts
■ ■ ■■■ app.module.ts
■ ■■■ assets/
■ ■ ■■■ images/
■ ■ ■■■ icons/
■ ■■■ environments/
■ ■ ■■■ environment.ts # { apiUrl: 'http://localhost:5000', wsUrl: '...' }
■ ■ ■■■ environment.prod.ts
■ ■■■ styles.scss # Global Tailwind imports + theme vars
■■■ angular.json
■■■ tailwind.config.js
■■■ package.json
17. Design System
Token Value Usage
--color-primary #4f46e5 Buttons, links, active states
--color-primary-dark #4338ca Hover on primary buttons
--color-accent #7c3aed Copilot UI, secondary highlights
--color-dark #0f172a Navbar, footer, hero banners
--color-light #eef2ff Section backgrounds, card fills
--color-border #c7d2fe Input borders, dividers
--color-success #059669 Scores, positive feedback
--color-warning #d97706 Score warnings, 'medium' states
--color-text #1e293b Body text
--color-muted #64748b Subtext, labels, hints
Font: Heading Inter 700 / Helvetica Bold H1–H3
Font: Body Inter 400 / System sans-serif Paragraphs, labels
Border Radius 8px cards, 6px buttons, 12px modals All UI elements
Max Content Width 1200px, centred All pages
Spacing Base 4px (Tailwind default) All padding/margin
Breakpoints sm:640px md:768px lg:1024px xl:1280px Tailwind defaults
Shadow 0 2px 12px rgba(0,0,0,0.08) Cards, dropdowns, modals
Transition 200ms ease-in-out Hover, focus states
18. Ready-to-Use AI Agent Prompt
Paste the following block directly into any AI agent or coding assistant:
Build a full-stack web application that replicates InterviewAI.io using Angular 17 for the frontend
and Flask (Python) for the backend REST API.
FRONTEND (Angular 17 + Tailwind CSS + Angular Material):
- Use lazy-loaded feature modules: PublicModule, AuthModule, DashboardModule, PracticeModule,
ResumeModule, GeneratorModule, CopilotModule, PreScreenModule
- Primary colour: #4f46e5 (indigo). Dark theme for navbar/footer: #0f172a
- SharedModule: NavbarComponent (fixed top, logo left, Sign In + Sign Up btns right),
FooterComponent
- CoreModule: AuthService (JWT in localStorage), ApiService (HttpClient wrapper), JwtInterceptor
(adds Authorization header), AuthGuard (CanActivate)
- Routes: / (home landing with hero + feature tabs + company logos + feature list + CTA), /async
(pricing cards + employer features), /education (career counselor landing), /contact (email+message
form), /auth/signin, /auth/signup, /dashboard, /practice, /practice/:id (live session),
/practice/:id/results, /resume, /resume/:id (split-pane editor), /cover-letter, /thank-you,
/copilot (WebSocket-based live session), /pre-screen (employer portal)
BACKEND (Flask 3 + PostgreSQL + SQLAlchemy + Flask-JWT-Extended + Flask-SocketIO):
- Blueprints: auth, practice, resume, cover_letter, thank_you, copilot, pre_screen, user, billing,
misc
- AI calls via OpenAI GPT-4o or Anthropic Claude (streaming where applicable)
- Key endpoints: POST /api/auth/register|login, POST /api/practice/session/start, POST
/api/practice/session/:id/answer, POST /api/ai/resume/summary|enhance|tailor, POST
/api/ai/cover-letter, POST /api/ai/thank-you, WebSocket events for copilot transcript/suggestion,
POST /api/pre-screen/jobs, POST /api/pre-screen/submit (public), POST /api/ai/pre-screen/score
- Use Flask-SocketIO for the real-time Copilot feature (emit transcript_chunk → receive
ai_suggestion)
- PDF generation for resume downloads using WeasyPrint or ReportLab
- Use environment variables for all secrets (SECRET_KEY, DATABASE_URL, OPENAI_API_KEY)
Start by scaffolding the folder structure, then implement auth, then the practice feature, then
resume builder, then cover letter, then thank you notes, then copilot, then pre-screen portal.
Document generated by Claude (Anthropic) · Deep research of interviewai.io · March 2026 · Angular 17 + Flask 3 Stack · For AI-agent
and developer use