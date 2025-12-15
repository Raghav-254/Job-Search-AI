"""Greenhouse job board scraper."""

import httpx
import asyncio
from typing import Optional
from api.schemas import Job
from scrapers.base_scraper import BaseScraper
from services.experience_extractor import extract_experience


class GreenhouseScraper(BaseScraper):
    """Scraper for Greenhouse job boards."""
    
    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def fetch_company_jobs(self, company: str) -> list[Job]:
        """Fetch jobs for a single company from Greenhouse."""
        jobs = []
        try:
            url = f"{self.BASE_URL}/{company}/jobs?content=true"  # Request content/description
            response = await self.client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                job_listings = data.get("jobs", [])
                
                for job_data in job_listings:
                    title = job_data.get("title", "")
                    # Get description if available (HTML content)
                    content = job_data.get("content", "")
                    
                    # Extract experience requirements from title and description
                    min_exp, max_exp = extract_experience(title, content)
                    
                    job = Job(
                        id=f"gh_{company}_{job_data.get('id', '')}",
                        title=title,
                        company=company.replace("-", " ").title(),
                        location=job_data.get("location", {}).get("name", ""),
                        url=job_data.get("absolute_url", ""),
                        source="greenhouse",
                        posted_date=job_data.get("updated_at", "")[:10] if job_data.get("updated_at") else None,
                        description=content[:1000] if content else None,  # Store truncated description
                        required_experience_min=min_exp,
                        required_experience_max=max_exp,
                    )
                    jobs.append(job)
                    
        except Exception as e:
            print(f"Error fetching jobs from Greenhouse for {company}: {e}")
        
        return jobs
    
    async def fetch_jobs(
        self, 
        companies: list[str], 
        keywords: Optional[list[str]] = None
    ) -> list[Job]:
        """
        Fetch jobs from multiple Greenhouse company boards.
        
        Args:
            companies: List of Greenhouse board slugs (e.g., ["stripe", "openai"])
            keywords: Optional keywords to filter job titles
            
        Returns:
            List of Job objects
        """
        # Fetch from all companies concurrently
        tasks = [self.fetch_company_jobs(company) for company in companies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results and filter out exceptions
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)
        
        # Filter by keywords if provided
        if keywords:
            keywords_lower = [kw.lower() for kw in keywords]
            all_jobs = [
                job for job in all_jobs 
                if any(kw in job.title.lower() for kw in keywords_lower)
            ]
        
        return all_jobs
    
    def get_source_name(self) -> str:
        return "greenhouse"
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
