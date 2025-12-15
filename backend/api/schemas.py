"""Pydantic schemas for API request and response models."""

from pydantic import BaseModel, Field
from typing import Optional


class ProfileRequest(BaseModel):
    """User profile input for job search."""
    
    role: str = Field(..., description="Current job role", min_length=1)
    company: str = Field(..., description="Current or recent company", min_length=1)
    years_of_experience: int = Field(..., description="Years of experience", ge=0, le=50)
    skills: Optional[list[str]] = Field(default=None, description="List of skills (optional)")
    expected_salary: Optional[int] = Field(default=None, description="Expected salary in USD (optional)")
    location: Optional[str] = Field(default="Remote", description="Preferred location")
    target_companies: Optional[list[str]] = Field(default=None, description="Specific companies to search")
    
    class Config:
        json_schema_extra = {
            "example": {
                "role": "Frontend Engineer",
                "company": "Google",
                "years_of_experience": 5,
                "skills": ["React", "TypeScript"],
                "expected_salary": 200000,
                "location": "Remote",
                "target_companies": ["stripe", "vercel", "openai"]
            }
        }


class ExpandedProfile(BaseModel):
    """AI-expanded user profile."""
    
    original_role: str
    original_company: str
    years_of_experience: int
    inferred_skills: list[str]
    seniority_level: str
    target_titles: list[str]
    company_tier: str
    expected_salary_range: str


class Job(BaseModel):
    """Job listing."""
    
    id: str
    title: str
    company: str
    location: Optional[str] = None
    url: str
    source: str  # greenhouse, lever, remoteok, etc.
    posted_date: Optional[str] = None
    description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    # Experience requirements extracted from description
    required_experience_min: Optional[int] = None  # Minimum years required
    required_experience_max: Optional[int] = None  # Maximum years (for ranges)


class RankedJob(Job):
    """Job with match score and insights."""
    
    match_score: int = Field(..., ge=0, le=100)
    insight: str
    match_reasons: list[str]


class AnalyzeResponse(BaseModel):
    """Response from the analyze endpoint."""
    
    profile: ExpandedProfile
    jobs: list[RankedJob]
    total_jobs: int
    companies_searched: list[str]


class ErrorResponse(BaseModel):
    """Error response."""
    
    error: str
    detail: Optional[str] = None
