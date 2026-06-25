ResumeIQ — Agentic Resume Analysis System

User Input
├── Resume (PDF/text)
└── Job Description (text)
         ↓
    LangGraph Orchestrator
         ↓
┌────────────────────────────┐
│     4 Specialized Agents   │
├────────────────────────────┤
│ Agent 1: JD Analyzer       │
│ → Extracts required skills │
│ → Identifies key keywords  │
│ → Scores role seniority    │
├────────────────────────────┤
│ Agent 2: Resume Analyzer   │
│ → Parses resume sections   │
│ → Extracts current skills  │
│ → Identifies weak bullets  │
├────────────────────────────┤
│ Agent 3: Gap Analyzer      │
│ → Compares JD vs Resume    │
│ → Scores match percentage  │
│ → Prioritizes skill gaps   │
├────────────────────────────┤
│ Agent 4: Content Generator │
│ → Rewrites weak bullets    │
│ → Generates cover letter   │
│ → Creates interview prep   │
└────────────────────────────┘
         ↓
    FastAPI Backend
         ↓
    Render Deployment


So final stack becomes: 
Backend: FastAPI
Frontend: React + Vite
Styling: Tailwind CSS
AI Workflow: LangGraph + LangChain
Database: PostgreSQL
ORM: SQLAlchemy
Migrations: Alembic
LLM Provider: OpenRouter / OpenAI-compatible API
Deployment: Render

                         ┌────────────────────────────┐
                         │       React Frontend        │
                         │   Vite + Tailwind CSS       │
                         │                            │
                         │ - Resume input/upload       │
                         │ - Job description input     │
                         │ - Fit score dashboard       │
                         │ - Skill gap tables          │
                         │ - Cover letter view         │
                         │ - Interview prep section    │
                         │ - Analysis history page     │
                         └──────────────┬─────────────┘
                                        │
                                        │ REST API
                                        ▼
┌────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend                          │
│                                                                │
│  ┌────────────────────┐     ┌───────────────────────────────┐  │
│  │ API Routes         │     │ Services Layer                 │  │
│  │ /analyze           │     │ Resume parsing                 │  │
│  │ /history           │     │ Job parsing                    │  │
│  │ /health            │     │ Analysis handling              │  │
│  └─────────┬──────────┘     └───────────────┬───────────────┘  │
│            │                                │                  │
│            ▼                                ▼                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 LangGraph AI Workflow                    │  │
│  │                                                          │  │
│  │ Extract JD Skills → Extract Resume Skills → Match Skills │  │
│  │ → Score Fit → Rewrite Bullets → Cover Letter → Questions │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                             │                                  │
│                             ▼                                  │
│                  OpenRouter / OpenAI-compatible LLM            │
│                                                                │
│  ┌────────────────────┐          ┌──────────────────────────┐ │
│  │ PostgreSQL          │          │ Vector Store Later       │ │
│  │ Analysis history    │          │ ChromaDB / Qdrant        │ │
│  └────────────────────┘          └──────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘