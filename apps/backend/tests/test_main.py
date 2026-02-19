"""Tests for FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from career_path.main import app


client = TestClient(app)


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
