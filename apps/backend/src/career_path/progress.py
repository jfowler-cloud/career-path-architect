"""Progress tracking for skill development."""

from datetime import datetime, UTC
from typing import Dict, List, Optional
from pydantic import BaseModel


class SkillProgress(BaseModel):
    """Progress for a single skill."""
    skill: str
    status: str = "not_started"  # not_started, in_progress, completed
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: str = ""


class RoadmapProgress(BaseModel):
    """Progress tracking for entire roadmap."""
    roadmap_id: str
    user_id: str
    skills: Dict[str, SkillProgress] = {}
    created_at: datetime
    updated_at: datetime


class ProgressTracker:
    """In-memory progress tracker (can be replaced with DynamoDB)."""
    
    def __init__(self):
        self._progress: Dict[str, RoadmapProgress] = {}
    
    def create_roadmap_progress(self, roadmap_id: str, user_id: str, skills: List[str]) -> RoadmapProgress:
        """Create progress tracking for a new roadmap."""
        now = datetime.now(UTC)
        progress = RoadmapProgress(
            roadmap_id=roadmap_id,
            user_id=user_id,
            skills={skill: SkillProgress(skill=skill) for skill in skills},
            created_at=now,
            updated_at=now,
        )
        self._progress[roadmap_id] = progress
        return progress
    
    def get_progress(self, roadmap_id: str) -> Optional[RoadmapProgress]:
        """Get progress for a roadmap."""
        return self._progress.get(roadmap_id)
    
    def update_skill_status(
        self,
        roadmap_id: str,
        skill: str,
        status: str,
        notes: str = "",
    ) -> Optional[SkillProgress]:
        """Update status of a skill."""
        progress = self._progress.get(roadmap_id)
        if not progress or skill not in progress.skills:
            return None
        
        skill_progress = progress.skills[skill]
        skill_progress.status = status
        skill_progress.notes = notes
        
        now = datetime.now(UTC)
        if status == "in_progress" and not skill_progress.started_at:
            skill_progress.started_at = now
        elif status == "completed" and not skill_progress.completed_at:
            skill_progress.completed_at = now
        
        progress.updated_at = now
        return skill_progress
    
    def get_completion_percentage(self, roadmap_id: str) -> float:
        """Calculate completion percentage."""
        progress = self._progress.get(roadmap_id)
        if not progress or not progress.skills:
            return 0.0
        
        completed = sum(1 for s in progress.skills.values() if s.status == "completed")
        return (completed / len(progress.skills)) * 100
    
    def get_statistics(self, roadmap_id: str) -> Dict[str, int]:
        """Get progress statistics."""
        progress = self._progress.get(roadmap_id)
        if not progress:
            return {"not_started": 0, "in_progress": 0, "completed": 0}
        
        stats = {"not_started": 0, "in_progress": 0, "completed": 0}
        for skill_progress in progress.skills.values():
            stats[skill_progress.status] += 1
        
        return stats


# Global progress tracker instance
progress_tracker = ProgressTracker()
