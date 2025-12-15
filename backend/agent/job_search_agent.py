"""Main job search agent that orchestrates the job search workflow."""

from typing import Optional
from langchain_openai import ChatOpenAI

from api.schemas import ProfileRequest, ExpandedProfile, RankedJob, AnalyzeResponse
from agent.tools.profile_expander import expand_profile
from agent.tools.job_ranker import rank_jobs
from services.job_aggregator import JobAggregator, LOCATION_ALIASES
from config import get_settings


class JobSearchAgent:
    """
    AI-powered job search agent.
    
    Workflow:
    1. Expand user profile using AI
    2. Fetch jobs from multiple sources with filtering
    3. Rank jobs by match score
    4. Sort by score AND location preference
    5. Return curated results
    """
    
    def __init__(self):
        settings = get_settings()
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=settings.openai_api_key
        )
        self.job_aggregator = JobAggregator()
    
    async def analyze(self, profile: ProfileRequest) -> AnalyzeResponse:
        """
        Analyze user profile and return matched jobs.
        """
        # Step 1: Expand user profile
        expanded_data = await expand_profile(
            role=profile.role,
            company=profile.company,
            years_of_experience=profile.years_of_experience,
            skills=profile.skills,
            expected_salary=profile.expected_salary,
            location=profile.location,
            llm=self.llm
        )
        
        expanded_profile = ExpandedProfile(
            original_role=profile.role,
            original_company=profile.company,
            years_of_experience=profile.years_of_experience,
            inferred_skills=expanded_data.inferred_skills,
            seniority_level=expanded_data.seniority_level,
            target_titles=expanded_data.target_titles,
            company_tier=expanded_data.company_tier,
            expected_salary_range=expanded_data.expected_salary_range
        )
        
        # Step 2: Fetch jobs from all sources WITH FILTERING
        jobs, companies_searched = await self.job_aggregator.fetch_all_jobs(
            target_companies=profile.target_companies,
            keywords=expanded_data.target_titles,
            location=profile.location,
            years_of_experience=profile.years_of_experience,
            seniority_level=expanded_data.seniority_level,
        )
        
        # Step 3: Rank jobs by match score
        ranked_jobs: list[RankedJob] = []
        if jobs:
            ranked_jobs = await rank_jobs(
                jobs=jobs,
                role=profile.role,
                company=profile.company,
                company_tier=expanded_data.company_tier,
                years_of_experience=profile.years_of_experience,
                seniority_level=expanded_data.seniority_level,
                skills=expanded_data.inferred_skills,
                target_titles=expanded_data.target_titles,
                expected_salary_range=expanded_data.expected_salary_range,
                llm=self.llm
            )
        
        # Filter by salary if specified
        if profile.expected_salary:
            ranked_jobs = [
                job for job in ranked_jobs
                if job.salary_max is None or job.salary_max >= profile.expected_salary
            ]
        
        # Step 4: Sort by match score AND location preference
        if profile.location:
            ranked_jobs = self._sort_by_score_and_location(ranked_jobs, profile.location)
        
        return AnalyzeResponse(
            profile=expanded_profile,
            jobs=ranked_jobs,
            total_jobs=len(ranked_jobs),
            companies_searched=companies_searched
        )
    
    def _sort_by_score_and_location(self, jobs: list[RankedJob], preferred_location: str) -> list[RankedJob]:
        """
        Sort jobs by location preference (PRIMARY) and match score (SECONDARY).
        
        Location priority: Preferred → India → Europe → US → Remote → Others
        Within each location group, jobs are sorted by match score.
        """
        location_lower = preferred_location.lower().strip()
        
        # Find matching location terms for preferred location
        match_terms = set()
        for canonical, aliases in LOCATION_ALIASES.items():
            if any(alias in location_lower for alias in aliases):
                match_terms.update(aliases)
                if canonical in ['bengaluru', 'hyderabad', 'mumbai', 'delhi', 'pune', 'chennai']:
                    match_terms.add('india')
        
        if not match_terms:
            match_terms = {location_lower}
        
        # Location categories
        india_terms = {'india', 'bengaluru', 'bangalore', 'hyderabad', 'mumbai', 'pune', 'chennai', 'delhi', 'gurgaon', 'noida', 'kolkata'}
        europe_terms = {'uk', 'london', 'berlin', 'germany', 'amsterdam', 'netherlands', 'paris', 'france', 'dublin', 'ireland', 'stockholm', 'sweden', 'zurich', 'switzerland', 'europe', 'barcelona', 'spain', 'lisbon', 'portugal'}
        us_terms = {'usa', 'united states', 'san francisco', 'new york', 'seattle', 'austin', 'boston', 'los angeles', 'denver', 'chicago', 'california', 'ca', 'ny', 'wa', 'tx'}
        remote_terms = {'remote', 'anywhere', 'distributed', 'work from home', 'wfh'}
        
        def get_location_priority(job_location: str) -> int:
            """Get location priority (lower = higher priority)."""
            loc = job_location.lower()
            
            # Priority 0: Exact preferred location match
            if any(term in loc for term in match_terms):
                return 0
            # Priority 1: India jobs
            if any(term in loc for term in india_terms):
                return 1
            # Priority 2: Europe jobs
            if any(term in loc for term in europe_terms):
                return 2
            # Priority 3: US jobs
            if any(term in loc for term in us_terms):
                return 3
            # Priority 4: Remote jobs
            if any(term in loc for term in remote_terms):
                return 4
            # Priority 5: No location specified
            if not loc.strip():
                return 5
            # Priority 6: Other locations
            return 6
        
        def sort_key(job: RankedJob) -> tuple:
            job_location = job.location or ''
            location_priority = get_location_priority(job_location)
            
            # Return tuple: (location_priority FIRST, -score for descending SECOND)
            return (location_priority, -job.match_score)
        
        return sorted(jobs, key=sort_key)
    
    async def close(self):
        """Clean up resources."""
        await self.job_aggregator.close()
