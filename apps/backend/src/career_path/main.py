"""FastAPI application."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .graph.workflow import create_workflow


# Global workflow instance
workflow = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize workflow on startup."""
    global workflow
    workflow = create_workflow()
    yield


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
    resume_text: str
    target_jobs: list[str]
    user_id: str = "default"


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
    return {"status": "healthy"}


@app.post("/api/roadmaps/generate", response_model=RoadmapResponse)
async def generate_roadmap(request: RoadmapRequest):
    """Generate career roadmap."""
    
    if not workflow:
        raise HTTPException(status_code=500, detail="Workflow not initialized")
    
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
        raise HTTPException(status_code=500, detail=str(e))
