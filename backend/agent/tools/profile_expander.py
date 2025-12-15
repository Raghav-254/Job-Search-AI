"""Profile expander tool - expands minimal user input to rich profile."""

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel


class ExpandedProfileData(BaseModel):
    """Structured expanded profile data."""
    inferred_skills: list[str]
    seniority_level: str
    target_titles: list[str]
    company_tier: str
    expected_salary_range: str


PROFILE_EXPANDER_PROMPT = """You are an expert tech recruiter who understands job roles, skills, and career levels.

Given the following user profile, expand it into a comprehensive profile:

Current Role: {role}
Current Company: {company}
Years of Experience: {years_of_experience}
Listed Skills: {skills}
Expected Salary: {expected_salary}
Preferred Location: {location}

Based on this information, provide:

1. **Inferred Skills**: What technical and soft skills would someone in this role at this company likely have? Include both listed skills and inferred ones. Be specific to their domain.

2. **Seniority Level**: Based on years of experience, what seniority level are they at?
   - 0-1 years: Junior/Entry
   - 2-3 years: Mid-level
   - 4-6 years: Senior
   - 7-10 years: Staff/Lead
   - 10+ years: Principal/Architect

3. **Target Job Titles**: IMPORTANT - Generate a comprehensive list of job titles they should search for:
   - Include their EXACT current title (e.g., "Software Engineer", "Senior Software Engineer")
   - Include GENERIC variations (e.g., "Software Engineer" should also match "Engineer", "Developer", "SWE")
   - Include SPECIALIZED variations (e.g., "Frontend Engineer", "Backend Engineer", "Full Stack Engineer")
   - Include EQUIVALENT titles at different companies (e.g., "SDE", "Software Developer", "Member of Technical Staff")
   - Include ADJACENT roles they could qualify for
   - Generate at least 8-12 diverse titles to ensure broad matching
   
   For example, if someone is a "Senior Software Engineer":
   - "Software Engineer"
   - "Senior Software Engineer"
   - "Software Developer"
   - "Senior Software Developer"
   - "SDE II"
   - "SDE III"
   - "Full Stack Engineer"
   - "Backend Engineer"
   - "Frontend Engineer"
   - "Member of Technical Staff"
   - "Platform Engineer"

4. **Company Tier**: What tier is their current company? (FAANG, Big Tech, Unicorn, Late-stage Startup, Early-stage Startup, Enterprise, Agency, etc.)

5. **Expected Salary Range**: Based on their experience and company tier, what salary range should they target? Format as "$XXX,XXX - $XXX,XXX"

Respond in JSON format with these exact keys:
- inferred_skills (array of strings)
- seniority_level (string)
- target_titles (array of strings - generate 8-12 diverse titles)
- company_tier (string)
- expected_salary_range (string)
"""


async def expand_profile(
    role: str,
    company: str,
    years_of_experience: int,
    skills: Optional[list[str]] = None,
    expected_salary: Optional[int] = None,
    location: Optional[str] = None,
    llm: Optional[ChatOpenAI] = None
) -> ExpandedProfileData:
    """
    Expand minimal user profile into comprehensive profile using AI.
    
    Args:
        role: Current job role
        company: Current company
        years_of_experience: Years of experience
        skills: Optional list of skills
        expected_salary: Optional expected salary
        location: Optional preferred location
        llm: Optional LLM instance (creates one if not provided)
        
    Returns:
        ExpandedProfileData with inferred information
    """
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    # Create structured output LLM
    structured_llm = llm.with_structured_output(ExpandedProfileData)
    
    prompt = ChatPromptTemplate.from_template(PROFILE_EXPANDER_PROMPT)
    
    chain = prompt | structured_llm
    
    result = await chain.ainvoke({
        "role": role,
        "company": company,
        "years_of_experience": years_of_experience,
        "skills": ", ".join(skills) if skills else "Not specified",
        "expected_salary": f"${expected_salary:,}" if expected_salary else "Not specified",
        "location": location or "Not specified"
    })
    
    # Ensure the original role is always included in target titles
    if role not in result.target_titles:
        result.target_titles.insert(0, role)
    
    return result
