"""Constants for career path workflow."""

# Model configuration
MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
MAX_TOKENS = 2000
TEMPERATURE = 0.3

# Limits
MAX_RESUME_LENGTH = 2000
MAX_SKILL_GAPS = 5
MAX_TARGET_JOBS = 5

# Timeouts (seconds)
LLM_TIMEOUT = 30
WORKFLOW_TIMEOUT = 120
