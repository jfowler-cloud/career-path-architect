"""Tests for career path comparison."""

import pytest
from career_path.comparison import compare_career_paths, calculate_learning_effort


def test_compare_career_paths_basic():
    """Test basic career path comparison."""
    current = ["Python", "Git"]
    path1 = ["Python", "AWS", "Docker"]
    path2 = ["Python", "Azure", "Kubernetes"]
    
    result = compare_career_paths(current, path1, path2, "AWS Path", "Azure Path")
    
    assert result["paths"]["AWS Path"]["missing_skills"] == 2
    assert result["paths"]["Azure Path"]["missing_skills"] == 2
    assert result["paths"]["AWS Path"]["current_skills"] == 1
    assert result["recommendation"]["easier_path"] == "Equal difficulty"


def test_compare_career_paths_one_easier():
    """Test comparison where one path is easier."""
    current = ["Python", "Git", "Docker"]
    path1 = ["Python", "Docker", "AWS"]  # 1 gap
    path2 = ["Python", "Azure", "Kubernetes", "Terraform"]  # 3 gaps
    
    result = compare_career_paths(current, path1, path2, "Path A", "Path B")
    
    assert result["paths"]["Path A"]["missing_skills"] == 1
    assert result["paths"]["Path B"]["missing_skills"] == 3
    assert result["recommendation"]["easier_path"] == "Path A"
    assert result["recommendation"]["gap_difference"] == 2


def test_compare_career_paths_readiness_percentage():
    """Test readiness percentage calculation."""
    current = ["Python", "Git"]
    path1 = ["Python", "Git", "AWS", "Docker"]  # 50% ready
    path2 = ["Python"]  # 100% ready
    
    result = compare_career_paths(current, path1, path2)
    
    assert result["paths"]["Path 1"]["readiness_percentage"] == 50.0
    assert result["paths"]["Path 2"]["readiness_percentage"] == 100.0


def test_compare_career_paths_common_gaps():
    """Test identification of common skill gaps."""
    current = ["Python"]
    path1 = ["Python", "AWS", "Docker", "Kubernetes"]
    path2 = ["Python", "Azure", "Docker", "Kubernetes"]
    
    result = compare_career_paths(current, path1, path2)
    
    assert "docker" in result["common_gaps"]
    assert "kubernetes" in result["common_gaps"]
    assert len(result["common_gaps"]) == 2


def test_compare_career_paths_unique_gaps():
    """Test identification of unique skill gaps."""
    current = ["Python"]
    path1 = ["Python", "AWS", "Docker"]
    path2 = ["Python", "Azure", "Kubernetes"]
    
    result = compare_career_paths(current, path1, path2)
    
    assert "aws" in result["paths"]["Path 1"]["unique_gaps"]
    assert "azure" in result["paths"]["Path 2"]["unique_gaps"]


def test_compare_career_paths_case_insensitive():
    """Test case-insensitive comparison."""
    current = ["PYTHON", "git"]
    path1 = ["Python", "AWS"]
    path2 = ["python", "Azure"]
    
    result = compare_career_paths(current, path1, path2)
    
    assert result["paths"]["Path 1"]["current_skills"] == 1
    assert result["paths"]["Path 2"]["current_skills"] == 1


def test_compare_career_paths_empty_current():
    """Test comparison with no current skills."""
    current = []
    path1 = ["Python", "AWS"]
    path2 = ["Java", "GCP"]
    
    result = compare_career_paths(current, path1, path2)
    
    assert result["paths"]["Path 1"]["readiness_percentage"] == 0.0
    assert result["paths"]["Path 2"]["readiness_percentage"] == 0.0
    assert result["paths"]["Path 1"]["missing_skills"] == 2
    assert result["paths"]["Path 2"]["missing_skills"] == 2


def test_compare_career_paths_should_learn_first():
    """Test recommendation of skills to learn first."""
    current = ["Python"]
    path1 = ["Python", "AWS", "Docker", "Kubernetes", "Terraform", "Ansible"]
    path2 = ["Python", "Azure", "Docker", "Kubernetes", "Terraform", "Jenkins"]
    
    result = compare_career_paths(current, path1, path2)
    
    # Should recommend common gaps first (max 5)
    assert len(result["recommendation"]["should_learn_first"]) <= 5
    assert "docker" in result["recommendation"]["should_learn_first"]
    assert "kubernetes" in result["recommendation"]["should_learn_first"]


def test_calculate_learning_effort_default():
    """Test learning effort calculation with defaults."""
    skills = ["Python", "AWS", "Docker"]
    
    result = calculate_learning_effort(skills)
    
    assert result["total_skills"] == 3
    assert result["estimated_hours"] == 180  # 3 * 60 (medium)
    assert result["estimated_weeks"] == 6
    assert result["difficulty_breakdown"]["medium"] == 3


def test_calculate_learning_effort_with_difficulty():
    """Test learning effort with custom difficulty."""
    skills = ["Python", "AWS", "Docker"]
    difficulty = {
        "python": "easy",
        "aws": "hard",
        "docker": "medium"
    }
    
    result = calculate_learning_effort(skills, difficulty)
    
    assert result["estimated_hours"] == 200  # 20 + 120 + 60
    assert result["estimated_weeks"] == 12  # max of all
    assert result["difficulty_breakdown"]["easy"] == 1
    assert result["difficulty_breakdown"]["medium"] == 1
    assert result["difficulty_breakdown"]["hard"] == 1


def test_calculate_learning_effort_empty():
    """Test learning effort with no skills."""
    result = calculate_learning_effort([])
    
    assert result["total_skills"] == 0
    assert result["estimated_hours"] == 0
    assert result["average_hours_per_skill"] == 0


def test_calculate_learning_effort_average():
    """Test average hours per skill calculation."""
    skills = ["Skill1", "Skill2"]
    difficulty = {"skill1": "easy", "skill2": "hard"}
    
    result = calculate_learning_effort(skills, difficulty)
    
    assert result["average_hours_per_skill"] == 70.0  # (20 + 120) / 2


def test_compare_career_paths_whitespace_handling():
    """Test handling of whitespace in skill names."""
    current = ["  Python  ", "Git"]
    path1 = ["Python", "  AWS  "]
    path2 = ["Python  ", "Azure"]
    
    result = compare_career_paths(current, path1, path2)
    
    assert result["paths"]["Path 1"]["current_skills"] == 1
    assert result["paths"]["Path 2"]["current_skills"] == 1
