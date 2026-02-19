"""Utility functions for career path workflow."""

from typing import Any


def deduplicate_skills(skills: list[str]) -> list[str]:
    """Remove duplicate skills (case-insensitive)."""
    seen = set()
    result = []
    for skill in skills:
        skill_lower = skill.lower().strip()
        if skill_lower and skill_lower not in seen:
            seen.add(skill_lower)
            result.append(skill.strip())
    return result


def calculate_priority(gap_count: int, total_gaps: int) -> str:
    """Calculate priority based on gap position."""
    if gap_count <= 3:
        return "high"
    elif gap_count <= total_gaps // 2:
        return "medium"
    return "low"


def estimate_learning_time(skill: str) -> int:
    """Estimate learning time in months for a skill."""
    # Simple heuristic - can be improved with ML
    skill_lower = skill.lower()
    if any(x in skill_lower for x in ["aws", "azure", "gcp", "cloud"]):
        return 4
    elif any(x in skill_lower for x in ["kubernetes", "docker", "terraform"]):
        return 3
    elif any(x in skill_lower for x in ["python", "javascript", "java"]):
        return 6
    return 3
