"""Career path comparison utilities."""

from typing import List, Dict, Set


def compare_career_paths(
    current_skills: List[str],
    path1_skills: List[str],
    path2_skills: List[str],
    path1_name: str = "Path 1",
    path2_name: str = "Path 2"
) -> Dict:
    """Compare two career paths based on current skills.
    
    Args:
        current_skills: Skills the user currently has
        path1_skills: Required skills for first career path
        path2_skills: Required skills for second career path
        path1_name: Name of first career path
        path2_name: Name of second career path
    
    Returns:
        Comparison data including gaps, overlaps, and recommendations
    """
    current = {s.lower().strip() for s in current_skills}
    path1 = {s.lower().strip() for s in path1_skills}
    path2 = {s.lower().strip() for s in path2_skills}
    
    # Calculate gaps
    path1_gaps = path1 - current
    path2_gaps = path2 - current
    
    # Calculate overlaps
    path1_overlap = path1 & current
    path2_overlap = path2 & current
    
    # Skills needed for both paths
    common_gaps = path1_gaps & path2_gaps
    
    # Unique gaps
    path1_unique = path1_gaps - path2_gaps
    path2_unique = path2_gaps - path1_gaps
    
    # Calculate readiness scores
    path1_readiness = (len(path1_overlap) / len(path1) * 100) if path1 else 0
    path2_readiness = (len(path2_overlap) / len(path2) * 100) if path2 else 0
    
    # Determine easier path
    easier_path = path1_name if len(path1_gaps) < len(path2_gaps) else path2_name
    if len(path1_gaps) == len(path2_gaps):
        easier_path = "Equal difficulty"
    
    return {
        "paths": {
            path1_name: {
                "total_skills": len(path1),
                "current_skills": len(path1_overlap),
                "missing_skills": len(path1_gaps),
                "readiness_percentage": round(path1_readiness, 1),
                "gaps": sorted(list(path1_gaps)),
                "unique_gaps": sorted(list(path1_unique))
            },
            path2_name: {
                "total_skills": len(path2),
                "current_skills": len(path2_overlap),
                "missing_skills": len(path2_gaps),
                "readiness_percentage": round(path2_readiness, 1),
                "gaps": sorted(list(path2_gaps)),
                "unique_gaps": sorted(list(path2_unique))
            }
        },
        "common_gaps": sorted(list(common_gaps)),
        "recommendation": {
            "easier_path": easier_path,
            "gap_difference": abs(len(path1_gaps) - len(path2_gaps)),
            "should_learn_first": sorted(list(common_gaps))[:5] if common_gaps else []
        }
    }


def calculate_learning_effort(
    skill_gaps: List[str],
    difficulty_map: Dict[str, str] = None
) -> Dict:
    """Calculate estimated learning effort for skill gaps.
    
    Args:
        skill_gaps: List of skills to learn
        difficulty_map: Optional mapping of skills to difficulty levels
    
    Returns:
        Effort estimation with time and difficulty breakdown
    """
    if difficulty_map is None:
        difficulty_map = {}
    
    # Default difficulty levels
    default_difficulty = {
        "easy": {"hours": 20, "weeks": 2},
        "medium": {"hours": 60, "weeks": 6},
        "hard": {"hours": 120, "weeks": 12}
    }
    
    total_hours = 0
    total_weeks = 0
    breakdown = {"easy": 0, "medium": 0, "hard": 0}
    
    for skill in skill_gaps:
        difficulty = difficulty_map.get(skill.lower(), "medium")
        effort = default_difficulty.get(difficulty, default_difficulty["medium"])
        
        total_hours += effort["hours"]
        total_weeks = max(total_weeks, effort["weeks"])
        breakdown[difficulty] += 1
    
    return {
        "total_skills": len(skill_gaps),
        "estimated_hours": total_hours,
        "estimated_weeks": total_weeks,
        "difficulty_breakdown": breakdown,
        "average_hours_per_skill": round(total_hours / len(skill_gaps), 1) if skill_gaps else 0
    }
