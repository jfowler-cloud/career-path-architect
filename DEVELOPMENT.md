# Development Guide - Career Path Architect

## Quick Start

```bash
# Install git hooks
./scripts/install-git-hooks.sh

# Start development (runs both backend and frontend)
./dev.sh
```

## Manual Setup

### Backend

```bash
cd apps/backend

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your AWS credentials

# Run server
uv run uvicorn career_path.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd apps/web

# Install dependencies (from root)
cd ../..
pnpm install

# Configure environment
cd apps/web
cp .env.local.example .env.local

# Run development server
pnpm dev
```

## Project Structure

```
career-path-architect/
├── apps/
│   ├── backend/                 # FastAPI + LangGraph
│   │   ├── src/career_path/
│   │   │   ├── main.py         # FastAPI app
│   │   │   ├── graph/          # LangGraph workflow
│   │   │   │   ├── state.py    # State definition
│   │   │   │   ├── nodes.py    # Agent implementations
│   │   │   │   └── workflow.py # Workflow definition
│   │   │   ├── agents/         # (Future) Additional agents
│   │   │   ├── services/       # (Future) Business logic
│   │   │   └── tools/          # (Future) Utility functions
│   │   ├── pyproject.toml      # Python dependencies
│   │   └── .env                # Environment variables
│   │
│   └── web/                    # Next.js 15 frontend
│       ├── app/
│       │   ├── layout.tsx      # Root layout
│       │   └── page.tsx        # Main page
│       ├── components/
│       │   └── RoadmapCanvas.tsx  # React Flow canvas
│       ├── lib/                # (Future) Utilities
│       ├── package.json
│       └── .env.local          # Frontend config
│
├── packages/                   # (Future) Shared packages
├── package.json                # Root package.json
├── pnpm-workspace.yaml         # Workspace config
└── turbo.json                  # Turborepo config
```

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangGraph** - Multi-agent workflow orchestration
- **LangChain** - LLM integration
- **AWS Bedrock** - Claude Sonnet 4.5
- **Boto3** - AWS SDK
- **Pydantic** - Data validation
- **uv** - Fast Python package manager

### Frontend
- **Next.js 15** - React framework with App Router
- **React 19** - UI library
- **Cloudscape Design System** - AWS-style components
- **React Flow** - Visual graph editor
- **Zustand** - State management (future)
- **TypeScript** - Type safety

## API Usage

### Generate Roadmap

```bash
curl -X POST http://localhost:8000/api/roadmaps/generate \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Senior Software Engineer with 5 years experience in Python, AWS, and React...",
    "target_jobs": ["Cloud Solutions Architect"],
    "user_id": "demo"
  }'
```

### Health Check

```bash
curl http://localhost:8000/health
```

## LangGraph Workflow

The workflow consists of 5 agents that run sequentially:

1. **Resume Analyzer** (`resume_analyzer_node`)
   - Extracts technical skills
   - Identifies years of experience
   - Highlights strengths

2. **Job Parser** (`job_parser_node`)
   - Analyzes target job requirements
   - Separates required vs nice-to-have skills

3. **Gap Analysis** (`gap_analysis_node`)
   - Compares current skills vs requirements
   - Prioritizes skill gaps
   - Estimates learning time

4. **Learning Path Designer** (`learning_path_node`)
   - Recommends online courses
   - Suggests hands-on projects
   - Identifies relevant certifications

5. **Roadmap Generator** (`roadmap_generator_node`)
   - Creates React Flow nodes and edges
   - Defines milestones
   - Generates visual roadmap

## Development Workflow

### Adding a New Agent

1. Define agent function in `apps/backend/src/career_path/graph/nodes.py`
2. Add node to workflow in `apps/backend/src/career_path/graph/workflow.py`
3. Update state in `apps/backend/src/career_path/graph/state.py` if needed

### Adding a New Frontend Component

1. Create component in `apps/web/components/`
2. Import and use in `apps/web/app/page.tsx`
3. Add types if needed

## Testing

### Backend Tests (Future)

```bash
cd apps/backend
uv run pytest
uv run pytest --cov=career_path
```

### Frontend Tests (Future)

```bash
cd apps/web
pnpm test
```

## Deployment (Future)

### Backend
- Deploy to AWS ECS Fargate
- Or AWS Lambda with Function URLs

### Frontend
- Deploy to Vercel
- Or CloudFront + S3

## Environment Variables

### Backend (.env)
```
AWS_PROFILE=default
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Troubleshooting

### Backend won't start
- Check AWS credentials: `aws sts get-caller-identity`
- Verify Bedrock model access in AWS Console
- Check Python version: `python3 --version` (need 3.12+)

### Frontend won't start
- Clear Next.js cache: `rm -rf apps/web/.next`
- Reinstall dependencies: `pnpm install --force`
- Check Node version: `node --version` (need 22+)

### CORS errors
- Verify `ALLOWED_ORIGINS` in backend `.env`
- Check frontend is running on `http://localhost:3000`

## Next Steps

- [ ] Add authentication (Cognito)
- [ ] Add database persistence (DynamoDB)
- [ ] Add progress tracking
- [ ] Add roadmap editing
- [ ] Add export functionality (PDF, PNG)
- [ ] Add tests
- [ ] Add CI/CD pipeline
