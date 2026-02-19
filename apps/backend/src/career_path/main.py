"""FastAPI application."""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from .graph.workflow import create_workflow
from .health import check_aws_credentials, check_bedrock_access
from .progress import progress_tracker, SkillProgress
from .comparison import compare_career_paths, calculate_learning_effort
from .cache import response_cache

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
    resume_text: str = Field(..., min_length=50, max_length=10000, description="Resume text")
    target_jobs: list[str] = Field(..., min_length=1, max_length=5, description="Target job titles")
    user_id: str = Field(default="default", description="User identifier")
    
    @field_validator('target_jobs')
    @classmethod
    def validate_jobs(cls, v):
        if not all(len(job.strip()) > 0 for job in v):
            raise ValueError("Job titles cannot be empty")
        return [job.strip() for job in v]
    
    @field_validator('resume_text')
    @classmethod
    def validate_resume(cls, v):
        if len(v.strip()) < 50:
            raise ValueError("Resume must be at least 50 characters")
        return v.strip()


class RoadmapResponse(BaseModel):
    nodes: list[dict] = Field(..., description="React Flow nodes")
    edges: list[dict] = Field(..., description="React Flow edges")
    milestones: list[dict] = Field(..., description="Career milestones")
    skill_gaps: list[dict] = Field(..., description="Identified skill gaps")
    courses: list[dict] = Field(..., description="Recommended courses")
    projects: list[dict] = Field(..., description="Project ideas")
    certifications: list[dict] = Field(..., description="Certification recommendations")


@app.get("/health")
async def health():
    """Health check endpoint with AWS connectivity tests."""
    aws_ok, aws_msg = check_aws_credentials()
    bedrock_ok, bedrock_msg = check_bedrock_access()
    
    return {
        "status": "healthy" if (aws_ok and bedrock_ok) else "degraded",
        "workflow_initialized": workflow is not None,
        "aws_credentials": {"ok": aws_ok, "message": aws_msg},
        "bedrock_access": {"ok": bedrock_ok, "message": bedrock_msg},
        "cache_stats": response_cache.get_stats()
    }


@app.post("/api/cache/clear")
async def clear_cache():
    """Clear response cache."""
    response_cache.clear()
    return {"message": "Cache cleared", "stats": response_cache.get_stats()}


@app.post("/api/cache/cleanup")
async def cleanup_cache():
    """Remove expired cache entries."""
    removed = response_cache.cleanup_expired()
    return {
        "message": f"Removed {removed} expired entries",
        "removed": removed,
        "stats": response_cache.get_stats()
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


class UpdateSkillRequest(BaseModel):
    """Request to update skill progress."""
    skill: str = Field(..., min_length=1, description="Skill name")
    status: str = Field(..., pattern="^(not_started|in_progress|completed)$", description="Status")
    notes: str = Field(default="", description="Optional notes")


@app.post("/api/roadmaps/{roadmap_id}/progress")
async def create_progress(roadmap_id: str, skills: list[str]):
    """Initialize progress tracking for a roadmap."""
    progress = progress_tracker.create_roadmap_progress(
        roadmap_id=roadmap_id,
        user_id="default",  # TODO: Get from auth
        skills=skills
    )
    return {
        "roadmap_id": progress.roadmap_id,
        "created_at": progress.created_at.isoformat(),
        "total_skills": len(skills)
    }


@app.get("/api/roadmaps/{roadmap_id}/progress")
async def get_progress(roadmap_id: str):
    """Get progress for a roadmap."""
    progress = progress_tracker.get_progress(roadmap_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    stats = progress_tracker.get_statistics(roadmap_id)
    completion = progress_tracker.get_completion_percentage(roadmap_id)
    
    return {
        "roadmap_id": progress.roadmap_id,
        "completion_percentage": completion,
        "statistics": stats,
        "skills": {
            skill: {
                "status": sp.status,
                "started_at": sp.started_at.isoformat() if sp.started_at else None,
                "completed_at": sp.completed_at.isoformat() if sp.completed_at else None,
                "notes": sp.notes
            }
            for skill, sp in progress.skills.items()
        },
        "updated_at": progress.updated_at.isoformat()
    }


@app.patch("/api/roadmaps/{roadmap_id}/skills/{skill}")
async def update_skill_progress(roadmap_id: str, skill: str, request: UpdateSkillRequest):
    """Update progress for a specific skill."""
    skill_progress = progress_tracker.update_skill_status(
        roadmap_id=roadmap_id,
        skill=skill,
        status=request.status,
        notes=request.notes
    )
    
    if not skill_progress:
        raise HTTPException(status_code=404, detail="Skill or roadmap not found")
    
    completion = progress_tracker.get_completion_percentage(roadmap_id)
    
    return {
        "skill": skill_progress.skill,
        "status": skill_progress.status,
        "started_at": skill_progress.started_at.isoformat() if skill_progress.started_at else None,
        "completed_at": skill_progress.completed_at.isoformat() if skill_progress.completed_at else None,
        "notes": skill_progress.notes,
        "roadmap_completion": completion
    }


class ComparePathsRequest(BaseModel):
    """Request to compare career paths."""
    current_skills: list[str] = Field(..., min_length=1, description="Current skills")
    path1_skills: list[str] = Field(..., min_length=1, description="Skills for first path")
    path2_skills: list[str] = Field(..., min_length=1, description="Skills for second path")
    path1_name: str = Field(default="Path 1", description="Name of first path")
    path2_name: str = Field(default="Path 2", description="Name of second path")


@app.post("/api/compare-paths")
async def compare_paths(request: ComparePathsRequest):
    """Compare two career paths."""
    comparison = compare_career_paths(
        current_skills=request.current_skills,
        path1_skills=request.path1_skills,
        path2_skills=request.path2_skills,
        path1_name=request.path1_name,
        path2_name=request.path2_name
    )
    
    # Add learning effort estimates
    path1_effort = calculate_learning_effort(comparison["paths"][request.path1_name]["gaps"])
    path2_effort = calculate_learning_effort(comparison["paths"][request.path2_name]["gaps"])
    
    comparison["paths"][request.path1_name]["learning_effort"] = path1_effort
    comparison["paths"][request.path2_name]["learning_effort"] = path2_effort
    
    return comparison
