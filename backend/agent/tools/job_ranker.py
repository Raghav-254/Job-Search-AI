"""Job ranker tool - ranks jobs by match score using AI."""

import asyncio
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from api.schemas import Job, RankedJob


class JobRankingResult(BaseModel):
    """Ranking result for a single job."""
    match_score: int
    insight: str
    match_reasons: list[str]


class BatchRankingResult(BaseModel):
    """Batch ranking results."""
    rankings: list[JobRankingResult]


JOB_RANKER_PROMPT = """You are an expert tech recruiter matching candidates to jobs.

## Candidate Profile:
- Current Role: {role}
- Company: {company} ({company_tier})
- Years of Experience: {years_of_experience}
- Seniority Level: {seniority_level}
- Skills: {skills}
- Target Titles: {target_titles}
- Expected Salary: {expected_salary_range}

## Jobs to Rank:
{jobs_text}

For EACH job listed above, provide:
1. **match_score** (0-100): How well does this job match the candidate?
   - 90-100: Perfect match
   - 70-89: Strong match
   - 50-69: Moderate match
   - Below 50: Weak match

2. **insight** (1-2 sentences): Explain why this is/isn't a good match in a friendly, helpful tone.

3. **match_reasons** (2-4 bullet points): Key reasons for the score.

Consider:
- Title alignment with experience level
- Company prestige relative to current company
- Skill relevance (infer from job title)
- Career progression (lateral move, step up, step down)

Respond with a list of rankings in the same order as the jobs provided.
"""


async def rank_jobs(
    jobs: list[Job],
    role: str,
    company: str,
    company_tier: str,
    years_of_experience: int,
    seniority_level: str,
    skills: list[str],
    target_titles: list[str],
    expected_salary_range: str,
    llm: Optional[ChatOpenAI] = None,
    max_jobs: int = 50,  # Limit to prevent excessive API calls
    batch_size: int = 15,  # Larger batches = fewer API calls
    max_concurrent: int = 5,  # Max parallel API calls
) -> list[RankedJob]:
    """
    Rank jobs by match score using AI with parallel processing.
    
    Args:
        jobs: List of jobs to rank
        role: User's current role
        company: User's current company
        company_tier: Company tier (FAANG, Startup, etc.)
        years_of_experience: Years of experience
        seniority_level: Seniority level
        skills: List of skills
        target_titles: Target job titles
        expected_salary_range: Expected salary range
        llm: Optional LLM instance
        max_jobs: Maximum jobs to rank (prevents excessive API calls)
        batch_size: Jobs per API call
        max_concurrent: Maximum concurrent API calls
        
    Returns:
        List of RankedJob objects sorted by match score
    """
    if not jobs:
        return []
    
    # Limit jobs to prevent excessive API usage
    jobs_to_rank = jobs[:max_jobs]
    
    if llm is None:
        llm = ChatOpenAI(model="gpt-5-nano", temperature=0.2)
    
    # Create batches
    batches = [
        jobs_to_rank[i:i + batch_size] 
        for i in range(0, len(jobs_to_rank), batch_size)
    ]
    
    # Process batches in parallel with concurrency limit
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def rank_with_semaphore(batch: list[Job]) -> list[RankedJob]:
        async with semaphore:
            return await _rank_batch(
                batch, role, company, company_tier, years_of_experience,
                seniority_level, skills, target_titles, expected_salary_range, llm
            )
    
    # Run all batches concurrently
    results = await asyncio.gather(
        *[rank_with_semaphore(batch) for batch in batches],
        return_exceptions=True
    )
    
    # Flatten results, skip failed batches
    all_ranked_jobs: list[RankedJob] = []
    for result in results:
        if isinstance(result, list):
            all_ranked_jobs.extend(result)
        else:
            # Log error but continue with other batches
            print(f"Batch ranking failed: {result}")
    
    # Sort by match score descending
    all_ranked_jobs.sort(key=lambda x: x.match_score, reverse=True)
    
    return all_ranked_jobs


async def _rank_batch(
    jobs: list[Job],
    role: str,
    company: str,
    company_tier: str,
    years_of_experience: int,
    seniority_level: str,
    skills: list[str],
    target_titles: list[str],
    expected_salary_range: str,
    llm: ChatOpenAI
) -> list[RankedJob]:
    """Rank a batch of jobs."""
    
    # Format jobs for prompt
    jobs_text = "\n".join([
        f"{idx + 1}. {job.title} at {job.company} ({job.location or 'Location not specified'})"
        for idx, job in enumerate(jobs)
    ])
    
    structured_llm = llm.with_structured_output(BatchRankingResult)
    prompt = ChatPromptTemplate.from_template(JOB_RANKER_PROMPT)
    chain = prompt | structured_llm
    
    result = await chain.ainvoke({
        "role": role,
        "company": company,
        "company_tier": company_tier,
        "years_of_experience": years_of_experience,
        "seniority_level": seniority_level,
        "skills": ", ".join(skills),
        "target_titles": ", ".join(target_titles),
        "expected_salary_range": expected_salary_range,
        "jobs_text": jobs_text
    })
    
    # Combine job data with rankings
    ranked_jobs = []
    for job, ranking in zip(jobs, result.rankings):
        ranked_job = RankedJob(
            id=job.id,
            title=job.title,
            company=job.company,
            location=job.location,
            url=job.url,
            source=job.source,
            posted_date=job.posted_date,
            description=job.description,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            match_score=ranking.match_score,
            insight=ranking.insight,
            match_reasons=ranking.match_reasons
        )
        ranked_jobs.append(ranked_job)
    
    return ranked_jobs
