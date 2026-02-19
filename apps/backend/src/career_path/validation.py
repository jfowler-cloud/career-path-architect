"""Input validation and sanitization utilities."""

import re
from typing import List, Optional


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize text input by removing dangerous characters.
    
    Args:
        text: Input text to sanitize
        max_length: Optional maximum length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    # Trim to max length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()


def validate_skill_name(skill: str) -> bool:
    """Validate skill name format.
    
    Args:
        skill: Skill name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not skill or len(skill) < 2:
        return False
    
    if len(skill) > 100:
        return False
    
    # Allow letters, numbers, spaces, hyphens, dots, plus, sharp
    pattern = r'^[a-zA-Z0-9\s\-\.+#]+$'
    return bool(re.match(pattern, skill))


def validate_job_title(title: str) -> bool:
    """Validate job title format.
    
    Args:
        title: Job title to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not title or len(title) < 3:
        return False
    
    if len(title) > 200:
        return False
    
    # Allow letters, numbers, spaces, common punctuation
    pattern = r'^[a-zA-Z0-9\s\-\.,/()&]+$'
    return bool(re.match(pattern, title))


def sanitize_list(items: List[str], max_items: Optional[int] = None) -> List[str]:
    """Sanitize a list of strings.
    
    Args:
        items: List of strings to sanitize
        max_items: Optional maximum number of items
        
    Returns:
        Sanitized list
    """
    if not items:
        return []
    
    # Remove empty strings and sanitize
    sanitized = [sanitize_text(item) for item in items if item and item.strip()]
    
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for item in sanitized:
        lower = item.lower()
        if lower not in seen:
            seen.add(lower)
            unique.append(item)
    
    # Limit to max items
    if max_items:
        unique = unique[:max_items]
    
    return unique


def extract_keywords(text: str, min_length: int = 2, max_keywords: int = 50) -> List[str]:
    """Extract keywords from text.
    
    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length
        max_keywords: Maximum number of keywords
        
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Split on whitespace and punctuation
    words = re.findall(r'\b[a-zA-Z0-9+#]+\b', text)
    
    # Filter by length and common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    keywords = [
        word for word in words
        if len(word) >= min_length and word.lower() not in stop_words
    ]
    
    # Remove duplicates (case-insensitive)
    seen = set()
    unique = []
    for keyword in keywords:
        lower = keyword.lower()
        if lower not in seen:
            seen.add(lower)
            unique.append(keyword)
    
    return unique[:max_keywords]


def validate_resume_text(text: str, min_length: int = 50, max_length: int = 50000) -> tuple[bool, str]:
    """Validate resume text.
    
    Args:
        text: Resume text to validate
        min_length: Minimum length
        max_length: Maximum length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Resume text cannot be empty"
    
    text = text.strip()
    
    if len(text) < min_length:
        return False, f"Resume text must be at least {min_length} characters"
    
    if len(text) > max_length:
        return False, f"Resume text must not exceed {max_length} characters"
    
    return True, ""


def normalize_skill_name(skill: str) -> str:
    """Normalize skill name for comparison.
    
    Args:
        skill: Skill name to normalize
        
    Returns:
        Normalized skill name
    """
    if not skill:
        return ""
    
    # Convert to lowercase
    normalized = skill.lower().strip()
    
    # Replace common variations
    replacements = {
        'javascript': 'js',
        'typescript': 'ts',
        'python3': 'python',
        'nodejs': 'node.js',
        'reactjs': 'react',
        'vuejs': 'vue',
    }
    
    for old, new in replacements.items():
        if normalized == old:
            normalized = new
            break
    
    return normalized
