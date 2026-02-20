"""
Model Configuration for Career Path Architect

Defines which Claude models to use for each agent.
Three deployment modes:
- TESTING: Uses Haiku 3.0 for all agents (fastest, cheapest, for development)
- OPTIMIZED: Uses mix of models based on task complexity (balanced cost/quality)
- PREMIUM: Uses Opus 4.5 for all agents (best quality, highest cost)
"""

from enum import Enum


class DeploymentMode(str, Enum):
    TESTING = "TESTING"
    OPTIMIZED = "OPTIMIZED"
    PREMIUM = "PREMIUM"


class ModelConfig:
    """Model configuration for each agent."""
    
    def __init__(
        self,
        resume_analyzer: str,
        job_parser: str,
        gap_analysis: str,
        learning_path: str,
        critical_review: str,
        roadmap_generator: str,
    ):
        self.resume_analyzer = resume_analyzer
        self.job_parser = job_parser
        self.gap_analysis = gap_analysis
        self.learning_path = learning_path
        self.critical_review = critical_review
        self.roadmap_generator = roadmap_generator


# Model configurations for different deployment modes
MODEL_CONFIGS = {
    # Testing: Haiku 3.0 for everything (fast and cheap for development)
    DeploymentMode.TESTING: ModelConfig(
        resume_analyzer="anthropic.claude-3-haiku-20240307-v1:0",
        job_parser="anthropic.claude-3-haiku-20240307-v1:0",
        gap_analysis="anthropic.claude-3-haiku-20240307-v1:0",
        learning_path="anthropic.claude-3-haiku-20240307-v1:0",
        critical_review="anthropic.claude-3-haiku-20240307-v1:0",
        roadmap_generator="anthropic.claude-3-haiku-20240307-v1:0",
    ),
    
    # Optimized: Mix of models based on task complexity
    DeploymentMode.OPTIMIZED: ModelConfig(
        # Simple extraction - use Haiku 4.5 (fast and cost-effective)
        resume_analyzer="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        
        # Simple parsing - use Haiku 4.5
        job_parser="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        
        # Analysis - use Sonnet 4.5 (excellent balance)
        gap_analysis="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        
        # Recommendations - use Opus 4.5 (best reasoning)
        learning_path="us.anthropic.claude-opus-4-5-20251101-v1:0",
        
        # Critical review - use Opus 4.5 (most important feedback)
        critical_review="us.anthropic.claude-opus-4-5-20251101-v1:0",
        
        # Visual generation - use Sonnet 4.5
        roadmap_generator="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    ),
    
    # Premium: Opus 4.5 for everything (maximum reasoning)
    DeploymentMode.PREMIUM: ModelConfig(
        resume_analyzer="us.anthropic.claude-opus-4-5-20251101-v1:0",
        job_parser="us.anthropic.claude-opus-4-5-20251101-v1:0",
        gap_analysis="us.anthropic.claude-opus-4-5-20251101-v1:0",
        learning_path="us.anthropic.claude-opus-4-5-20251101-v1:0",
        critical_review="us.anthropic.claude-opus-4-5-20251101-v1:0",
        roadmap_generator="us.anthropic.claude-opus-4-5-20251101-v1:0",
    ),
}


def get_model_config(mode: str | None = None) -> ModelConfig:
    """
    Get model configuration for deployment.
    
    Cost comparison (approximate per 1M tokens):
    
    Claude Opus 4.5:
      Input: $15.00 | Output: $75.00
    
    Claude Sonnet 4.5:
      Input: $3.00 | Output: $15.00
    
    Claude Haiku 4.5:
      Input: $1.00 | Output: $5.00
      
    Claude Haiku 3.0:
      Input: $0.25 | Output: $1.25
    
    Estimated savings:
    - TESTING vs PREMIUM: ~95% cost reduction
    - OPTIMIZED vs PREMIUM: ~60% cost reduction
    """
    try:
        deployment_mode = DeploymentMode(mode.upper()) if mode else DeploymentMode.TESTING
    except ValueError:
        print(f"Unknown deployment mode: {mode}, defaulting to TESTING")
        deployment_mode = DeploymentMode.TESTING
    
    return MODEL_CONFIGS[deployment_mode]
