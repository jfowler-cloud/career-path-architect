# 🗺️ Career Path Architect

> AI-powered career planning tool that designs personalized learning roadmaps using LangGraph and AWS Bedrock

[![AWS](https://img.shields.io/badge/AWS-Serverless-orange)](https://aws.amazon.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-purple)](https://langchain.com/)
[![Claude](https://img.shields.io/badge/Claude-Opus%204.5-purple)](https://www.anthropic.com/claude)
[![React](https://img.shields.io/badge/React-19-blue)](https://react.dev/)
[![Status](https://img.shields.io/badge/Status-Planning-yellow)](https://github.com)

---

## 🎯 Project Vision

An intelligent career planning platform that analyzes your current skills, identifies gaps for target roles, and generates visual learning roadmaps with actionable project ideas. Built using LangGraph multi-agent architecture from [Scaffold AI](https://github.com/jfowler-cloud/scaffold-ai).

**Portfolio Position**: Demonstrates advanced AI orchestration and the tool that planned my own career growth.

---

## ✨ Planned Features

### Phase 1: Core Analysis (Week 1)
- 📄 **Resume Analysis** - Extract current skills, experience, and strengths
- 🎯 **Target Role Parsing** - Analyze job descriptions for required skills
- 🔍 **Gap Identification** - AI-powered skill gap analysis with prioritization
- 📊 **Visual Roadmap** - React Flow canvas showing learning path

### Phase 2: Learning Path Generation (Week 2)
- 🎓 **Course Recommendations** - AWS certifications, online courses, books
- 💻 **Project Ideas** - Hands-on projects to build missing skills
- ⏱️ **Timeline Planning** - Realistic milestones based on time commitment
- 🏆 **Certification Paths** - AWS, Azure, GCP certification roadmaps

### Phase 3: Intelligence & Tracking (Week 3)
- 🔄 **Progress Tracking** - Mark completed courses, projects, certifications
- 🧠 **Adaptive Recommendations** - Adjust path based on progress
- 📈 **Market Insights** - Salary ranges, demand trends, competition level
- 🎨 **Multiple Career Paths** - Compare different role trajectories

---

## 🏗️ Planned Architecture

```
React Frontend (Cloudscape + React Flow)
        ↓
Cognito Authentication
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
│                                         │
│  4. Learning Path Designer Agent        │
│     - Generate course recommendations   │
│     - Create project ideas              │
│     - Build timeline                    │
│                                         │
│  5. Market Intelligence Agent           │
│     - Salary data                       │
│     - Demand trends                     │
│     - Competition analysis              │
│                                         │
│  6. Roadmap Generator Agent             │
│     - Create visual graph nodes         │
│     - Define dependencies               │
│     - Generate milestones               │
└─────────────────────────────────────────┘
```

**Tech Stack:**
- **Frontend**: React 19 + TypeScript + Next.js 15 + Cloudscape + React Flow
- **Backend**: FastAPI (Python 3.12+)
- **AI Orchestration**: LangGraph (multi-agent workflow)
- **LLM**: Amazon Bedrock (Claude Opus 4.5)
- **Authentication**: AWS Cognito
- **Storage**: DynamoDB (progress tracking) + S3 (documents)
- **Deployment**: ECS Fargate (backend) + CloudFront (frontend)
- **IaC**: AWS CDK (TypeScript)

---

## 🚀 Quick Start (Coming Soon)

```bash
# Clone repository
git clone https://github.com/jfowler-cloud/career-path-architect.git
cd career-path-architect

# Install dependencies
pnpm install

# Backend setup
cd apps/backend
uv sync
cp .env.example .env
# Edit .env with AWS credentials

# Run backend (port 8000)
uv run uvicorn career_path.main:app --reload

# Run frontend (port 3000)
cd ../web
pnpm dev
```

---

## 💡 How It Will Work

1. **Upload Resume** - Provide your current resume (or import from Resume Tailor AI)
2. **Add Target Roles** - Paste job descriptions for roles you're targeting
3. **AI Analysis** - Multi-agent system analyzes gaps and opportunities
4. **Visual Roadmap** - Interactive canvas shows your learning path
5. **Get Recommendations** - Courses, projects, certifications, and timeline
6. **Track Progress** - Mark items complete and watch your path evolve

---

## 📊 Development Roadmap

### ✅ Phase 0: Planning (Current)
- [x] Project concept and architecture design
- [x] Repository setup with best practices
- [x] README and documentation structure
- [ ] LangGraph workflow design
- [ ] UI/UX wireframes for canvas

### 🚧 Phase 1: MVP (Target: 7 days)
- [ ] FastAPI backend setup
- [ ] LangGraph multi-agent workflow
- [ ] Resume analyzer agent
- [ ] Job parser agent
- [ ] Gap analysis agent
- [ ] Basic React Flow canvas
- [ ] Cognito authentication

### 📋 Phase 2: Enhanced Features (Target: 7 days)
- [ ] Learning path designer agent
- [ ] Course and project recommendations
- [ ] Timeline generation
- [ ] Interactive roadmap editing
- [ ] Progress tracking (DynamoDB)
- [ ] Export roadmap (PDF, PNG)

### 🎯 Phase 3: Advanced Features (Target: 7 days)
- [ ] Market intelligence agent
- [ ] Salary and demand data
- [ ] Multiple career path comparison
- [ ] Adaptive recommendations
- [ ] Integration with Resume Tailor AI
- [ ] Certification path templates

### 🚀 Phase 4: Production Ready
- [ ] Comprehensive testing (unit + integration)
- [ ] CI/CD pipeline
- [ ] ECS Fargate deployment
- [ ] Cost optimization
- [ ] Documentation and demos

---

## 🎓 Learning Objectives

This project demonstrates:
- **LangGraph Mastery**: Complex multi-agent orchestration
- **Dynamic Routing**: Agent decisions based on analysis results
- **State Management**: Workflow state with checkpointing
- **Visual Design**: Interactive canvas with React Flow
- **Product Thinking**: Career planning as a service
- **Framework Reuse**: Leveraging Scaffold AI patterns

---

## 🔗 Related Projects

- **[Scaffold AI](https://github.com/jfowler-cloud/scaffold-ai)** - AWS architecture designer (architecture foundation)
- **[Resume Tailor AI](https://github.com/jfowler-cloud/resume-tailor-ai)** - Resume optimization (data source)
- **Interview Prep AI Coach** - Interview preparation tool (coming soon)

**Together, these projects form a complete AI-powered career development platform.**

---

## 💰 Estimated Costs

| Service | Monthly Usage | Cost |
|---------|--------------|------|
| Cognito | 1 user | $0 (free tier) |
| ECS Fargate | 1 task (0.25 vCPU) | $3.50 |
| Bedrock Claude Opus 4.5 | ~150K tokens | $4.50 |
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
