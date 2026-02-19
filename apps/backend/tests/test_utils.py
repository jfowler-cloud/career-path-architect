"""Tests for utility functions."""

import pytest
from career_path.utils import deduplicate_skills, calculate_priority, estimate_learning_time


def test_deduplicate_skills():
    """Test skill deduplication."""
    # Test basic deduplication
    skills = ["Python", "python", "PYTHON", "JavaScript"]
    result = deduplicate_skills(skills)
    assert len(result) == 2
    assert "Python" in result
    assert "JavaScript" in result
    
    # Test with whitespace
    skills = ["  Python  ", "Python", "Java  "]
    result = deduplicate_skills(skills)
    assert len(result) == 2
    
    # Test empty list
    assert deduplicate_skills([]) == []
    
    # Test with empty strings
    skills = ["Python", "", "  ", "Java"]
    result = deduplicate_skills(skills)
    assert len(result) == 2


def test_calculate_priority():
    """Test priority calculation."""
    # High priority (first 3)
    assert calculate_priority(1, 10) == "high"
    assert calculate_priority(2, 10) == "high"
    assert calculate_priority(3, 10) == "high"
    
    # Medium priority (middle)
    assert calculate_priority(4, 10) == "medium"
    assert calculate_priority(5, 10) == "medium"
    
    # Low priority (rest)
    assert calculate_priority(6, 10) == "low"
    assert calculate_priority(10, 10) == "low"


def test_estimate_learning_time():
    """Test learning time estimation."""
    # Cloud skills
    assert estimate_learning_time("AWS") == 4
    assert estimate_learning_time("Azure") == 4
    assert estimate_learning_time("GCP") == 4
    assert estimate_learning_time("Cloud Architecture") == 4
    
    # Container/IaC skills
    assert estimate_learning_time("Kubernetes") == 3
    assert estimate_learning_time("Docker") == 3
    assert estimate_learning_time("Terraform") == 3
    
    # Programming languages
    assert estimate_learning_time("Python") == 6
    assert estimate_learning_time("JavaScript") == 6
    assert estimate_learning_time("Java") == 6
    
    # Default
    assert estimate_learning_time("Unknown Skill") == 3
