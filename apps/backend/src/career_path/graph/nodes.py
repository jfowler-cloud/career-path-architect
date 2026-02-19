"""Agent node implementations for career path workflow."""

import json
from typing import Any

import boto3
from langchain_aws import ChatBedrock

from ..graph.state import CareerPathState

bedrock = boto3.client("bedrock-runtime")


def resume_analyzer_node(state: CareerPathState) -> dict[str, Any]:
    """Extract skills and experience from resume."""
    
    llm = ChatBedrock(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        client=bedrock,
    )
    
    prompt = f"""Analyze this resume and extract:
1. Technical skills (programming languages, frameworks, tools, cloud services)
2. Years of experience per skill category
3. Key strengths and achievements

Resume:
{state['resume_text']}

Return ONLY valid JSON in this exact format:
{{
  "skills": ["skill1", "skill2"],
  "experience": {{"category": years}},
  "strengths": ["strength1", "strength2"]
}}"""
    
    response = llm.invoke(prompt)
    result = json.loads(response.content)
    
    return {
        "current_skills": result["skills"],
        "experience_years": result["experience"],
        "strengths": result["strengths"],
        "workflow_status": "resume_analyzed"
    }


def job_parser_node(state: CareerPathState) -> dict[str, Any]:
    """Parse job descriptions and extract requirements."""
    
    llm = ChatBedrock(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        client=bedrock,
    )
    
    required_skills = {}
    nice_to_have = {}
    
    for job_title in state["target_jobs"]:
        prompt = f"""For the role "{job_title}", list:
1. Required technical skills
2. Nice-to-have skills

Return ONLY valid JSON:
{{
  "required": ["skill1", "skill2"],
  "nice_to_have": ["skill3", "skill4"]
}}"""
        
        response = llm.invoke(prompt)
        result = json.loads(response.content)
        
        required_skills[job_title] = result["required"]
        nice_to_have[job_title] = result["nice_to_have"]
    
    return {
        "required_skills": required_skills,
        "nice_to_have_skills": nice_to_have,
        "workflow_status": "jobs_parsed"
    }


def gap_analysis_node(state: CareerPathState) -> dict[str, Any]:
    """Identify and prioritize skill gaps."""
    
    current = set(state["current_skills"])
    gaps = []
    
    for job_title, required in state["required_skills"].items():
        missing = set(required) - current
        for skill in missing:
            gaps.append({
                "skill": skill,
                "for_job": job_title,
                "priority": "high",
                "difficulty": "medium",
                "time_months": 3
            })
    
    # Sort by priority
    gaps.sort(key=lambda x: x["priority"], reverse=True)
    
    return {
        "skill_gaps": gaps,
        "workflow_status": "gaps_analyzed"
    }


def learning_path_node(state: CareerPathState) -> dict[str, Any]:
    """Generate learning recommendations."""
    
    llm = ChatBedrock(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        client=bedrock,
    )
    
    skills_needed = [gap["skill"] for gap in state["skill_gaps"][:5]]
    
    prompt = f"""For these skills: {', '.join(skills_needed)}

Recommend:
1. Online courses (with provider and URL)
2. Hands-on project ideas
3. Relevant certifications

Return ONLY valid JSON:
{{
  "courses": [{{"name": "...", "provider": "...", "url": "...", "duration": "..."}}],
  "projects": [{{"name": "...", "description": "...", "skills": ["..."]}}],
  "certifications": [{{"name": "...", "provider": "...", "url": "..."}}]
}}"""
    
    response = llm.invoke(prompt)
    result = json.loads(response.content)
    
    return {
        "courses": result["courses"],
        "projects": result["projects"],
        "certifications": result["certifications"],
        "workflow_status": "learning_path_generated"
    }


def roadmap_generator_node(state: CareerPathState) -> dict[str, Any]:
    """Generate visual roadmap nodes and edges."""
    
    nodes = []
    edges = []
    
    # Current state node
    nodes.append({
        "id": "current",
        "type": "milestone",
        "data": {"label": "Current State", "skills": state["current_skills"]},
        "position": {"x": 100, "y": 100}
    })
    
    # Skill gap nodes
    y_offset = 200
    for i, gap in enumerate(state["skill_gaps"][:5]):
        node_id = f"skill-{i}"
        nodes.append({
            "id": node_id,
            "type": "skill",
            "data": {
                "label": gap["skill"],
                "priority": gap["priority"],
                "time": gap["time_months"]
            },
            "position": {"x": 100 + (i * 150), "y": y_offset}
        })
        edges.append({"id": f"e-current-{node_id}", "source": "current", "target": node_id})
    
    # Target job node
    nodes.append({
        "id": "target",
        "type": "milestone",
        "data": {"label": state["target_jobs"][0], "achieved": False},
        "position": {"x": 400, "y": 400}
    })
    
    return {
        "nodes": nodes,
        "edges": edges,
        "milestones": [
            {"name": "Complete foundational courses", "target_date": "3 months"},
            {"name": "Build portfolio projects", "target_date": "6 months"},
            {"name": "Obtain certifications", "target_date": "9 months"}
        ],
        "workflow_status": "complete"
    }
