from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class CareerPathState(TypedDict):
    """State for career path analysis workflow."""
    
    # Input
    messages: Annotated[list, add_messages]
    resume_text: str
    target_jobs: list[str]
    job_description: str | None
    specialty_info: str | None
    user_id: str
    
    # Resume Analysis
    current_skills: list[str]
    experience_years: dict[str, int]
    strengths: list[str]
    
    # Job Analysis
    required_skills: dict[str, list[str]]
    nice_to_have_skills: dict[str, list[str]]
    
    # Gap Analysis
    skill_gaps: list[dict]
    estimated_time: dict[str, int]
    fit_score: int
    matched_skills: list[str]
    
    # Learning Path
    courses: list[dict]
    projects: list[dict]
    certifications: list[dict]
    
    # Critical Review
    critical_review: dict
    
    # Roadmap
    nodes: list[dict]
    edges: list[dict]
    milestones: list[dict]
    
    # Metadata
    workflow_status: str
    error: str | None
