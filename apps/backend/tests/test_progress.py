"""Tests for progress tracking."""

import pytest
from datetime import datetime
from career_path.progress import ProgressTracker, SkillProgress, RoadmapProgress


@pytest.fixture
def tracker():
    """Create a fresh progress tracker."""
    return ProgressTracker()


def test_create_roadmap_progress(tracker):
    """Test creating progress for a roadmap."""
    skills = ["Python", "AWS", "Docker"]
    progress = tracker.create_roadmap_progress("roadmap-1", "user-1", skills)
    
    assert progress.roadmap_id == "roadmap-1"
    assert progress.user_id == "user-1"
    assert len(progress.skills) == 3
    assert all(skill in progress.skills for skill in skills)
    assert all(sp.status == "not_started" for sp in progress.skills.values())


def test_get_progress(tracker):
    """Test retrieving progress."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python"])
    
    progress = tracker.get_progress("roadmap-1")
    assert progress is not None
    assert progress.roadmap_id == "roadmap-1"
    
    missing = tracker.get_progress("nonexistent")
    assert missing is None


def test_update_skill_status_to_in_progress(tracker):
    """Test updating skill to in_progress."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python"])
    
    skill_progress = tracker.update_skill_status("roadmap-1", "Python", "in_progress", "Started course")
    
    assert skill_progress is not None
    assert skill_progress.status == "in_progress"
    assert skill_progress.notes == "Started course"
    assert skill_progress.started_at is not None
    assert skill_progress.completed_at is None


def test_update_skill_status_to_completed(tracker):
    """Test updating skill to completed."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python"])
    tracker.update_skill_status("roadmap-1", "Python", "in_progress")
    
    skill_progress = tracker.update_skill_status("roadmap-1", "Python", "completed", "Finished!")
    
    assert skill_progress.status == "completed"
    assert skill_progress.notes == "Finished!"
    assert skill_progress.completed_at is not None


def test_update_nonexistent_skill(tracker):
    """Test updating nonexistent skill."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python"])
    
    result = tracker.update_skill_status("roadmap-1", "Java", "completed")
    assert result is None


def test_update_nonexistent_roadmap(tracker):
    """Test updating skill in nonexistent roadmap."""
    result = tracker.update_skill_status("nonexistent", "Python", "completed")
    assert result is None


def test_get_completion_percentage_empty(tracker):
    """Test completion percentage with no progress."""
    completion = tracker.get_completion_percentage("nonexistent")
    assert completion == 0.0


def test_get_completion_percentage_partial(tracker):
    """Test completion percentage with partial progress."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python", "AWS", "Docker", "Kubernetes"])
    tracker.update_skill_status("roadmap-1", "Python", "completed")
    tracker.update_skill_status("roadmap-1", "AWS", "completed")
    
    completion = tracker.get_completion_percentage("roadmap-1")
    assert completion == 50.0


def test_get_completion_percentage_full(tracker):
    """Test completion percentage with all skills completed."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python", "AWS"])
    tracker.update_skill_status("roadmap-1", "Python", "completed")
    tracker.update_skill_status("roadmap-1", "AWS", "completed")
    
    completion = tracker.get_completion_percentage("roadmap-1")
    assert completion == 100.0


def test_get_statistics_empty(tracker):
    """Test statistics for nonexistent roadmap."""
    stats = tracker.get_statistics("nonexistent")
    assert stats == {"not_started": 0, "in_progress": 0, "completed": 0}


def test_get_statistics_mixed(tracker):
    """Test statistics with mixed progress."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python", "AWS", "Docker", "Kubernetes", "Terraform"])
    tracker.update_skill_status("roadmap-1", "Python", "completed")
    tracker.update_skill_status("roadmap-1", "AWS", "completed")
    tracker.update_skill_status("roadmap-1", "Docker", "in_progress")
    
    stats = tracker.get_statistics("roadmap-1")
    assert stats["completed"] == 2
    assert stats["in_progress"] == 1
    assert stats["not_started"] == 2


def test_skill_progress_timestamps(tracker):
    """Test that timestamps are set correctly."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python"])
    
    # Start skill
    tracker.update_skill_status("roadmap-1", "Python", "in_progress")
    progress = tracker.get_progress("roadmap-1")
    skill = progress.skills["Python"]
    
    assert skill.started_at is not None
    assert skill.completed_at is None
    started_time = skill.started_at
    
    # Complete skill
    tracker.update_skill_status("roadmap-1", "Python", "completed")
    progress = tracker.get_progress("roadmap-1")
    skill = progress.skills["Python"]
    
    assert skill.started_at == started_time  # Should not change
    assert skill.completed_at is not None
    assert skill.completed_at >= skill.started_at


def test_multiple_roadmaps(tracker):
    """Test tracking multiple roadmaps."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python"])
    tracker.create_roadmap_progress("roadmap-2", "user-2", ["Java"])
    
    progress1 = tracker.get_progress("roadmap-1")
    progress2 = tracker.get_progress("roadmap-2")
    
    assert progress1.roadmap_id == "roadmap-1"
    assert progress2.roadmap_id == "roadmap-2"
    assert "Python" in progress1.skills
    assert "Java" in progress2.skills


def test_updated_at_changes(tracker):
    """Test that updated_at changes on updates."""
    tracker.create_roadmap_progress("roadmap-1", "user-1", ["Python"])
    progress = tracker.get_progress("roadmap-1")
    initial_updated = progress.updated_at
    
    tracker.update_skill_status("roadmap-1", "Python", "in_progress")
    progress = tracker.get_progress("roadmap-1")
    
    assert progress.updated_at >= initial_updated
