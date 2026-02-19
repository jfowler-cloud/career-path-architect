"""Tests for validation utilities."""

import pytest
from career_path.validation import (
    sanitize_text,
    validate_skill_name,
    validate_job_title,
    sanitize_list,
    extract_keywords,
    validate_resume_text,
    normalize_skill_name
)


def test_sanitize_text_basic():
    """Test basic text sanitization."""
    result = sanitize_text("  Hello   World  ")
    assert result == "Hello World"


def test_sanitize_text_null_bytes():
    """Test removal of null bytes."""
    result = sanitize_text("Hello\x00World")
    assert result == "HelloWorld"


def test_sanitize_text_max_length():
    """Test max length truncation."""
    result = sanitize_text("Hello World", max_length=5)
    assert result == "Hello"


def test_sanitize_text_empty():
    """Test empty text."""
    assert sanitize_text("") == ""
    assert sanitize_text(None) == ""


def test_validate_skill_name_valid():
    """Test valid skill names."""
    assert validate_skill_name("Python") is True
    assert validate_skill_name("C++") is True
    assert validate_skill_name("Node.js") is True
    assert validate_skill_name("C#") is True


def test_validate_skill_name_invalid():
    """Test invalid skill names."""
    assert validate_skill_name("") is False
    assert validate_skill_name("A") is False  # Too short
    assert validate_skill_name("A" * 101) is False  # Too long
    assert validate_skill_name("Python@") is False  # Invalid char


def test_validate_job_title_valid():
    """Test valid job titles."""
    assert validate_job_title("Software Engineer") is True
    assert validate_job_title("Senior DevOps Engineer (AWS/Azure)") is True
    assert validate_job_title("Full-Stack Developer") is True


def test_validate_job_title_invalid():
    """Test invalid job titles."""
    assert validate_job_title("") is False
    assert validate_job_title("AB") is False  # Too short
    assert validate_job_title("A" * 201) is False  # Too long
    assert validate_job_title("Engineer@Company") is False  # Invalid char


def test_sanitize_list_basic():
    """Test basic list sanitization."""
    items = ["Python", "  AWS  ", "Docker", ""]
    result = sanitize_list(items)
    assert result == ["Python", "AWS", "Docker"]


def test_sanitize_list_duplicates():
    """Test duplicate removal."""
    items = ["Python", "python", "PYTHON", "AWS"]
    result = sanitize_list(items)
    assert result == ["Python", "AWS"]


def test_sanitize_list_max_items():
    """Test max items limit."""
    items = ["A", "B", "C", "D", "E"]
    result = sanitize_list(items, max_items=3)
    assert len(result) == 3
    assert result == ["A", "B", "C"]


def test_sanitize_list_empty():
    """Test empty list."""
    assert sanitize_list([]) == []
    assert sanitize_list(None) == []


def test_extract_keywords_basic():
    """Test basic keyword extraction."""
    text = "Python developer with AWS and Docker experience"
    keywords = extract_keywords(text)
    assert "Python" in keywords
    assert "AWS" in keywords
    assert "Docker" in keywords
    assert "with" not in keywords  # Stop word


def test_extract_keywords_min_length():
    """Test minimum length filtering."""
    text = "I am a Python developer"
    keywords = extract_keywords(text, min_length=3)
    assert "am" not in keywords
    assert "Python" in keywords


def test_extract_keywords_max_keywords():
    """Test max keywords limit."""
    text = " ".join([f"skill{i}" for i in range(100)])
    keywords = extract_keywords(text, max_keywords=10)
    assert len(keywords) == 10


def test_extract_keywords_duplicates():
    """Test duplicate removal."""
    text = "Python Python python AWS aws"
    keywords = extract_keywords(text)
    assert keywords.count("Python") + keywords.count("python") == 1
    assert keywords.count("AWS") + keywords.count("aws") == 1


def test_extract_keywords_empty():
    """Test empty text."""
    assert extract_keywords("") == []
    assert extract_keywords(None) == []


def test_validate_resume_text_valid():
    """Test valid resume text."""
    text = "A" * 100
    is_valid, msg = validate_resume_text(text)
    assert is_valid is True
    assert msg == ""


def test_validate_resume_text_too_short():
    """Test resume text too short."""
    text = "Short"
    is_valid, msg = validate_resume_text(text, min_length=50)
    assert is_valid is False
    assert "at least 50" in msg


def test_validate_resume_text_too_long():
    """Test resume text too long."""
    text = "A" * 60000
    is_valid, msg = validate_resume_text(text, max_length=50000)
    assert is_valid is False
    assert "not exceed 50000" in msg


def test_validate_resume_text_empty():
    """Test empty resume text."""
    is_valid, msg = validate_resume_text("")
    assert is_valid is False
    assert "cannot be empty" in msg


def test_normalize_skill_name_basic():
    """Test basic skill name normalization."""
    assert normalize_skill_name("Python") == "python"
    assert normalize_skill_name("  AWS  ") == "aws"


def test_normalize_skill_name_variations():
    """Test common skill variations."""
    assert normalize_skill_name("JavaScript") == "js"
    assert normalize_skill_name("TypeScript") == "ts"
    assert normalize_skill_name("Python3") == "python"
    assert normalize_skill_name("NodeJS") == "node.js"
    assert normalize_skill_name("ReactJS") == "react"


def test_normalize_skill_name_empty():
    """Test empty skill name."""
    assert normalize_skill_name("") == ""
    assert normalize_skill_name(None) == ""


def test_sanitize_text_multiple_spaces():
    """Test multiple space normalization."""
    result = sanitize_text("Hello    World    Test")
    assert result == "Hello World Test"


def test_sanitize_text_newlines():
    """Test newline handling."""
    result = sanitize_text("Hello\nWorld\nTest")
    assert result == "Hello World Test"


def test_validate_skill_name_special_chars():
    """Test skill names with special characters."""
    assert validate_skill_name("C++") is True
    assert validate_skill_name("C#") is True
    assert validate_skill_name("F#") is True
    assert validate_skill_name(".NET") is True


def test_sanitize_list_preserves_order():
    """Test that list order is preserved."""
    items = ["Z", "A", "M", "B"]
    result = sanitize_list(items)
    assert result == ["Z", "A", "M", "B"]


def test_extract_keywords_special_chars():
    """Test keyword extraction with special characters."""
    text = "Cplusplus and Csharp developer with dotNET experience"
    keywords = extract_keywords(text)
    assert "Cplusplus" in keywords
    assert "Csharp" in keywords
    assert "dotNET" in keywords


def test_validate_resume_text_whitespace_only():
    """Test resume with only whitespace."""
    is_valid, msg = validate_resume_text("   \n\n   ")
    assert is_valid is False
    assert "cannot be empty" in msg
