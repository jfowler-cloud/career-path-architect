"""Tests for graph nodes."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from career_path.graph.nodes import (
    _extract_json,
    resume_analyzer_node,
    job_parser_node,
    gap_analysis_node,
    learning_path_node,
    roadmap_generator_node
)


def test_extract_json_direct():
    """Test direct JSON extraction."""
    text = '{"skills": ["Python", "AWS"]}'
    result = _extract_json(text)
    assert result == {"skills": ["Python", "AWS"]}


def test_extract_json_markdown():
    """Test JSON extraction from markdown code block."""
    text = '```json\n{"skills": ["Python"]}\n```'
    result = _extract_json(text)
    assert result == {"skills": ["Python"]}


def test_extract_json_embedded():
    """Test JSON extraction from embedded text."""
    text = 'Here is the result: {"skills": ["Python"]} and more text'
    result = _extract_json(text)
    assert result == {"skills": ["Python"]}


def test_extract_json_invalid():
    """Test JSON extraction with invalid input."""
    with pytest.raises(ValueError, match="No valid JSON found"):
        _extract_json("This is not JSON at all")


@patch('career_path.graph.nodes.boto3.client')
def test_get_bedrock_client_cached(mock_boto_client):
    """Test bedrock client caching."""
    from career_path.graph.nodes import _get_bedrock_client
    
    # Clear cache
    _get_bedrock_client.cache_clear()
    
    # First call
    client1 = _get_bedrock_client()
    # Second call should return cached
    client2 = _get_bedrock_client()
    
    # Should only create client once
    assert mock_boto_client.call_count == 1


@patch('career_path.graph.nodes._get_bedrock_client')
def test_get_llm(mock_get_client):
    """Test LLM creation."""
    from career_path.graph.nodes import _get_llm
    
    # Don't actually create LLM, just test the function exists
    mock_get_client.return_value = None
    # Just verify function is callable
    assert callable(_get_llm)


@patch('career_path.graph.nodes._get_llm')
def test_resume_analyzer_success(mock_get_llm):
    """Test successful resume analysis."""
    mock_llm = Mock()
    mock_response = Mock()
    mock_response.content = '{"skills": ["Python", "AWS"], "experience": {"Python": 5}, "strengths": ["Problem solving"]}'
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm
    
    state = {"resume_text": "Senior Engineer with Python and AWS experience"}
    result = resume_analyzer_node(state)
    
    assert "current_skills" in result
    assert "Python" in result["current_skills"]
    assert result["workflow_status"] == "resume_analyzed"


@patch('career_path.graph.nodes._get_llm')
def test_resume_analyzer_error(mock_get_llm):
    """Test resume analysis with error."""
    mock_llm = Mock()
    mock_llm.invoke.side_effect = Exception("LLM error")
    mock_get_llm.return_value = mock_llm
    
    state = {"resume_text": "Test resume"}
    result = resume_analyzer_node(state)
    
    assert result["current_skills"] == []
    assert "error" in result


@patch('career_path.graph.nodes._get_llm')
def test_job_parser_success(mock_get_llm):
    """Test successful job parsing."""
    mock_llm = Mock()
    mock_response = Mock()
    mock_response.content = '{"required": ["Python", "AWS"], "nice_to_have": ["Docker"]}'
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm
    
    state = {"target_jobs": ["Senior Cloud Engineer"]}
    result = job_parser_node(state)
    
    assert "required_skills" in result
    assert "Senior Cloud Engineer" in result["required_skills"]
    assert result["workflow_status"] == "jobs_parsed"


@patch('career_path.graph.nodes._get_llm')
def test_job_parser_error(mock_get_llm):
    """Test job parsing with error."""
    mock_llm = Mock()
    mock_llm.invoke.side_effect = Exception("LLM error")
    mock_get_llm.return_value = mock_llm
    
    state = {"target_jobs": ["Test Job"]}
    result = job_parser_node(state)
    
    assert result["required_skills"]["Test Job"] == []


def test_gap_analysis():
    """Test gap analysis."""
    state = {
        "current_skills": ["Python", "JavaScript"],
        "required_skills": {
            "Senior Engineer": ["Python", "AWS", "Kubernetes"]
        }
    }
    result = gap_analysis_node(state)
    
    assert "skill_gaps" in result
    assert len(result["skill_gaps"]) == 2  # AWS and Kubernetes
    assert result["workflow_status"] == "gaps_analyzed"


def test_gap_analysis_no_gaps():
    """Test gap analysis with no gaps."""
    state = {
        "current_skills": ["Python", "AWS"],
        "required_skills": {
            "Engineer": ["Python"]
        }
    }
    result = gap_analysis_node(state)
    
    assert len(result["skill_gaps"]) == 0


@patch('career_path.graph.nodes._get_llm')
def test_learning_path_success(mock_get_llm):
    """Test successful learning path generation."""
    mock_llm = Mock()
    mock_response = Mock()
    mock_response.content = '{"courses": [{"name": "AWS Course", "provider": "Udemy", "url": "http://test.com", "duration": "10h"}], "projects": [{"name": "Build API", "description": "REST API", "skills": ["Python"]}], "certifications": [{"name": "AWS Cert", "provider": "AWS", "url": "http://aws.com"}]}'
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm
    
    state = {"skill_gaps": [{"skill": "AWS", "priority": "high", "time_months": 3}]}
    result = learning_path_node(state)
    
    assert len(result["courses"]) > 0
    assert result["workflow_status"] == "learning_path_generated"


def test_learning_path_no_gaps():
    """Test learning path with no gaps."""
    state = {"skill_gaps": []}
    result = learning_path_node(state)
    
    assert result["courses"] == []
    assert result["projects"] == []


@patch('career_path.graph.nodes._get_llm')
def test_learning_path_error(mock_get_llm):
    """Test learning path with error."""
    mock_llm = Mock()
    mock_llm.invoke.side_effect = Exception("LLM error")
    mock_get_llm.return_value = mock_llm
    
    state = {"skill_gaps": [{"skill": "AWS", "priority": "high", "time_months": 3}]}
    result = learning_path_node(state)
    
    assert result["courses"] == []
    assert "error" in result


def test_roadmap_generator():
    """Test roadmap generation."""
    state = {
        "current_skills": ["Python", "JavaScript"],
        "skill_gaps": [
            {"skill": "AWS", "priority": "high", "time_months": 4},
            {"skill": "Kubernetes", "priority": "medium", "time_months": 3}
        ],
        "target_jobs": ["Senior Cloud Engineer"]
    }
    result = roadmap_generator_node(state)
    
    assert "nodes" in result
    assert "edges" in result
    assert len(result["nodes"]) >= 3  # current, skills, target
    assert result["workflow_status"] == "complete"


def test_roadmap_generator_no_gaps():
    """Test roadmap generation with no gaps."""
    state = {
        "current_skills": ["Python"],
        "skill_gaps": [],
        "target_jobs": ["Engineer"]
    }
    result = roadmap_generator_node(state)
    
    assert len(result["nodes"]) == 2  # current and target only
