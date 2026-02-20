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
from ..constants import MAX_TOKENS, TEMPERATURE, MAX_RESUME_LENGTH, MAX_SKILL_GAPS
from ..utils import deduplicate_skills, calculate_priority, estimate_learning_time
from ..model_config import get_model_config

logger = logging.getLogger(__name__)

# Get model configuration based on deployment mode
MODEL_CONFIG = get_model_config(os.getenv("DEPLOYMENT_MODE", "TESTING"))

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


def _get_llm(agent_name: str):
    """Get configured LLM instance for specific agent."""
    model_id = getattr(MODEL_CONFIG, agent_name)
    logger.info(f"Using model {model_id} for {agent_name}")
    return ChatBedrock(
        model_id=model_id,
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
        response = _get_llm("resume_analyzer").invoke(prompt)
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
            response = _get_llm("job_parser").invoke(prompt)
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
    """Identify and prioritize skill gaps with fit score."""
    
    logger.info("Analyzing skill gaps")
    
    current = set(s.lower() for s in state["current_skills"])
    gaps = []
    matched = []
    seen_skills = set()  # Track skills we've already added
    
    # Calculate matched and missing skills
    all_required = []
    for job_title, required in state["required_skills"].items():
        all_required.extend(required)
        for skill in required:
            if skill.lower() in current:
                matched.append(skill)
            elif skill.lower() not in seen_skills:  # Only add if not seen
                seen_skills.add(skill.lower())
                priority = calculate_priority(len(gaps) + 1, len(required))
                time_months = estimate_learning_time(skill)
                gaps.append({
                    "skill": skill,
                    "for_job": job_title,
                    "priority": priority,
                    "difficulty": "medium",
                    "time_months": time_months
                })
    
    # Calculate fit score
    total_skills = len(set(s.lower() for s in all_required))
    matched_count = len(set(s.lower() for s in matched))
    fit_score = int((matched_count / total_skills * 100)) if total_skills > 0 else 0
    
    # Sort by priority then skill name
    gaps.sort(key=lambda x: (x["priority"] != "high", x["skill"]))
    
    logger.info(f"Found {len(gaps)} skill gaps, fit score: {fit_score}%")
    
    return {
        "skill_gaps": gaps,
        "fit_score": fit_score,
        "matched_skills": list(set(matched)),
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
        response = _get_llm("learning_path").invoke(prompt)
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


def critical_review_node(state: CareerPathState) -> dict[str, Any]:
    """Provide honest assessment of career readiness."""
    
    logger.info("Performing critical review")
    
    prompt = f"""Provide brutally honest feedback on this career transition readiness.

CURRENT PROFILE:
- Skills: {', '.join(state['current_skills'][:20])}
- Experience: {state.get('experience_years', {})}
- Strengths: {', '.join(state.get('strengths', [])[:5])}

TARGET ROLE: {', '.join(state['target_jobs'])}

FIT SCORE: {state.get('fit_score', 0)}%
SKILL GAPS: {len(state.get('skill_gaps', []))} missing skills

Provide critical analysis in JSON:
{{
  "overallRating": <1-10 score>,
  "readinessLevel": "<not ready|somewhat ready|ready|highly ready>",
  "strengths": [<what works well>],
  "weaknesses": [<what needs improvement>],
  "redFlags": [<potential concerns>],
  "competitivePosition": "<how you compare to typical candidates>",
  "actionableSteps": [<specific improvements>],
  "timelineRealism": "<honest assessment of timeline>",
  "summary": "<2-3 sentence honest assessment>"
}}

Be direct and constructive. Return ONLY valid JSON."""
    
    try:
        response = _get_llm("critical_review").invoke(prompt)
        result = _extract_json(response.content)
        
        logger.info(f"Critical review complete: {result.get('overallRating', 0)}/10")
        
        return {
            "critical_review": result,
            "workflow_status": "review_complete"
        }
    except Exception as e:
        logger.error(f"Critical review failed: {e}")
        return {
            "critical_review": {
                "overallRating": 0,
                "summary": "Review unavailable",
                "strengths": [],
                "weaknesses": [],
                "actionableSteps": []
            },
            "workflow_status": "review_complete",
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
