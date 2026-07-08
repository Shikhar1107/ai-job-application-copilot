# Render Deployment Guide

This guide explains how to deploy **AI Job Application Copilot** on Render.

The project has three deployable parts:

```txt
1. PostgreSQL database
2. FastAPI backend
3. React frontend
```

Recommended Render setup:

```txt
Render PostgreSQL
Render Web Service for FastAPI backend
Render Static Site for React frontend
```

Render supports Python web services, static sites, environment variables, managed PostgreSQL, and Git-based auto-deploys. FastAPI services commonly use a Uvicorn start command with Render’s `$PORT` variable. Static sites are served through Render’s CDN with managed TLS and Git-based deploys. Environment variables should be configured in the Render dashboard instead of being committed to Git.

---

## 1. Prerequisites

Before deploying, make sure the project is pushed to GitHub.

```bash
git add .
git commit -m "Prepare project for Render deployment"
git push origin main
```

Also make sure these files are not committed:

```txt
backend/.env
frontend/.env
.venv/
node_modules/
```

Use `.env.example` files for documentation only.

---

## 2. Create Render PostgreSQL Database

In the Render Dashboard:

```txt
New +  >  Postgres
```

Suggested settings:

```txt
Name: ai-job-copilot-db
Database: ai_job_copilot
User: ai_job_copilot_user
Region: Same region as backend
Plan: Free or lowest suitable plan
```

After creation, open the database Info page and copy the **Internal Database URL**.

Render recommends using the internal URL when the connecting service and database are in the same account and region.

It will look similar to:

```txt
postgresql://user:password@host:5432/database
```

This will be used as:

```env
DATABASE_URL=<internal_database_url>
```

---

## 3. Deploy FastAPI Backend

In the Render Dashboard:

```txt
New +  >  Web Service
```

Connect your GitHub repository:

```txt
ai-job-application-copilot
```

Use these settings:

```txt
Name: ai-job-copilot-backend
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Render’s FastAPI guide uses the same pattern: install dependencies from `requirements.txt` and run Uvicorn on `0.0.0.0` with `$PORT`.

---

## 4. Backend Environment Variables

Add these environment variables to the backend service in Render:

```env
APP_NAME=AI Job Application Copilot
APP_ENV=production
API_V1_PREFIX=/api/v1

DATABASE_URL=<render_internal_postgres_url>

BACKEND_CORS_ORIGINS=https://your-frontend-service.onrender.com

OPENROUTER_API_KEY=<your_openrouter_api_key>
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-oss-20b:free
LLM_TEMPERATURE=0.2
```

At this stage, you will not know the frontend URL yet. Temporarily use:

```env
BACKEND_CORS_ORIGINS=*
```

or use your expected frontend URL and update it after frontend deployment.

For a cleaner production setup, avoid `*` once your frontend URL is known.

---

## 5. Run Database Migrations on Render

The project uses Alembic migrations.

Recommended approach:

Use Render’s **Pre-Deploy Command** for the backend service:

```bash
alembic upgrade head
```

Render supports a pre-deploy command that runs after build and before the start command, and it is recommended for tasks such as database migrations.

Backend service configuration:

```txt
Build Command:
pip install -r requirements.txt

Pre-Deploy Command:
alembic upgrade head

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

This ensures the database schema is upgraded before the backend starts.

---

## 6. Deploy React Frontend as Static Site

In the Render Dashboard:

```txt
New +  >  Static Site
```

Connect the same GitHub repository:

```txt
ai-job-application-copilot
```

Use these settings:

```txt
Name: ai-job-copilot-frontend
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

Render Static Sites are suitable for React frontends and serve static assets over a CDN.

---

## 7. Frontend Environment Variables

Add this environment variable to the frontend static site:

```env
VITE_BACKEND_API_URL=https://your-backend-service.onrender.com
```

Example:

```env
VITE_BACKEND_API_URL=https://ai-job-copilot-backend.onrender.com
```

Important:

Vite environment variables are baked into the frontend at build time. After changing `VITE_BACKEND_API_URL`, redeploy the frontend.

---

## 8. Update Backend CORS

After the frontend is deployed, copy its Render URL.

Example:

```txt
https://ai-job-copilot-frontend.onrender.com
```

Go back to the backend service environment variables and update:

```env
BACKEND_CORS_ORIGINS=https://ai-job-copilot-frontend.onrender.com
```

Then redeploy the backend.

---

## 9. Test Production Deployment

Test backend health:

```txt
https://your-backend-service.onrender.com/api/v1/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "AI Job Application Copilot API",
  "version": "v1"
}
```

Test frontend:

```txt
https://your-frontend-service.onrender.com
```

Full flow to test:

```txt
1. Open frontend
2. Upload or paste resume
3. Paste job description
4. Run analysis
5. Confirm fit score appears
6. Generate resume bullets
7. Open history page
8. Open analysis detail
9. Download Markdown
10. Delete test analysis
```

---

## 10. Render Service Summary

| Component | Render Type | Root Directory | Build Command                     | Start / Publish                                    |
| --------- | ----------- | -------------- | --------------------------------- | -------------------------------------------------- |
| Backend   | Web Service | `backend`      | `pip install -r requirements.txt` | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Frontend  | Static Site | `frontend`     | `npm install && npm run build`    | `dist`                                             |
| Database  | PostgreSQL  | N/A            | N/A                               | Internal DB URL                                    |

---

## 11. Common Issues

### Backend cannot connect to database

Check that:

```env
DATABASE_URL=<Render Internal Database URL>
```

Do not use the local Docker URL:

```env
postgresql://postgres:postgres@postgres:5432/ai_job_copilot
```

That only works inside Docker Compose.

---

### Frontend cannot reach backend

Check frontend env:

```env
VITE_BACKEND_API_URL=https://your-backend-service.onrender.com
```

Then redeploy frontend.

Also check backend CORS:

```env
BACKEND_CORS_ORIGINS=https://your-frontend-service.onrender.com
```

Then redeploy backend.

---

### Refreshing `/history/1` gives 404

Render Static Sites usually support rewrite rules, but if direct route refresh fails, add a rewrite rule:

```txt
Source: /*
Destination: /index.html
Action: Rewrite
```

This is needed for React Router client-side routes.

---

### Alembic migration fails

Check:

```txt
backend/alembic.ini
backend/alembic/env.py
DATABASE_URL
```

Also confirm that `alembic` exists in:

```txt
backend/requirements.txt
```

---

### Free services are slow after inactivity

Render free services may spin down or have limitations. Render notes that free services are best for testing, hobby projects, and previews, not production workloads.

---

## 12. Production Notes

Before treating this as production-ready:

```txt
1. Replace wildcard CORS with the real frontend URL
2. Use a stable paid LLM/provider model for long generations
3. Add authentication
4. Add rate limiting
5. Add request size limits
6. Add logging and monitoring
7. Add proper error reporting
8. Use non-free database/service tiers for reliability
```

---

## 13. Recommended Render Deployment Order

```txt
1. Push code to GitHub
2. Create Render PostgreSQL
3. Deploy backend web service
4. Add backend environment variables
5. Add backend pre-deploy command: alembic upgrade head
6. Test backend health endpoint
7. Deploy frontend static site
8. Add frontend VITE_BACKEND_API_URL
9. Update backend BACKEND_CORS_ORIGINS
10. Test full app flow
```
