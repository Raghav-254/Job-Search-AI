"""Base scraper interface."""

from abc import ABC, abstractmethod
from typing import Optional
from api.schemas import Job


class BaseScraper(ABC):
    """Abstract base class for job scrapers."""
    
    @abstractmethod
    async def fetch_jobs(
        self, 
        companies: list[str], 
        keywords: Optional[list[str]] = None
    ) -> list[Job]:
        """
        Fetch jobs from the source.
        
        Args:
            companies: List of company identifiers to search
            keywords: Optional keywords to filter jobs
            
        Returns:
            List of Job objects
        """
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of the job source."""
        pass


