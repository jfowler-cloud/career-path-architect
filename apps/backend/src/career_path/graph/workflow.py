"""LangGraph workflow definition."""

from langgraph.graph import StateGraph, END

from .state import CareerPathState
from .nodes import (
    resume_analyzer_node,
    job_parser_node,
    gap_analysis_node,
    learning_path_node,
    critical_review_node,
    roadmap_generator_node,
)


def create_workflow() -> StateGraph:
    """Create the career path analysis workflow."""
    
    workflow = StateGraph(CareerPathState)
    
    # Add nodes
    workflow.add_node("resume_analyzer", resume_analyzer_node)
    workflow.add_node("job_parser", job_parser_node)
    workflow.add_node("gap_analysis", gap_analysis_node)
    workflow.add_node("learning_path", learning_path_node)
    workflow.add_node("critical_review", critical_review_node)
    workflow.add_node("roadmap_generator", roadmap_generator_node)
    
    # Define edges
    workflow.set_entry_point("resume_analyzer")
    workflow.add_edge("resume_analyzer", "job_parser")
    workflow.add_edge("job_parser", "gap_analysis")
    workflow.add_edge("gap_analysis", "learning_path")
    workflow.add_edge("learning_path", "critical_review")
    workflow.add_edge("critical_review", "roadmap_generator")
    workflow.add_edge("roadmap_generator", END)
    
    return workflow.compile()
