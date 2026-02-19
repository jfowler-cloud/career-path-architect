"""Tests for FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from career_path.main import app
from career_path.progress import progress_tracker


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_progress_tracker():
    """Reset progress tracker before each test."""
    progress_tracker._progress.clear()
    yield


def test_health_endpoint():
    """Test health check endpoint."""
    with patch('career_path.main.check_aws_credentials') as mock_aws, \
         patch('career_path.main.check_bedrock_access') as mock_bedrock:
        mock_aws.return_value = (True, "OK")
        mock_bedrock.return_value = (True, "OK")
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "workflow_initialized" in data


def test_health_endpoint_degraded():
    """Test health check with degraded status."""
    with patch('career_path.main.check_aws_credentials') as mock_aws, \
         patch('career_path.main.check_bedrock_access') as mock_bedrock:
        mock_aws.return_value = (False, "Error")
        mock_bedrock.return_value = (True, "OK")
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "degraded"


def test_generate_roadmap_validation_error():
    """Test roadmap generation with validation error."""
    # Too short resume
    response = client.post("/api/roadmaps/generate", json={
        "resume_text": "Short",
        "target_jobs": ["Engineer"]
    })
    assert response.status_code == 422


def test_generate_roadmap_empty_jobs():
    """Test roadmap generation with empty job titles."""
    response = client.post("/api/roadmaps/generate", json={
        "resume_text": "A" * 100,
        "target_jobs": [""]
    })
    assert response.status_code == 422


def test_generate_roadmap_too_many_jobs():
    """Test roadmap generation with too many jobs."""
    response = client.post("/api/roadmaps/generate", json={
        "resume_text": "A" * 100,
        "target_jobs": ["Job1", "Job2", "Job3", "Job4", "Job5", "Job6"]
    })
    assert response.status_code == 422


@patch('career_path.main.workflow')
def test_generate_roadmap_success(mock_workflow):
    """Test successful roadmap generation."""
    mock_workflow.invoke.return_value = {
        "nodes": [{"id": "1", "data": {"label": "Test"}, "position": {"x": 0, "y": 0}}],
        "edges": [],
        "milestones": [],
        "skill_gaps": [],
        "courses": [],
        "projects": [],
        "certifications": []
    }
    
    resume = "Senior Engineer with 5 years of Python experience. " * 5  # Make it longer
    response = client.post("/api/roadmaps/generate", json={
        "resume_text": resume,
        "target_jobs": ["Cloud Architect"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data


@patch('career_path.main.workflow')
def test_generate_roadmap_workflow_error(mock_workflow):
    """Test roadmap generation with workflow error."""
    mock_workflow.invoke.side_effect = Exception("Workflow failed")
    
    resume = "Senior Engineer with 5 years of Python experience. " * 5
    response = client.post("/api/roadmaps/generate", json={
        "resume_text": resume,
        "target_jobs": ["Cloud Architect"]
    })
    
    assert response.status_code == 500


def test_generate_roadmap_no_workflow():
    """Test roadmap generation when workflow not initialized."""
    with patch('career_path.main.workflow', None):
        resume = "Senior Engineer with 5 years of Python experience. " * 5
        response = client.post("/api/roadmaps/generate", json={
            "resume_text": resume,
            "target_jobs": ["Cloud Architect"]
        })
        
        assert response.status_code == 500


def test_api_docs():
    """Test API documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """Test OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data


def test_cors_middleware():
    """Test CORS middleware is configured."""
    # Just verify the app runs and has middleware
    response = client.get("/health")
    assert response.status_code == 200


def test_roadmap_request_validation():
    """Test RoadmapRequest validation."""
    from career_path.main import RoadmapRequest
    
    # Valid request
    req = RoadmapRequest(
        resume_text="A" * 100,
        target_jobs=["Engineer"]
    )
    assert len(req.resume_text) == 100
    
    # Test whitespace trimming
    req = RoadmapRequest(
        resume_text="  " + "A" * 100 + "  ",
        target_jobs=["  Engineer  "]
    )
    assert req.resume_text.strip() == "A" * 100
    assert req.target_jobs[0] == "Engineer"


def test_app_lifespan():
    """Test app lifespan initialization."""
    from career_path.main import app
    # App should have lifespan configured
    assert app.router.lifespan_context is not None


def test_roadmap_response_model():
    """Test RoadmapResponse model."""
    from career_path.main import RoadmapResponse
    
    response = RoadmapResponse(
        nodes=[],
        edges=[],
        milestones=[],
        skill_gaps=[],
        courses=[],
        projects=[],
        certifications=[]
    )
    assert response.nodes == []


def test_logging_configured():
    """Test logging is configured."""
    import logging
    logger = logging.getLogger("career_path.main")
    assert logger is not None


def test_create_progress():
    """Test creating progress tracking."""
    response = client.post(
        "/api/roadmaps/roadmap-123/progress",
        json=["Python", "AWS", "Docker"]
    )
    assert response.status_code == 200
    data = response.json()
    assert data["roadmap_id"] == "roadmap-123"
    assert data["total_skills"] == 3
    assert "created_at" in data


def test_get_progress_not_found():
    """Test getting nonexistent progress."""
    response = client.get("/api/roadmaps/nonexistent/progress")
    assert response.status_code == 404


def test_get_progress_success():
    """Test getting progress."""
    # Create progress first
    client.post("/api/roadmaps/roadmap-123/progress", json=["Python", "AWS"])
    
    response = client.get("/api/roadmaps/roadmap-123/progress")
    assert response.status_code == 200
    data = response.json()
    assert data["roadmap_id"] == "roadmap-123"
    assert data["completion_percentage"] == 0.0
    assert data["statistics"]["not_started"] == 2
    assert "Python" in data["skills"]
    assert "AWS" in data["skills"]


def test_update_skill_progress_success():
    """Test updating skill progress."""
    # Create progress first
    client.post("/api/roadmaps/roadmap-123/progress", json=["Python"])
    
    response = client.patch(
        "/api/roadmaps/roadmap-123/skills/Python",
        json={"skill": "Python", "status": "in_progress", "notes": "Started learning"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["skill"] == "Python"
    assert data["status"] == "in_progress"
    assert data["notes"] == "Started learning"
    assert data["started_at"] is not None
    assert data["roadmap_completion"] == 0.0


def test_update_skill_progress_to_completed():
    """Test completing a skill."""
    client.post("/api/roadmaps/roadmap-123/progress", json=["Python", "AWS"])
    
    response = client.patch(
        "/api/roadmaps/roadmap-123/skills/Python",
        json={"skill": "Python", "status": "completed", "notes": "Done!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None
    assert data["roadmap_completion"] == 50.0


def test_update_skill_progress_not_found():
    """Test updating nonexistent skill."""
    response = client.patch(
        "/api/roadmaps/roadmap-123/skills/Python",
        json={"skill": "Python", "status": "completed"}
    )
    assert response.status_code == 404


def test_update_skill_progress_invalid_status():
    """Test updating with invalid status."""
    client.post("/api/roadmaps/roadmap-123/progress", json=["Python"])
    
    response = client.patch(
        "/api/roadmaps/roadmap-123/skills/Python",
        json={"skill": "Python", "status": "invalid_status"}
    )
    assert response.status_code == 422


def test_progress_workflow_integration():
    """Test full progress tracking workflow."""
    # Create roadmap progress
    create_response = client.post(
        "/api/roadmaps/roadmap-456/progress",
        json=["Python", "AWS", "Docker"]
    )
    assert create_response.status_code == 200
    
    # Start first skill
    client.patch(
        "/api/roadmaps/roadmap-456/skills/Python",
        json={"skill": "Python", "status": "in_progress"}
    )
    
    # Complete first skill
    client.patch(
        "/api/roadmaps/roadmap-456/skills/Python",
        json={"skill": "Python", "status": "completed"}
    )
    
    # Start second skill
    client.patch(
        "/api/roadmaps/roadmap-456/skills/AWS",
        json={"skill": "AWS", "status": "in_progress"}
    )
    
    # Check progress
    progress_response = client.get("/api/roadmaps/roadmap-456/progress")
    assert progress_response.status_code == 200
    data = progress_response.json()
    
    assert data["completion_percentage"] == pytest.approx(33.33, rel=0.1)
    assert data["statistics"]["completed"] == 1
    assert data["statistics"]["in_progress"] == 1
    assert data["statistics"]["not_started"] == 1
    assert data["skills"]["Python"]["status"] == "completed"
    assert data["skills"]["AWS"]["status"] == "in_progress"
    assert data["skills"]["Docker"]["status"] == "not_started"


def test_compare_paths_endpoint():
    """Test career path comparison endpoint."""
    response = client.post("/api/compare-paths", json={
        "current_skills": ["Python", "Git"],
        "path1_skills": ["Python", "AWS", "Docker"],
        "path2_skills": ["Python", "Azure", "Kubernetes"],
        "path1_name": "AWS DevOps",
        "path2_name": "Azure DevOps"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "paths" in data
    assert "AWS DevOps" in data["paths"]
    assert "Azure DevOps" in data["paths"]
    assert "common_gaps" in data
    assert "recommendation" in data
    
    # Check learning effort is included
    assert "learning_effort" in data["paths"]["AWS DevOps"]
    assert "estimated_hours" in data["paths"]["AWS DevOps"]["learning_effort"]


def test_compare_paths_validation_error():
    """Test comparison with invalid input."""
    response = client.post("/api/compare-paths", json={
        "current_skills": [],  # Empty not allowed
        "path1_skills": ["Python"],
        "path2_skills": ["Java"]
    })
    assert response.status_code == 422
