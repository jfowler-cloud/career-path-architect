#!/usr/bin/env python3
"""Simple test script for Career Path Architect API."""

import json
import os
import sys

import boto3

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from career_path.graph.workflow import create_workflow

EXAMPLE_RESUME = """Senior Software Engineer with 5 years of experience.

Skills: Python, JavaScript, React, AWS (EC2, S3, Lambda), Docker

Experience:
- Built web applications serving 100K+ users
- Implemented CI/CD pipelines
- Led team of 3 developers
"""

def test_workflow():
    """Test the LangGraph workflow."""
    
    print("🧪 Testing Career Path Architect Workflow\n")
    
    # Check AWS credentials
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        print(f"✅ AWS Identity: {identity['Arn']}\n")
    except Exception as e:
        print(f"❌ AWS credentials not configured: {e}\n")
        return False
    
    # Create workflow
    print("📦 Creating workflow...")
    try:
        workflow = create_workflow()
        print("✅ Workflow created\n")
    except Exception as e:
        print(f"❌ Failed to create workflow: {e}\n")
        return False
    
    # Test workflow
    print("🚀 Running workflow...")
    initial_state = {
        "messages": [],
        "resume_text": EXAMPLE_RESUME,
        "target_jobs": ["Senior Cloud Architect"],
        "user_id": "test",
        "current_skills": [],
        "experience_years": {},
        "strengths": [],
        "required_skills": {},
        "nice_to_have_skills": {},
        "skill_gaps": [],
        "estimated_time": {},
        "courses": [],
        "projects": [],
        "certifications": [],
        "nodes": [],
        "edges": [],
        "milestones": [],
        "workflow_status": "started",
        "error": None
    }
    
    try:
        result = workflow.invoke(initial_state)
        
        print("✅ Workflow completed!\n")
        print(f"📊 Results:")
        print(f"  - Skills found: {len(result['current_skills'])}")
        print(f"  - Skill gaps: {len(result['skill_gaps'])}")
        print(f"  - Courses: {len(result['courses'])}")
        print(f"  - Projects: {len(result['projects'])}")
        print(f"  - Nodes: {len(result['nodes'])}")
        print(f"  - Edges: {len(result['edges'])}")
        
        if result['skill_gaps']:
            print(f"\n🎯 Top 3 Skill Gaps:")
            for gap in result['skill_gaps'][:3]:
                print(f"  - {gap['skill']} ({gap['priority']} priority)")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_workflow()
    sys.exit(0 if success else 1)
