# AI Job Application Copilot

AI Job Application Copilot is a full-stack GenAI application that helps candidates analyze how well their resume matches a target job description. It extracts skills from both the resume and job description, identifies matched and missing skills, generates an explainable fit score, and provides job-application support such as tailored resume bullets, cover letter generation, interview preparation, saved analysis history, and Markdown export.

The project is built as a production-style AI engineering portfolio project using FastAPI, React, LangChain, LangGraph, PostgreSQL, Docker, and OpenRouter-compatible LLM APIs.

---

## Features

### Resume and Job Analysis

* Upload or paste a resume
* Parse PDF, DOCX, and TXT resumes
* Paste a target job description
* Extract candidate skills from the resume
* Extract required skills from the job description
* Identify matched skills
* Identify missing or weakly represented skills
* Generate an explainable fit score
* Save each analysis run into PostgreSQL

### Optional GenAI Outputs

* Generate tailored resume bullet rewrites
* Generate a cover letter grounded in the resume
* Generate interview preparation questions with suggested answers
* Persist optional generated outputs back to the saved analysis record

### History and Export

* View saved analysis history
* Open detailed analysis records
* Delete saved analyses
* Export analysis details as a Markdown file

---

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS
* React Router
* Axios
* lucide-react

### Backend

* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy
* PostgreSQL
* PyMuPDF
* python-docx

### AI / LLM Workflow

* LangChain
* LangGraph
* OpenRouter as an OpenAI-compatible LLM provider
* JSON prompting with manual parsing
* Pydantic validation for structured LLM outputs

### DevOps

* Docker
* Docker Compose
* Environment-based configuration
* Render deployment planned

---

## High-Level Architecture

```txt
React Frontend
     |
     | HTTP API calls
     v
FastAPI Backend
     |
     | Service Layer
     v
LangGraph Analysis Workflow
     |
     | LangChain LLM Calls
     v
OpenRouter / OpenAI-Compatible LLM

FastAPI Backend
     |
     v
PostgreSQL
```

---

## LangGraph Workflow

The core analysis endpoint uses a LangGraph workflow for deterministic orchestration.

```txt
START
  |
  v
extract_skills
  |
  v
match_skills
  |
  v
score_fit
  |
  v
END
```

### Nodes

#### `extract_skills`

Extracts:

* Resume skills
* Job required skills
* Preferred skills
* Responsibilities
* Resume project experience

Resume and job skill extraction are run in parallel to reduce latency.

#### `match_skills`

Compares canonical skill names and produces:

* Resume skills
* Job required skills
* Matched skills
* Missing skills

#### `score_fit`

Calculates an explainable fit score using deterministic scoring logic based on:

* Required skill coverage
* Resume skill breadth
* Completeness bonus

The scoring is deterministic rather than LLM-based to keep results stable and explainable.

---

## Project Structure

```txt
ai-job-application-copilot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── routes/
│   │   │       │   ├── analysis.py
│   │   │       │   ├── health.py
│   │   │       │   ├── history.py
│   │   │       │   └── resume.py
│   │   │       └── router.py
│   │   │
│   │   ├── ai/
│   │   │   ├── chains/
│   │   │   ├── graphs/
│   │   │   ├── llm/
│   │   │   ├── nodes/
│   │   │   ├── prompts/
│   │   │   ├── utils/
│   │   │   └── state.py
│   │   │
│   │   ├── core/
│   │   ├── db/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── .dockerignore
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── Dockerfile
│   ├── package.json
│   └── .dockerignore
│
├── docker-compose.yml
└── README.md
```

---

## Backend API Endpoints

### Health

```txt
GET /api/v1/health
```

Returns API health status.

---

### Resume Parsing

```txt
POST /api/v1/resume/parse
```

Supports:

* PDF
* DOCX
* TXT

Returns extracted resume text and metadata.

If a PDF appears to be scanned or image-based, the backend marks it as scanned. OCR support is planned as a future improvement.

---

### Core Analysis

```txt
POST /api/v1/analysis/analyze
```

Request:

```json
{
  "resume_text": "Candidate resume text...",
  "job_description": "Target job description..."
}
```

Response includes:

```json
{
  "analysis_id": 1,
  "fit_score": 82,
  "fit_summary": "The candidate appears to be a strong match...",
  "resume_skills": [],
  "job_required_skills": [],
  "matched_skills": [],
  "missing_skills": [],
  "rewritten_bullets": [],
  "cover_letter": "",
  "interview_questions": []
}
```

---

### Resume Bullet Rewriting

```txt
POST /api/v1/analysis/rewrite-bullets
```

Generates tailored resume bullet suggestions and updates the saved analysis record when `analysis_id` is provided.

---

### Cover Letter Generation

```txt
POST /api/v1/analysis/cover-letter
```

Generates a cover letter grounded in the candidate resume and job description.

---

### Interview Preparation

```txt
POST /api/v1/analysis/interview-questions
```

Generates interview preparation questions with suggested answers, categories, difficulty, and evaluation focus.

---

### History

```txt
GET /api/v1/history
```

Returns saved analysis history.

```txt
GET /api/v1/history/{analysis_id}
```

Returns full analysis detail.

```txt
DELETE /api/v1/history/{analysis_id}
```

Deletes a saved analysis.

---

## Frontend Routes

```txt
/analyze
```

Main analysis page.

```txt
/history
```

Saved analysis history.

```txt
/history/:id
```

Detailed saved analysis page.

---

## Environment Variables

Create:

```txt
backend/.env
```

Example:

```env
APP_NAME=AI Job Application Copilot
APP_ENV=development
API_V1_PREFIX=/api/v1

BACKEND_CORS_ORIGINS=http://localhost:5173

DATABASE_URL=postgresql://postgres:postgres@localhost:5433/ai_job_copilot

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-oss-20b:free
LLM_TEMPERATURE=0.2
```

For Docker, the backend service uses:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/ai_job_copilot
```

Create:

```txt
frontend/.env
```

Example:

```env
VITE_BACKEND_API_URL=http://localhost:8000
```

---

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ai-job-application-copilot.git
cd ai-job-application-copilot
```

---

### 2. Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will run at:

```txt
http://localhost:8000
```

Swagger UI:

```txt
http://localhost:8000/docs
```

---

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at:

```txt
http://localhost:5173
```

---

## Docker Setup

Run the full stack with:

```bash
docker compose up --build
```

Services:

```txt
Frontend:   http://localhost:5173
Backend:    http://localhost:8000
Swagger:    http://localhost:8000/docs
PostgreSQL: localhost:5433
```

---

## Docker Compose Services

```txt
frontend
backend
postgres
```

The backend connects to PostgreSQL using the Docker service name:

```txt
postgres
```

So inside Docker:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/ai_job_copilot
```

For local non-Docker backend access to the Dockerized database:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/ai_job_copilot
```

---

## Current LLM Design Notes

The project uses OpenRouter through an OpenAI-compatible API interface.

Native structured output was not reliable across the selected OpenRouter free model, so the backend uses:

* JSON prompting
* Manual JSON extraction
* Pydantic schema validation
* Error handling around invalid model responses

The core analysis flow is intentionally separated from optional generation endpoints. This prevents long-running cover letter or interview generation from blocking the main fit analysis.

---

## Known Limitations

* OCR is not implemented yet for scanned/image-based PDFs.
* The selected free OpenRouter model may occasionally return invalid or empty structured output for longer generation tasks.
* Alembic migrations are not yet added; the MVP currently uses SQLAlchemy table creation during startup.
* Authentication is not implemented.
* Multi-user workspace support is not implemented yet.
* Deployment configuration for Render is planned but not finalized.

---

## Future Improvements

* Add OCR support for scanned resumes
* Add Alembic database migrations
* Add user authentication
* Add multi-user saved analysis workspace
* Add vector search over previous resumes and job descriptions
* Add job description quality scoring
* Add ATS-style keyword coverage report
* Add downloadable PDF export
* Add production frontend build using Nginx or Render Static Site
* Deploy backend, frontend, and PostgreSQL on Render
* Add GitHub Actions for linting and CI checks
* Add LangSmith tracing for LLM workflow observability

---

## Resume-Worthy Highlights

This project demonstrates:

* Full-stack GenAI application development
* FastAPI backend architecture
* React frontend development
* LangGraph workflow orchestration
* LangChain LLM integration
* OpenAI-compatible provider configuration through OpenRouter
* Structured LLM output validation with Pydantic
* PostgreSQL persistence
* Docker Compose orchestration
* Resume parsing and analysis
* Practical AI product design with history, export, and modular generation endpoints

---

## License

This project is intended for portfolio and educational use.
