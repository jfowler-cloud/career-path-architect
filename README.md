# 🗺️ Career Path Architect

> AI-powered career planning tool that designs personalized learning roadmaps using LangGraph and AWS Bedrock

[![AWS](https://img.shields.io/badge/AWS-Serverless-orange)](https://aws.amazon.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-purple)](https://langchain.com/)
[![Claude](https://img.shields.io/badge/Claude-Opus%204.5-purple)](https://www.anthropic.com/claude)
[![React](https://img.shields.io/badge/React-19-blue)](https://react.dev/)
[![Tests](https://img.shields.io/badge/Tests-128%20passing-brightgreen)](https://github.com)
[![Coverage](https://img.shields.io/badge/Coverage-99%25-brightgreen)](https://github.com)
[![MVP](https://img.shields.io/badge/MVP-2%20Days-success)](https://github.com)

---

## 🚀 Development Speed

| Milestone | Timeline | Highlights |
|-----------|----------|------------|
| **MVP Ready** | **2 Days** | Full-stack LangGraph multi-agent system with visual roadmap generation |
| **Enhanced Features** | **+1 Hour** | Progress tracking, path comparison, export, caching, rate limiting, validation |
| **Test Coverage** | **Continuous** | 99% coverage with 142 comprehensive tests |

> This project demonstrates **rapid AI agent development** using LangGraph and modern tooling (FastAPI + React + uv), achieving a production-quality multi-agent system in days instead of weeks.

---

## 📋 Overview

An intelligent career planning platform that analyzes your resume, compares it against target job descriptions, identifies skill gaps, and generates interactive visual learning roadmaps with courses, projects, and timelines. Built with LangGraph multi-agent orchestration and AWS Bedrock Claude Opus 4.5.

**Built for rapid iteration** - leveraging LangGraph's agent framework and modern Python tooling, this project went from concept to working MVP with visual roadmap generation in 2 days, then to production-ready with 97% test coverage within a week.

### My Philosophy: Honest Career Growth Through Actionable Insights

> **This tool isn't about gaming the system—it's about genuine skill development.**
>
> I built Career Path Architect to give you a clear, honest assessment of where you are and exactly what you need to learn to get where you want to go. It doesn't sugarcoat gaps or make false promises—it gives you a roadmap based on real skill requirements.
>
> **What this tool does:**
> - Analyzes your actual skills and experience from your resume
> - Identifies genuine gaps between your skills and target roles
> - Prioritizes what to learn based on importance and difficulty
> - Recommends specific courses, projects, and certifications
> - Creates a realistic timeline for skill development
> - Generates visual roadmaps to track your progress
>
> **What this tool does NOT do:**
> - Pretend you have skills you don't
> - Suggest shortcuts that skip real learning
> - Make unrealistic promises about career transitions
> - Hide the work required to reach your goals

### ✨ Key Features

- 📄 **Resume Analysis** - Extract skills, experience, and strengths using Claude Opus 4.5
- 🎯 **Job Description Parsing** - Analyze multiple target roles for required skills
- 🔍 **Intelligent Gap Analysis** - Identify and prioritize skill gaps with case-insensitive matching
- 📊 **Visual Roadmap** - Interactive React Flow canvas with color-coded nodes
- 🎓 **Course Recommendations** - Specific courses, books, and certifications for each gap
- 💻 **Project Ideas** - Hands-on projects to build missing skills
- ⏱️ **Timeline Estimation** - Realistic learning time estimates
- 🎨 **Interactive Canvas** - Drag, zoom, and explore your learning path
- 📈 **Progress Tracking** - Mark skills as not_started, in_progress, or completed
- 📊 **Completion Statistics** - Track percentage complete and time spent
- 🔄 **Career Path Comparison** - Compare two career paths side-by-side
- 💾 **Export Functionality** - Export roadmap as PNG or JSON
- ⚡ **Response Caching** - Cache LLM responses for faster performance
- 🔒 **Input Validation** - Comprehensive sanitization and validation
- ⚡ **Fast Generation** - Complete roadmap in 30-60 seconds
- 💰 **Cost-Effective** - Runs for ~$4-5/month on AWS
- ✅ **99% Test Coverage** - 128 tests with comprehensive mocking

---

## 🚀 Quick Start

### Prerequisites

- AWS Account with credentials configured (`aws configure`)
- Python 3.12+ with [uv](https://docs.astral.sh/uv/) installed
- Node.js 20+ and npm
- AWS Bedrock access to Claude Opus 4.5

### Run Backend (2 minutes)

```bash
# Clone repository
git clone https://github.com/jfowler-cloud/career-path-architect.git
cd career-path-architect/apps/backend

# Install dependencies with uv
uv sync

# Set AWS region
export AWS_REGION=us-east-1

# Run FastAPI server (port 8000)
uv run uvicorn career_path.main:app --reload
```

### Run Frontend (1 minute)

```bash
# In a new terminal
cd career-path-architect/apps/web

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start Next.js dev server (port 3000)
npm run dev
```

**Important:** Request access to Claude Opus 4.5 in [Bedrock Console](https://console.aws.amazon.com/bedrock/) → Model access before first use.

Open http://localhost:3000 and start building your career roadmap!

**Detailed guides:** [QUICKSTART.md](QUICKSTART.md) | [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 🏗️ Architecture

```
React Frontend (Next.js + React Flow)
        ↓
FastAPI Backend
        ↓
┌─────────────────────────────────────────┐
│  LangGraph Multi-Agent Workflow         │
│                                         │
│  1. Resume Analyzer Agent               │
│     - Extract skills, experience        │
│     - Identify strengths                │
│                                         │
│  2. Job Parser Agent                    │
│     - Parse job requirements            │
│     - Extract required skills           │
│                                         │
│  3. Gap Analysis Agent                  │
│     - Compare current vs target         │
│     - Prioritize skill gaps             │
│     - Calculate learning time           │
│                                         │
│  4. Learning Path Designer Agent        │
│     - Generate course recommendations   │
│     - Create project ideas              │
│     - Build timeline                    │
│                                         │
│  5. Roadmap Generator Agent             │
│     - Create React Flow nodes/edges     │
│     - Color-code by priority            │
│     - Generate visual layout            │
└─────────────────────────────────────────┘
        ↓
   AWS Bedrock (Claude Opus 4.5)
```

**Tech Stack:**
- **Frontend**: React 19 + TypeScript + Next.js 15 + React Flow
- **Backend**: FastAPI (Python 3.12+) + LangGraph
- **AI**: Amazon Bedrock (Claude Opus 4.5)
- **Package Management**: uv (Python), npm (Node.js)
- **Testing**: pytest + pytest-cov (97% coverage)
- **Monorepo**: Turborepo

---

## 💡 How It Works

1. **Upload Resume** - Paste your resume text (or upload file)
2. **Add Target Roles** - Enter 1-3 job titles you're targeting
3. **AI Analysis** - LangGraph agents analyze gaps and generate recommendations
4. **Visual Roadmap** - Interactive canvas shows your learning path with:
   - 🔴 High priority skills (hard, important)
   - 🟡 Medium priority skills (moderate difficulty)
   - 🟢 Low priority skills (easy, quick wins)
5. **Get Recommendations** - Specific courses, projects, and timeline for each skill
6. **Explore & Plan** - Drag, zoom, and interact with your roadmap

---

## 📸 Screenshots

### Upload Resume & Target Roles
![Upload Interface](docs/images/upload.png)
*Simple interface to paste resume and enter target job titles*

### Visual Learning Roadmap
![Roadmap Canvas](docs/images/roadmap.png)
*Interactive React Flow canvas with color-coded skill nodes and learning paths*

### Skill Gap Analysis
![Gap Analysis](docs/images/gaps.png)
*Detailed breakdown of missing skills with priority levels and learning time estimates*

### Course & Project Recommendations
![Recommendations](docs/images/recommendations.png)
*Specific courses, books, certifications, and hands-on projects for each skill gap*

---

## 🧪 Testing

**99% Test Coverage** with 128 comprehensive tests:

```bash
cd apps/backend
uv run pytest tests/ --cov=src/career_path --cov-report=term-missing
```

**Test Breakdown:**
- `test_utils.py` - 3 tests (100% coverage) - Utility functions
- `test_health.py` - 5 tests (100% coverage) - Health checks
- `test_nodes.py` - 17 tests (99% coverage) - LangGraph agents
- `test_workflow.py` - 2 tests (100% coverage) - Workflow creation
- `test_main.py` - 28 tests (95% coverage) - FastAPI endpoints
- `test_progress.py` - 14 tests (100% coverage) - Progress tracking
- `test_comparison.py` - 15 tests (100% coverage) - Path comparison
- `test_cache.py` - 19 tests (100% coverage) - Response caching
- `test_validation.py` - 30 tests (100% coverage) - Input validation

See [TEST_COVERAGE.md](TEST_COVERAGE.md) for detailed coverage report.

---

## 📊 Development Timeline

### ✅ Day 1: Core MVP
- [x] FastAPI backend setup with health checks
- [x] LangGraph multi-agent workflow (5 agents)
- [x] Resume analyzer agent
- [x] Job parser agent
- [x] Gap analysis agent with prioritization
- [x] Learning path designer agent
- [x] Roadmap generator agent
- [x] React Flow canvas integration
- [x] Next.js frontend with API integration
- [x] End-to-end roadmap generation

### ✅ Day 2: Polish & Features
- [x] Utility functions (deduplicate, prioritize, estimate time)
- [x] Health check utilities (AWS credentials, Bedrock access)
- [x] Constants and configuration
- [x] Error handling and validation
- [x] Loading states and UX improvements
- [x] Color-coded nodes by priority
- [x] Animated edges and better layout

### ✅ Day 3: Testing & Documentation
- [x] Comprehensive test suite (128 tests)
- [x] 99% test coverage
- [x] Test documentation
- [x] README updates
- [x] Quick start guide
- [x] Development guide

### ✅ Enhanced Features (+1 Hour)
- [x] Progress tracking system (14 tests)
- [x] Career path comparison (15 tests)
- [x] Export roadmap (PNG, JSON)
- [x] Response caching (19 tests)
- [x] Input validation and sanitization (30 tests)
- [x] Rate limiting (13 tests)
- [x] Cache management endpoints
- [x] API documentation
- [x] 99% test coverage (142 tests total)

### 🚧 Future Enhancements
- [ ] Integration with Resume Tailor AI
- [ ] Market intelligence (salary data, demand trends)
- [ ] Adaptive recommendations based on progress
- [ ] AWS deployment (ECS Fargate + CloudFront)
- [ ] User authentication (Cognito)
- [ ] DynamoDB persistence

---

## 🎓 Learning Objectives

This project demonstrates:
- **LangGraph Mastery**: Multi-agent orchestration with state management
- **Agent Design**: Specialized agents with clear responsibilities
- **Visual Design**: Interactive canvas with React Flow
- **Rapid Development**: MVP to production in 3 days
- **Test-Driven**: 99% coverage with comprehensive mocking
- **Modern Tooling**: uv, FastAPI, Next.js 15, React 19
- **Product Thinking**: Career planning as a service
- **AI-Assisted**: Enhanced with 100 tests in 1 hour

---

## 🔗 Related Projects

- **[Scaffold AI](https://github.com/jfowler-cloud/scaffold-ai)** - AWS architecture designer with multi-agent system
- **[Resume Tailor AI](https://github.com/jfowler-cloud/resume-tailor-ai)** - Resume optimization with Claude Opus 4.5

**Together, these projects form a complete AI-powered career development platform.**

---

## 💰 Estimated Costs

| Service | Monthly Usage | Cost |
|---------|--------------|------|
| Bedrock Claude Opus 4.5 | ~150K tokens | $4.50 |
| **Total (Local Dev)** | | **~$4-5/month** |

**Future AWS Deployment:**
| Service | Monthly Usage | Cost |
|---------|--------------|------|
| Cognito | 1 user | $0 (free tier) |
| ECS Fargate | 1 task (0.25 vCPU) | $3.50 |
| Bedrock Claude Opus 4.5 | ~150K tokens | $4.50 |
| DynamoDB | On-demand | $0.50 |
| S3 | ~2GB storage | $0.05 |
| CloudFront | ~1K requests | $0.01 |
| **Total (Deployed)** | | **~$8-9/month** |

---

## 🎨 Key Differentiators

### vs Scaffold AI
| Feature | Scaffold AI | Career Path Architect |
|---------|-------------|----------------------|
| **Purpose** | AWS architecture design | Career planning |
| **Agents** | 4 (Interpreter, Architect, Security, Code Gen) | 5 (Resume, Job, Gap, Learning, Roadmap) |
| **Output** | Infrastructure code | Learning roadmap |
| **Canvas** | AWS service nodes | Career milestones |
| **State** | Architecture graph | Skill gaps & progress |
| **Development** | 5 days to MVP | 2 days to MVP |

### Shared Patterns
- ✅ LangGraph multi-agent orchestration
- ✅ React Flow visual canvas
- ✅ FastAPI backend
- ✅ Bedrock Claude integration
- ✅ Comprehensive testing
- ✅ Rapid development workflow

---

## 🤝 Contributing

This project is currently in MVP phase. Contributions welcome! Please open an issue first to discuss proposed changes.

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 👤 Author

**James Fowler**
- GitHub: [@jfowler-cloud](https://github.com/jfowler-cloud)
- LinkedIn: [James Fowler - AWS Cloud Architect & DevOps Professional](https://www.linkedin.com/in/james-fowler-aws-cloud-architect-dev-ops-professional/)

---

## 💭 Personal Note

> "This is the tool I wish I had when planning my own career transition. By building it, I'm not only creating something useful for others but also demonstrating the exact skills I'm developing along the way. The rapid development timeline (2 days to MVP) showcases what's possible with modern AI-assisted development and the right tooling."

---

**Built with ❤️ to help professionals navigate their career growth**
| DynamoDB | On-demand | $0.50 |
| S3 | ~2GB storage | $0.05 |
| CloudFront | ~1K requests | $0.01 |
| **Total** | | **~$8-9/month** |

---

## 🎨 Key Differentiators

### vs Scaffold AI
| Feature | Scaffold AI | Career Path Architect |
|---------|-------------|----------------------|
| **Purpose** | AWS architecture design | Career planning |
| **Agents** | 4 (Interpreter, Architect, Security, Code Gen) | 6 (Resume, Job, Gap, Learning, Market, Roadmap) |
| **Output** | Infrastructure code | Learning roadmap |
| **Canvas** | AWS service nodes | Career milestones |
| **State** | Architecture graph | Progress tracking |

### Shared Patterns
- ✅ LangGraph multi-agent orchestration
- ✅ React Flow visual canvas
- ✅ AWS Cloudscape UI
- ✅ FastAPI backend
- ✅ Bedrock Claude integration
- ✅ Security-first design

---

## 🤝 Contributing

This project is currently in planning phase. Contributions will be welcome once the MVP is complete.

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 👤 Author

**James Fowler**
- GitHub: [@jfowler-cloud](https://github.com/jfowler-cloud)
- LinkedIn: [James Fowler - AWS Cloud Architect & DevOps Professional](https://www.linkedin.com/in/james-fowler-aws-cloud-architect-dev-ops-professional/)

---

## 🎯 Next Steps

1. **LangGraph Workflow Design** - Define agent interactions and state
2. **UI Wireframes** - Canvas layout and interaction patterns
3. **FastAPI Setup** - Backend structure from Scaffold AI
4. **Resume Analyzer Agent** - First agent implementation
5. **React Flow Canvas** - Visual roadmap component

**Target MVP Date**: March 2026

---

## 💭 Personal Note

> "This is the tool I wish I had when planning my own career transition. By building it, I'm not only creating something useful for others but also demonstrating the exact skills I'm developing along the way."

---

**Built with ❤️ to help professionals navigate their career growth**
