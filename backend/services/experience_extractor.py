"""Experience requirement extractor from job descriptions."""

import re
from typing import Optional, Tuple


# Regex patterns to extract experience requirements
EXPERIENCE_PATTERNS = [
    # "8+ years of experience" or "8+ yrs experience"
    (r'(\d+)\+\s*(?:years?|yrs?)(?:\s+of)?(?:\s+experience)?', 'min_only'),
    
    # "5-7 years of experience" or "5 to 7 years"
    (r'(\d+)\s*[-–—to]+\s*(\d+)\s*(?:years?|yrs?)', 'range'),
    
    # "minimum 6 years" or "min 6 years" or "at least 6 years"
    (r'(?:minimum|min\.?|at\s+least)\s*(\d+)\s*(?:years?|yrs?)', 'min_only'),
    
    # "6 years minimum" or "6+ years required"
    (r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:minimum|min\.?|required|or\s+more)', 'min_only'),
    
    # "over 5 years" or "more than 5 years"
    (r'(?:over|more\s+than)\s*(\d+)\s*(?:years?|yrs?)', 'min_only'),
    
    # "X years of professional experience"
    (r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:professional|industry|relevant|hands-on)\s+experience', 'min_only'),
    
    # Generic "X years experience" (last resort, more common pattern)
    (r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?experience', 'exact'),
]

# Title-based experience heuristics (fallback when no description available)
TITLE_EXPERIENCE_HINTS = {
    'intern': (0, 1),
    'internship': (0, 1),
    'junior': (0, 2),
    'entry': (0, 2),
    'associate': (1, 3),
    'mid': (2, 5),
    'senior': (5, 10),
    'sr': (5, 10),
    'staff': (8, 15),
    'principal': (10, 20),
    'distinguished': (15, 25),
    'architect': (8, 15),
    'lead': (5, 12),
    'manager': (5, 15),
    'director': (10, 20),
    'vp': (12, 25),
    'head': (10, 20),
}


def extract_experience_from_text(text: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Extract experience requirements from job description text.
    
    Args:
        text: Job description or any text containing experience requirements
        
    Returns:
        Tuple of (min_years, max_years). Either or both can be None.
    """
    if not text:
        return None, None
    
    text_lower = text.lower()
    
    # Try each pattern
    for pattern, pattern_type in EXPERIENCE_PATTERNS:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        
        if matches:
            if pattern_type == 'range':
                # Pattern captures two groups (min, max)
                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        min_exp = int(match[0])
                        max_exp = int(match[1])
                        # Validate reasonable range
                        if 0 <= min_exp <= 30 and 0 <= max_exp <= 30 and min_exp <= max_exp:
                            return min_exp, max_exp
            
            elif pattern_type == 'min_only':
                # Pattern captures one group (min)
                for match in matches:
                    exp = int(match) if isinstance(match, str) else int(match[0]) if isinstance(match, tuple) else None
                    if exp is not None and 0 <= exp <= 30:
                        return exp, None
            
            elif pattern_type == 'exact':
                # Treat as exact requirement (min = max)
                for match in matches:
                    exp = int(match) if isinstance(match, str) else int(match[0]) if isinstance(match, tuple) else None
                    if exp is not None and 0 <= exp <= 30:
                        return exp, exp
    
    return None, None


def extract_experience_from_title(title: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Infer experience requirements from job title.
    
    Used as a fallback when description doesn't contain explicit requirements.
    
    Args:
        title: Job title
        
    Returns:
        Tuple of (min_years, max_years) based on title keywords.
    """
    if not title:
        return None, None
    
    title_lower = title.lower()
    
    for keyword, (min_exp, max_exp) in TITLE_EXPERIENCE_HINTS.items():
        if keyword in title_lower:
            return min_exp, max_exp
    
    return None, None


def extract_experience(title: str, description: Optional[str] = None) -> Tuple[Optional[int], Optional[int]]:
    """
    Extract experience requirements from job title and/or description.
    
    Priority:
    1. Extract from description (most accurate)
    2. Infer from title (fallback)
    
    Args:
        title: Job title
        description: Job description (optional)
        
    Returns:
        Tuple of (min_years, max_years). Either or both can be None.
    """
    # First try to extract from description
    if description:
        min_exp, max_exp = extract_experience_from_text(description)
        if min_exp is not None:
            return min_exp, max_exp
    
    # Fallback to title-based inference
    return extract_experience_from_title(title)


def is_experience_match(
    user_experience: int,
    required_min: Optional[int],
    required_max: Optional[int],
    buffer_years: int = 1  # Changed from 2 to 1 year buffer
) -> bool:
    """
    Check if user's experience matches job requirements.
    
    Args:
        user_experience: User's years of experience
        required_min: Job's minimum required experience
        required_max: Job's maximum required experience
        buffer_years: Allow jobs requiring up to this many years more than user has
        
    Returns:
        True if user qualifies for the job
    """
    # If no requirements specified, assume match
    if required_min is None:
        return True
    
    # User should have at least (required_min - buffer) years
    # This allows slight flexibility for strong candidates
    effective_min = max(0, required_min - buffer_years)
    
    # Check if user meets minimum (with buffer)
    if user_experience < effective_min:
        return False
    
    # If there's a max requirement, check user isn't overqualified
    # (Usually not a concern, but some jobs want specific ranges)
    if required_max is not None:
        # Allow some buffer for overqualification too
        effective_max = required_max + buffer_years
        if user_experience > effective_max:
            return False
    
    return True

