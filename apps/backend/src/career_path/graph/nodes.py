"""Agent node implementations for career path workflow."""

import json
import logging
import os
import re
from functools import lru_cache
from typing import Any

import boto3
from langchain_aws import ChatBedrock

from ..graph.state import CareerPathState
from ..constants import MODEL_ID, MAX_TOKENS, TEMPERATURE, MAX_RESUME_LENGTH, MAX_SKILL_GAPS
from ..utils import deduplicate_skills, calculate_priority, estimate_learning_time

logger = logging.getLogger(__name__)

# Cache bedrock client
_bedrock_client = None


@lru_cache(maxsize=1)
def _get_bedrock_client():
    """Lazy load and cache bedrock client."""
    global _bedrock_client
    if _bedrock_client is None:
        _bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
    return _bedrock_client


def _get_llm():
    """Get configured LLM instance."""
    return ChatBedrock(
        model_id=MODEL_ID,
        client=_get_bedrock_client(),
        model_kwargs={
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
        }
    )


def _extract_json(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown code blocks."""
    try:
        # Try direct parse first
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract from markdown code block
        match = re.search(r'```(?:json)?\s*(\{[^`]*\})\s*```', text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        # Try to find any JSON object
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError(f"No valid JSON found in response: {text[:200]}")


def resume_analyzer_node(state: CareerPathState) -> dict[str, Any]:
    """Extract skills and experience from resume."""
    
    logger.info("Starting resume analysis")
    
    prompt = f"""Extract from this resume:
1. Technical skills
2. Years of experience per category
3. Key strengths

Resume (first {MAX_RESUME_LENGTH} chars):
{state['resume_text'][:MAX_RESUME_LENGTH]}

Return JSON:
{{"skills": ["..."], "experience": {{"category": years}}, "strengths": ["..."]}}"""
    
    try:
        response = _get_llm().invoke(prompt)
        result = _extract_json(response.content)
        
        logger.info(f"Extracted {len(result.get('skills', []))} skills")
        
        skills = deduplicate_skills(result.get("skills", []))
        
        return {
            "current_skills": skills,
            "experience_years": result.get("experience", {}),
            "strengths": result.get("strengths", []),
            "workflow_status": "resume_analyzed"
        }
    except Exception as e:
        logger.error(f"Resume analysis failed: {e}")
        return {
            "current_skills": [],
            "experience_years": {},
            "strengths": [],
            "workflow_status": "resume_analyzed",
            "error": str(e)
        }


def job_parser_node(state: CareerPathState) -> dict[str, Any]:
    """Parse job descriptions and extract requirements."""
    
    logger.info(f"Parsing {len(state['target_jobs'])} target jobs")
    
    required_skills = {}
    nice_to_have = {}
    
    for job_title in state["target_jobs"]:
        # Use job description if provided, otherwise infer from title
        if state.get("job_description"):
            prompt = f"""Analyze this job posting for "{job_title}":

{state['job_description'][:2000]}

Extract required and nice-to-have technical skills.
{f"Focus on: {state['specialty_info']}" if state.get('specialty_info') else ""}

Return JSON:
{{"required": ["..."], "nice_to_have": ["..."]}}"""
        else:
            prompt = f"""For "{job_title}", list required and nice-to-have technical skills.
{f"Focus on: {state['specialty_info']}" if state.get('specialty_info') else ""}

Return JSON:
{{"required": ["..."], "nice_to_have": ["..."]}}"""
        
        try:
            response = _get_llm().invoke(prompt)
            result = _extract_json(response.content)
            
            required_skills[job_title] = result.get("required", [])
            nice_to_have[job_title] = result.get("nice_to_have", [])
        except Exception as e:
            logger.error(f"Job parsing failed for {job_title}: {e}")
            required_skills[job_title] = []
            nice_to_have[job_title] = []
    
    return {
        "required_skills": required_skills,
        "nice_to_have_skills": nice_to_have,
        "workflow_status": "jobs_parsed"
    }


def gap_analysis_node(state: CareerPathState) -> dict[str, Any]:
    """Identify and prioritize skill gaps."""
    
    logger.info("Analyzing skill gaps")
    
    current = set(s.lower() for s in state["current_skills"])
    gaps = []
    
    for job_title, required in state["required_skills"].items():
        missing = [s for s in required if s.lower() not in current]
        for idx, skill in enumerate(missing):
            priority = calculate_priority(idx + 1, len(missing))
            time_months = estimate_learning_time(skill)
            gaps.append({
                "skill": skill,
                "for_job": job_title,
                "priority": priority,
                "difficulty": "medium",
                "time_months": time_months
            })
    
    # Sort by priority then skill name
    gaps.sort(key=lambda x: (x["priority"] != "high", x["skill"]))
    
    logger.info(f"Found {len(gaps)} skill gaps")
    
    return {
        "skill_gaps": gaps,
        "workflow_status": "gaps_analyzed"
    }


def learning_path_node(state: CareerPathState) -> dict[str, Any]:
    """Generate learning recommendations."""
    
    logger.info("Generating learning path")
    
    if not state["skill_gaps"]:
        logger.info("No skill gaps found, returning empty recommendations")
        return {
            "courses": [],
            "projects": [],
            "certifications": [],
            "workflow_status": "learning_path_generated"
        }
    
    skills_needed = [gap["skill"] for gap in state["skill_gaps"][:MAX_SKILL_GAPS]]
    
    prompt = f"""For skills: {', '.join(skills_needed)}

Recommend courses, projects, and certifications.

Return JSON:
{{"courses": [{{"name": "...", "provider": "...", "url": "...", "duration": "..."}}], "projects": [{{"name": "...", "description": "...", "skills": ["..."]}}], "certifications": [{{"name": "...", "provider": "...", "url": "..."}}]}}"""
    
    try:
        response = _get_llm().invoke(prompt)
        result = _extract_json(response.content)
        
        logger.info(f"Generated {len(result.get('courses', []))} course recommendations")
        
        return {
            "courses": result.get("courses", []),
            "projects": result.get("projects", []),
            "certifications": result.get("certifications", []),
            "workflow_status": "learning_path_generated"
        }
    except Exception as e:
        logger.error(f"Learning path generation failed: {e}")
        return {
            "courses": [],
            "projects": [],
            "certifications": [],
            "workflow_status": "learning_path_generated",
            "error": str(e)
        }


def roadmap_generator_node(state: CareerPathState) -> dict[str, Any]:
    """Generate visual roadmap nodes and edges."""
    
    logger.info("Generating visual roadmap")
    
    nodes = []
    edges = []
    
    # Current state node
    skills_count = len(state['current_skills'])
    nodes.append({
        "id": "current",
        "type": "default",
        "data": {"label": f"Current State\n{skills_count} skills"},
        "position": {"x": 250, "y": 50},
        "style": {"background": "#e3f2fd", "border": "2px solid #2196f3"}
    })
    
    # Skill gap nodes
    if state["skill_gaps"]:
        for i, gap in enumerate(state["skill_gaps"][:MAX_SKILL_GAPS]):
            node_id = f"skill-{i}"
            color = "#fff3e0" if gap["priority"] == "high" else "#f3e5f5"
            border = "#ff9800" if gap["priority"] == "high" else "#9c27b0"
            nodes.append({
                "id": node_id,
                "type": "default",
                "data": {
                    "label": f"{gap['skill']}\n({gap['time_months']}mo)"
                },
                "position": {"x": 50 + (i * 150), "y": 200},
                "style": {"background": color, "border": f"2px solid {border}"}
            })
            edges.append({
                "id": f"e-current-{node_id}",
                "source": "current",
                "target": node_id,
                "animated": True,
                "style": {"stroke": border}
            })
    
    # Target job node
    if state["target_jobs"]:
        nodes.append({
            "id": "target",
            "type": "default",
            "data": {"label": state["target_jobs"][0]},
            "position": {"x": 250, "y": 350},
            "style": {"background": "#e8f5e9", "border": "2px solid #4caf50"}
        })
        
        # Connect skills to target
        for i in range(min(len(state["skill_gaps"]), MAX_SKILL_GAPS)):
            edges.append({
                "id": f"e-skill-{i}-target",
                "source": f"skill-{i}",
                "target": "target",
                "animated": True,
                "style": {"stroke": "#4caf50"}
            })
    
    logger.info(f"Generated {len(nodes)} nodes and {len(edges)} edges")
    
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
