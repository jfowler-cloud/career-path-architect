# Technical Specification - Career Path Architect

## 1. System Architecture

### High-Level Components
```
┌─────────────────────────────────────────────────────────────┐
│                     CloudFront (CDN)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Next.js Frontend (Vercel/CloudFront)           │
│  - React 19 + Server Components                             │
│  - Cloudscape Design System                                 │
│  - React Flow for visual roadmaps                           │
│  - Zustand for state management                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    AWS Cognito                              │
│  - User authentication                                      │
│  - JWT token management                                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (ECS Fargate)              │
│  - RESTful API endpoints                                    │
│  - LangGraph workflow orchestration                         │
│  - Async request handling                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              LangGraph Multi-Agent Workflow                 │
│                                                             │
│  ┌─────────────────────────────────────────────────┐       │
│  │  1. Resume Analyzer Agent                       │       │
│  │     - Extract skills and experience             │       │
│  │     - Identify strengths                        │       │
│  └─────────────────────────────────────────────────┘       │
│                        ↓                                    │
│  ┌─────────────────────────────────────────────────┐       │
│  │  2. Job Parser Agent                            │       │
│  │     - Parse job requirements                    │       │
│  │     - Extract required skills                   │       │
│  └─────────────────────────────────────────────────┘       │
│                        ↓                                    │
│  ┌─────────────────────────────────────────────────┐       │
│  │  3. Gap Analysis Agent                          │       │
│  │     - Compare current vs target                 │       │
│  │     - Prioritize skill gaps                     │       │
│  └─────────────────────────────────────────────────┘       │
│                        ↓                                    │
│  ┌─────────────────────────────────────────────────┐       │
│  │  4. Learning Path Designer Agent                │       │
│  │     - Generate course recommendations           │       │
│  │     - Create project ideas                      │       │
│  │     - Build timeline                            │       │
│  └─────────────────────────────────────────────────┘       │
│                        ↓                                    │
│  ┌─────────────────────────────────────────────────┐       │
│  │  5. Market Intelligence Agent                   │       │
│  │     - Salary data                               │       │
│  │     - Demand trends                             │       │
│  │     - Competition analysis                      │       │
│  └─────────────────────────────────────────────────┘       │
│                        ↓                                    │
│  ┌─────────────────────────────────────────────────┐       │
│  │  6. Roadmap Generator Agent                     │       │
│  │     - Create visual graph nodes                 │       │
│  │     - Define dependencies                       │       │
│  │     - Generate milestones                       │       │
│  └─────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
│  - S3: Resumes, roadmaps, exports                          │
│  - DynamoDB: User data, progress, roadmap state            │
│  - Bedrock: Claude Opus 4.5 for AI processing              │
└─────────────────────────────────────────────────────────────┘
```

## 2. LangGraph Workflow Design

### State Definition
```python
from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph

class CareerPathState(TypedDict):
    # Input
    resume_text: str
    target_jobs: List[str]
    user_id: str
    
    # Resume Analysis
    current_skills: List[str]
    experience_years: Dict[str, int]
    strengths: List[str]
    
    # Job Analysis
    required_skills: Dict[str, List[str]]  # job_title -> skills
    nice_to_have_skills: Dict[str, List[str]]
    
    # Gap Analysis
    skill_gaps: List[Dict[str, any]]  # [{skill, priority, difficulty}]
    estimated_time: Dict[str, int]  # skill -> months
    
    # Learning Path
    courses: List[Dict[str, any]]
    projects: List[Dict[str, any]]
    certifications: List[Dict[str, any]]
    
    # Market Intelligence
    salary_range: Dict[str, tuple]  # job_title -> (min, max)
    demand_score: Dict[str, int]  # job_title -> 0-100
    competition_level: Dict[str, str]  # job_title -> low/medium/high
    
    # Roadmap
    nodes: List[Dict[str, any]]  # React Flow nodes
    edges: List[Dict[str, any]]  # React Flow edges
    milestones: List[Dict[str, any]]
    
    # Metadata
    workflow_status: str
    error: Optional[str]
```

### Agent Implementations

#### 1. Resume Analyzer Agent
```python
def resume_analyzer_node(state: CareerPathState) -> CareerPathState:
    """Extract skills and experience from resume."""
    prompt = f"""
    Analyze this resume and extract:
    1. Technical skills (programming languages, frameworks, tools)
    2. Years of experience per skill
    3. Key strengths and achievements
    
    Resume:
    {state['resume_text']}
    
    Return JSON format.
    """
    
    response = bedrock_client.invoke_model(
        modelId="us.anthropic.claude-3-opus-20240229-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000
        })
    )
    
    # Parse and update state
    result = parse_json_response(response)
    state['current_skills'] = result['skills']
    state['experience_years'] = result['experience']
    state['strengths'] = result['strengths']
    
    return state
```

#### 2. Gap Analysis Agent
```python
def gap_analysis_node(state: CareerPathState) -> CareerPathState:
    """Identify and prioritize skill gaps."""
    current = set(state['current_skills'])
    
    gaps = []
    for job_title, required in state['required_skills'].items():
        missing = set(required) - current
        for skill in missing:
            gaps.append({
                'skill': skill,
                'for_job': job_title,
                'priority': calculate_priority(skill, job_title),
                'difficulty': estimate_difficulty(skill),
                'time_months': estimate_learning_time(skill)
            })
    
    # Sort by priority
    gaps.sort(key=lambda x: x['priority'], reverse=True)
    state['skill_gaps'] = gaps
    
    return state
```

## 3. Data Models

### DynamoDB Tables

#### Users Table
```typescript
{
  PK: "USER#<userId>",
  SK: "PROFILE",
  email: string,
  name: string,
  currentRole: string,
  targetRoles: string[],
  createdAt: string,
  lastUpdated: string
}
```

#### Roadmaps Table
```typescript
{
  PK: "USER#<userId>",
  SK: "ROADMAP#<roadmapId>",
  roadmapId: string,
  name: string,
  targetJob: string,
  status: "active" | "completed" | "archived",
  createdAt: string,
  nodes: ReactFlowNode[],
  edges: ReactFlowEdge[],
  progress: {
    completedItems: number,
    totalItems: number,
    percentage: number
  }
}
```

#### Progress Table
```typescript
{
  PK: "USER#<userId>",
  SK: "PROGRESS#<itemId>",
  itemId: string,
  type: "course" | "project" | "certification",
  name: string,
  status: "not_started" | "in_progress" | "completed",
  startedAt?: string,
  completedAt?: string,
  notes: string
}
```

## 4. API Endpoints

### Resume Management
- `POST /api/resumes` - Upload resume
- `GET /api/resumes` - List resumes
- `GET /api/resumes/{id}` - Get resume details

### Roadmap Generation
- `POST /api/roadmaps/generate` - Generate new roadmap
- `GET /api/roadmaps` - List user's roadmaps
- `GET /api/roadmaps/{id}` - Get roadmap details
- `PUT /api/roadmaps/{id}` - Update roadmap
- `DELETE /api/roadmaps/{id}` - Delete roadmap

### Progress Tracking
- `POST /api/progress` - Mark item complete
- `GET /api/progress` - Get user progress
- `PUT /api/progress/{id}` - Update progress item

### Market Intelligence
- `GET /api/market/salary?job={title}` - Get salary data
- `GET /api/market/demand?skill={skill}` - Get demand trends
- `GET /api/market/competition?job={title}` - Get competition level

## 5. React Flow Canvas Design

### Node Types

#### 1. Skill Node
```typescript
interface SkillNode {
  id: string;
  type: 'skill';
  data: {
    name: string;
    status: 'current' | 'learning' | 'planned';
    priority: 'high' | 'medium' | 'low';
    estimatedTime: number; // months
  };
  position: { x: number; y: number };
}
```

#### 2. Course Node
```typescript
interface CourseNode {
  id: string;
  type: 'course';
  data: {
    name: string;
    provider: string;
    url: string;
    duration: string;
    cost: number;
    status: 'not_started' | 'in_progress' | 'completed';
  };
  position: { x: number; y: number };
}
```

#### 3. Project Node
```typescript
interface ProjectNode {
  id: string;
  type: 'project';
  data: {
    name: string;
    description: string;
    skills: string[];
    estimatedTime: number; // weeks
    status: 'not_started' | 'in_progress' | 'completed';
  };
  position: { x: number; y: number };
}
```

#### 4. Milestone Node
```typescript
interface MilestoneNode {
  id: string;
  type: 'milestone';
  data: {
    name: string;
    targetDate: string;
    requirements: string[];
    achieved: boolean;
  };
  position: { x: number; y: number };
}
```

## 6. Frontend Components

### Key React Components

#### 1. RoadmapCanvas
- React Flow canvas
- Drag-and-drop nodes
- Zoom and pan controls
- Node editing

#### 2. SkillGapAnalysis
- Current vs required skills
- Gap visualization
- Priority indicators

#### 3. LearningPathPanel
- Course recommendations
- Project ideas
- Certification paths

#### 4. ProgressTracker
- Completed items
- Time tracking
- Achievement badges

#### 5. MarketInsights
- Salary charts
- Demand trends
- Competition analysis

## 7. Cost Estimation

### Monthly Costs (50 roadmaps/month)

| Service | Usage | Cost |
|---------|-------|------|
| Cognito | 1 user | $0 |
| ECS Fargate | 1 task (0.25 vCPU, 0.5 GB) | $3.50 |
| Bedrock (Claude Opus 4.5) | 300K tokens | $9.00 |
| DynamoDB | On-demand | $1.00 |
| S3 | 5GB storage | $0.12 |
| CloudFront | 1K requests | $0.01 |
| **Total** | | **~$13.63/month** |

## 8. Performance Targets

- Resume analysis: < 10 seconds
- Gap analysis: < 5 seconds
- Roadmap generation: < 15 seconds
- Canvas rendering: < 1 second
- Frontend load time: < 2 seconds

## 9. Testing Strategy

### Unit Tests
- Agent logic
- React components
- Utility functions

### Integration Tests
- LangGraph workflow
- API endpoints
- Database operations

### E2E Tests
- Complete roadmap generation
- Progress tracking
- Export functionality

## 10. Deployment Strategy

### Backend (ECS Fargate)
```yaml
Task Definition:
  CPU: 256 (0.25 vCPU)
  Memory: 512 MB
  Container:
    Image: career-path-backend:latest
    Port: 8000
    Environment:
      - AWS_REGION
      - BEDROCK_MODEL_ID
      - DYNAMODB_TABLE
```

### Frontend (Vercel or CloudFront)
- Next.js static export
- CloudFront distribution
- S3 bucket for assets

## 11. Monitoring & Observability

### CloudWatch Metrics
- ECS task CPU/memory
- API request count
- LangGraph execution time
- Error rates

### CloudWatch Logs
- FastAPI application logs
- LangGraph agent logs
- Frontend error logs

### Alarms
- High error rate (> 5%)
- High latency (> 10s)
- ECS task failures
- Bedrock throttling

## 12. Future Enhancements

### Phase 2
- Collaborative roadmaps
- Mentor matching
- Community project sharing
- Integration with LinkedIn

### Phase 3
- AI career coach chatbot
- Automated progress tracking
- Skill assessment tests
- Job application tracking

---

**Status**: Planning  
**Last Updated**: February 19, 2026  
**Next Review**: March 1, 2026
