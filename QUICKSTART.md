# 🚀 Quick Start - Career Path Architect

## Prerequisites

- Python 3.12+
- Node.js 22+
- pnpm 10+
- AWS CLI configured with Bedrock access
- uv (Python package manager)

## Installation

```bash
# 1. Clone repository
git clone https://github.com/jfowler-cloud/career-path-architect.git
cd career-path-architect

# 2. Install git hooks
./scripts/install-git-hooks.sh

# 3. Configure backend
cd apps/backend
cp .env.example .env
# Edit .env with your AWS credentials

# 4. Start development
cd ../..
./dev.sh
```

## What Gets Started

- **Backend**: http://localhost:8000 (FastAPI + LangGraph)
- **Frontend**: http://localhost:3000 (Next.js 15)
- **API Docs**: http://localhost:8000/docs

## First Use

1. Open http://localhost:3000
2. Paste your resume in the text area
3. Enter target job title (e.g., "Senior Cloud Architect")
4. Click "Generate Roadmap"
5. View your personalized career roadmap!

## Manual Setup

### Backend Only

```bash
cd apps/backend
uv sync
cp .env.example .env
uv run uvicorn career_path.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Only

```bash
# From project root
pnpm install
cd apps/web
cp .env.local.example .env.local
pnpm dev
```

## Test the API

```bash
# Health check
curl http://localhost:8000/health

# Generate roadmap
curl -X POST http://localhost:8000/api/roadmaps/generate \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Senior Software Engineer with 5 years Python and AWS experience",
    "target_jobs": ["Cloud Solutions Architect"],
    "user_id": "demo"
  }'
```

## Troubleshooting

### "uv: command not found"
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "pnpm: command not found"
```bash
npm install -g pnpm
```

### AWS Bedrock Access Denied
1. Go to AWS Console → Bedrock → Model access
2. Request access to Claude 3.5 Sonnet
3. Wait for approval (usually instant)

### CORS Errors
- Ensure backend is running on port 8000
- Ensure frontend is running on port 3000
- Check `ALLOWED_ORIGINS` in backend `.env`

## Next Steps

- Read [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development guide
- Read [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) for architecture details
- Check [README.md](README.md) for project overview

## Quick Commands

```bash
# Start everything
./dev.sh

# Backend only
cd apps/backend && uv run uvicorn career_path.main:app --reload

# Frontend only
cd apps/web && pnpm dev

# Run tests (when available)
pnpm test

# Lint code
pnpm lint

# Clean everything
pnpm clean
```

---

**Built with ❤️ using FastAPI, LangGraph, Next.js 15, and Claude Sonnet 4.5**
