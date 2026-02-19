"""FastAPI application."""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from .graph.workflow import create_workflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Global workflow instance
workflow = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize workflow on startup."""
    global workflow
    logger.info("Initializing LangGraph workflow")
    workflow = create_workflow()
    logger.info("Workflow initialized successfully")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="Career Path Architect API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RoadmapRequest(BaseModel):
    resume_text: str = Field(..., min_length=50, max_length=10000)
    target_jobs: list[str] = Field(..., min_length=1, max_length=5)
    user_id: str = "default"
    
    @field_validator('target_jobs')
    @classmethod
    def validate_jobs(cls, v):
        if not all(len(job.strip()) > 0 for job in v):
            raise ValueError("Job titles cannot be empty")
        return [job.strip() for job in v]


class RoadmapResponse(BaseModel):
    nodes: list[dict]
    edges: list[dict]
    milestones: list[dict]
    skill_gaps: list[dict]
    courses: list[dict]
    projects: list[dict]
    certifications: list[dict]


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "workflow_initialized": workflow is not None
    }


@app.post("/api/roadmaps/generate", response_model=RoadmapResponse)
async def generate_roadmap(request: RoadmapRequest):
    """Generate career roadmap."""
    
    if not workflow:
        logger.error("Workflow not initialized")
        raise HTTPException(status_code=500, detail="Workflow not initialized")
    
    logger.info(f"Generating roadmap for {len(request.target_jobs)} jobs")
    
    try:
        initial_state = {
            "messages": [],
            "resume_text": request.resume_text,
            "target_jobs": request.target_jobs,
            "user_id": request.user_id,
            "current_skills": [],
            "experience_years": {},
            "strengths": [],
            "required_skills": {},
            "nice_to_have_skills": {},
            "skill_gaps": [],
            "estimated_time": {},
            "courses": [],
            "projects": [],
            "certifications": [],
            "nodes": [],
            "edges": [],
            "milestones": [],
            "workflow_status": "started",
            "error": None
        }
        
        result = workflow.invoke(initial_state)
        
        logger.info(f"Roadmap generated successfully with {len(result['nodes'])} nodes")
        
        return RoadmapResponse(
            nodes=result["nodes"],
            edges=result["edges"],
            milestones=result["milestones"],
            skill_gaps=result["skill_gaps"],
            courses=result["courses"],
            projects=result["projects"],
            certifications=result["certifications"]
        )
        
    except Exception as e:
        logger.error(f"Roadmap generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
