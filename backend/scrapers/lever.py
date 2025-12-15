"""Lever job board scraper."""

import httpx
import asyncio
from typing import Optional
from api.schemas import Job
from scrapers.base_scraper import BaseScraper
from services.experience_extractor import extract_experience


class LeverScraper(BaseScraper):
    """Scraper for Lever job boards."""
    
    BASE_URL = "https://api.lever.co/v0/postings"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def fetch_company_jobs(self, company: str) -> list[Job]:
        """Fetch jobs for a single company from Lever."""
        jobs = []
        try:
            url = f"{self.BASE_URL}/{company}"
            response = await self.client.get(url)
            
            if response.status_code == 200:
                job_listings = response.json()
                
                for job_data in job_listings:
                    # Extract location from categories
                    location = job_data.get("categories", {}).get("location", "")
                    title = job_data.get("text", "")
                    
                    # Get description if available
                    description = job_data.get("descriptionPlain", "")
                    
                    # Extract experience requirements from title and description
                    min_exp, max_exp = extract_experience(title, description)
                    
                    job = Job(
                        id=f"lv_{company}_{job_data.get('id', '')}",
                        title=title,
                        company=company.replace("-", " ").title(),
                        location=location,
                        url=job_data.get("hostedUrl", ""),
                        source="lever",
                        posted_date=None,  # Lever doesn't always provide this
                        description=description[:1000] if description else None,
                        required_experience_min=min_exp,
                        required_experience_max=max_exp,
                    )
                    jobs.append(job)
                    
        except Exception as e:
            print(f"Error fetching jobs from Lever for {company}: {e}")
        
        return jobs
    
    async def fetch_jobs(
        self, 
        companies: list[str], 
        keywords: Optional[list[str]] = None
    ) -> list[Job]:
        """
        Fetch jobs from multiple Lever company boards.
        
        Args:
            companies: List of Lever company slugs (e.g., ["vercel", "anthropic"])
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
        return "lever"
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
