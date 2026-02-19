# Career Path Architect - Backend

FastAPI backend with LangGraph multi-agent workflow for career path analysis.

## Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Copy environment file
cp .env.example .env
# Edit .env with your AWS credentials

# Run development server
uv run uvicorn career_path.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Generate Roadmap
```bash
POST /api/roadmaps/generate
Content-Type: application/json

{
  "resume_text": "Your resume here...",
  "target_jobs": ["Senior Cloud Architect"],
  "user_id": "demo"
}
```

## Architecture

### LangGraph Workflow

1. **Resume Analyzer** - Extracts skills and experience
2. **Job Parser** - Analyzes target job requirements
3. **Gap Analysis** - Identifies skill gaps
4. **Learning Path** - Recommends courses and projects
5. **Roadmap Generator** - Creates visual roadmap nodes

### Tech Stack

- FastAPI - Web framework
- LangGraph - Multi-agent orchestration
- LangChain - LLM integration
- AWS Bedrock - Claude Sonnet 4.5
- Pydantic - Data validation
