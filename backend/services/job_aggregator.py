"""Job aggregator service - combines jobs from multiple sources."""

import re
from typing import Optional
from api.schemas import Job
from scrapers.greenhouse import GreenhouseScraper
from scrapers.lever import LeverScraper
from services.experience_extractor import is_experience_match
from config import GREENHOUSE_COMPANIES, LEVER_COMPANIES


# Experience level keywords mapping
EXPERIENCE_KEYWORDS = {
    "intern": ["intern", "internship"],
    "junior": ["junior", "entry", "associate", "new grad", "graduate", "i", "1"],
    "mid": ["mid", "ii", "2", "iii", "3"],
    "senior": ["senior", "sr", "lead", "iv", "4"],
    "staff": ["staff", "principal", "architect", "v", "5", "distinguished"],
    "manager": ["manager", "director", "head", "vp", "chief"],
}

# Location normalization mapping
LOCATION_ALIASES = {
    "bengaluru": ["bengaluru", "bangalore", "blr"],
    "hyderabad": ["hyderabad", "hyd"],
    "mumbai": ["mumbai", "bombay"],
    "delhi": ["delhi", "ncr", "gurgaon", "gurugram", "noida"],
    "pune": ["pune"],
    "chennai": ["chennai", "madras"],
    "india": ["india", "bengaluru", "bangalore", "hyderabad", "mumbai", "pune", "chennai", "delhi", "gurgaon", "noida"],
    "san francisco": ["san francisco", "sf", "bay area"],
    "new york": ["new york", "nyc", "ny", "manhattan", "brooklyn"],
    "seattle": ["seattle"],
    "austin": ["austin"],
    "boston": ["boston"],
    "london": ["london"],
    "berlin": ["berlin"],
    "remote": ["remote", "anywhere", "distributed", "work from home", "wfh"],
}

# Software/Tech related terms - jobs MUST have one of these
SOFTWARE_TERMS = {
    'software', 'frontend', 'backend', 'fullstack', 'full-stack', 'full stack',
    'web', 'mobile', 'ios', 'android', 'cloud', 'devops', 'sre', 'data',
    'machine learning', 'ml', 'ai', 'artificial intelligence', 'platform',
    'infrastructure', 'security', 'cybersecurity', 'product', 'ux', 'ui',
    'design', 'qa', 'quality', 'test', 'automation', 'python', 'java',
    'javascript', 'typescript', 'react', 'node', 'golang', 'rust', 'c++',
    'systems', 'distributed', 'api', 'integration', 'solutions', 'technical',
    'tech', 'it', 'information technology', 'computer', 'application',
    'sde', 'swe', 'mts', 'developer', 'programmer', 'coder', 'engineering manager',
}

# Non-software engineering terms to EXCLUDE
EXCLUDE_TERMS = {
    'food', 'mechanical', 'civil', 'electrical', 'chemical', 'industrial',
    'manufacturing', 'structural', 'environmental', 'biomedical', 'aerospace',
    'automotive', 'marine', 'nuclear', 'petroleum', 'agricultural', 'mining',
    'hardware', 'facilities', 'maintenance', 'hvac', 'plumbing', 'construction',
    'sales', 'marketing', 'hr', 'human resources', 'finance', 'accounting',
    'legal', 'compliance', 'operations', 'supply chain', 'logistics', 'warehouse',
    'customer success', 'customer support', 'receptionist', 'administrative',
}


class JobAggregator:
    """Aggregates jobs from multiple sources and handles deduplication."""
    
    def __init__(self):
        self.greenhouse_scraper = GreenhouseScraper()
        self.lever_scraper = LeverScraper()
        self._preferred_location = None
    
    async def fetch_all_jobs(
        self,
        target_companies: Optional[list[str]] = None,
        keywords: Optional[list[str]] = None,
        location: Optional[str] = None,
        years_of_experience: Optional[int] = None,
        seniority_level: Optional[str] = None,
    ) -> tuple[list[Job], list[str]]:
        """
        Fetch jobs from all sources with filtering.
        """
        self._preferred_location = location
        all_jobs: list[Job] = []
        companies_searched: list[str] = []
        
        # Determine which companies to search
        if target_companies:
            target_lower = [c.lower() for c in target_companies]
            gh_companies = [c for c in GREENHOUSE_COMPANIES if c.lower() in target_lower]
            lv_companies = [c for c in LEVER_COMPANIES if c.lower() in target_lower]
        else:
            gh_companies = GREENHOUSE_COMPANIES
            lv_companies = LEVER_COMPANIES
        
        # Fetch from Greenhouse
        if gh_companies:
            gh_jobs = await self.greenhouse_scraper.fetch_jobs(gh_companies, keywords=None)
            all_jobs.extend(gh_jobs)
            companies_searched.extend(gh_companies)
        
        # Fetch from Lever
        if lv_companies:
            lv_jobs = await self.lever_scraper.fetch_jobs(lv_companies, keywords=None)
            all_jobs.extend(lv_jobs)
            companies_searched.extend(lv_companies)
        
        # Apply filters
        filtered_jobs = all_jobs
        
        # Filter by keywords (software-focused matching)
        if keywords:
            filtered_jobs = self._filter_by_keywords(filtered_jobs, keywords)
        
        # Filter by location
        if location:
            filtered_jobs = self._filter_by_location(filtered_jobs, location)
        
        # Filter by experience/seniority
        if years_of_experience is not None or seniority_level:
            filtered_jobs = self._filter_by_experience(
                filtered_jobs, years_of_experience, seniority_level
            )
        
        # Deduplicate jobs
        deduplicated_jobs = self._deduplicate_jobs(filtered_jobs)
        
        # Sort by location preference (preferred location first, then remote)
        if location:
            deduplicated_jobs = self._sort_by_location_preference(deduplicated_jobs, location)
        
        return deduplicated_jobs, companies_searched
    
    def _filter_by_keywords(self, jobs: list[Job], keywords: list[str]) -> list[Job]:
        """
        Filter jobs by keywords with software-focused matching.
        
        A job matches if:
        1. It contains software-related terms AND
        2. It matches any keyword word AND
        3. It does NOT contain excluded terms (non-software engineering)
        """
        if not keywords:
            return jobs
        
        # Extract individual words from all keywords
        keyword_words = set()
        for kw in keywords:
            words = re.split(r'[\s,/\-]+', kw.lower())
            stop_words = {'a', 'an', 'the', 'and', 'or', 'at', 'in', 'on', 'for', 'to', 'of', 'i', 'ii', 'iii', 'iv', 'v'}
            keyword_words.update(w for w in words if len(w) > 2 and w not in stop_words)
        
        filtered = []
        for job in jobs:
            title_lower = job.title.lower()
            title_words = set(re.split(r'[\s,/\-]+', title_lower))
            
            # Check if job contains EXCLUDED terms (non-software)
            has_excluded = any(term in title_lower for term in EXCLUDE_TERMS)
            if has_excluded:
                continue
            
            # Check if job is software-related
            is_software_related = any(term in title_lower for term in SOFTWARE_TERMS)
            
            # Check if any keyword word matches
            has_keyword_match = bool(keyword_words & title_words)
            
            # Include if:
            # 1. Has keyword match AND is software-related, OR
            # 2. Is clearly a software role (sde, developer, etc.)
            if has_keyword_match and is_software_related:
                filtered.append(job)
            elif is_software_related and any(term in title_lower for term in ['engineer', 'developer', 'sde', 'swe', 'programmer']):
                # Include generic software roles
                filtered.append(job)
        
        return filtered
    
    def _filter_by_location(self, jobs: list[Job], preferred_location: str) -> list[Job]:
        """
        Filter jobs by location with fuzzy matching.
        """
        if not preferred_location:
            return jobs
        
        location_lower = preferred_location.lower().strip()
        
        # Check if user wants remote only
        is_remote_only = location_lower in ['remote', 'anywhere', 'wfh', 'work from home']
        
        # Find matching location aliases
        match_terms = set()
        for canonical, aliases in LOCATION_ALIASES.items():
            if any(alias in location_lower for alias in aliases):
                match_terms.update(aliases)
                # If searching for a city in India, also add "india"
                if canonical in ['bengaluru', 'hyderabad', 'mumbai', 'delhi', 'pune', 'chennai']:
                    match_terms.add('india')
        
        # If no specific location found, use the input directly
        if not match_terms:
            match_terms = {location_lower}
        
        # Remote terms - always include remote jobs
        remote_terms = {'remote', 'anywhere', 'distributed', 'work from home', 'wfh'}
        
        filtered = []
        for job in jobs:
            job_location = (job.location or '').lower()
            
            # Check if job is remote
            is_remote = any(term in job_location for term in remote_terms)
            
            # Check if job matches preferred location
            matches_preferred = any(term in job_location for term in match_terms)
            
            # Check if job has no location (might be remote)
            no_location = not job_location or job_location.strip() == ''
            
            if is_remote_only:
                # Only include remote jobs
                if is_remote or no_location:
                    filtered.append(job)
            else:
                # Include preferred location + remote
                if matches_preferred or is_remote or no_location:
                    filtered.append(job)
        
        return filtered
    
    def _sort_by_location_preference(self, jobs: list[Job], preferred_location: str) -> list[Job]:
        """
        Sort jobs by location priority (PRIMARY).
        
        Priority order:
        0. Preferred location (exact match)
        1. India
        2. Europe
        3. US
        4. Remote
        5. No location
        6. Others
        """
        location_lower = preferred_location.lower().strip()
        
        # Find matching location aliases for preferred location
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
        
        def get_location_priority(job: Job) -> int:
            job_location = (job.location or '').lower()
            
            # Priority 0: Exact preferred location match
            if any(term in job_location for term in match_terms):
                return 0
            # Priority 1: India jobs
            if any(term in job_location for term in india_terms):
                return 1
            # Priority 2: Europe jobs
            if any(term in job_location for term in europe_terms):
                return 2
            # Priority 3: US jobs
            if any(term in job_location for term in us_terms):
                return 3
            # Priority 4: Remote jobs
            if any(term in job_location for term in remote_terms):
                return 4
            # Priority 5: No location specified
            if not job_location.strip():
                return 5
            # Priority 6: Other locations
            return 6
        
        return sorted(jobs, key=get_location_priority)
    
    def _filter_by_experience(
        self, 
        jobs: list[Job], 
        years_of_experience: Optional[int],
        seniority_level: Optional[str]
    ) -> list[Job]:
        """
        Filter jobs by experience level.
        
        Uses two approaches:
        1. Extracted experience requirements from job descriptions (primary)
        2. Title-based heuristics (fallback)
        """
        if years_of_experience is None and not seniority_level:
            return jobs
        
        user_exp = years_of_experience or 0
        
        # Title-based heuristics for fallback
        appropriate_levels = set()
        if years_of_experience is not None:
            if years_of_experience <= 1:
                appropriate_levels.update(['intern', 'junior'])
            elif years_of_experience <= 3:
                appropriate_levels.update(['junior', 'mid'])
            elif years_of_experience <= 5:
                appropriate_levels.update(['mid', 'senior'])
            elif years_of_experience <= 8:
                appropriate_levels.update(['senior', 'staff'])
            else:
                appropriate_levels.update(['senior', 'staff', 'manager'])
        
        if seniority_level:
            level_lower = seniority_level.lower()
            for level, keywords in EXPERIENCE_KEYWORDS.items():
                if any(kw in level_lower for kw in keywords):
                    appropriate_levels.add(level)
        
        valid_keywords = set()
        for level in appropriate_levels:
            if level in EXPERIENCE_KEYWORDS:
                valid_keywords.update(EXPERIENCE_KEYWORDS[level])
        
        too_senior_keywords = set()
        if years_of_experience is not None and years_of_experience < 7:
            too_senior_keywords.update(EXPERIENCE_KEYWORDS.get('staff', []))
        if years_of_experience is not None and years_of_experience < 4:
            too_senior_keywords.update(EXPERIENCE_KEYWORDS.get('senior', []))
        
        filtered = []
        for job in jobs:
            # PRIMARY CHECK: Use extracted experience requirements from description
            if job.required_experience_min is not None:
                # Check if user qualifies based on extracted requirements
                if is_experience_match(
                    user_experience=user_exp,
                    required_min=job.required_experience_min,
                    required_max=job.required_experience_max,
                    buffer_years=1  # Allow 1 year flexibility only
                ):
                    filtered.append(job)
                # Skip jobs that require too much experience
                continue
            
            # FALLBACK: Use title-based heuristics if no extracted requirements
            title_lower = job.title.lower()
            
            is_too_senior = any(kw in title_lower for kw in too_senior_keywords)
            
            has_level_indicator = any(
                any(kw in title_lower for kw in keywords)
                for keywords in EXPERIENCE_KEYWORDS.values()
            )
            
            if is_too_senior:
                continue
            elif not has_level_indicator:
                filtered.append(job)
            elif any(kw in title_lower for kw in valid_keywords):
                filtered.append(job)
        
        return filtered
    
    def _deduplicate_jobs(self, jobs: list[Job]) -> list[Job]:
        """Remove duplicate jobs based on title + company combination."""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = (
                job.title.lower().strip(),
                job.company.lower().strip()
            )
            
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    async def close(self):
        """Close all scraper connections."""
        await self.greenhouse_scraper.close()
        await self.lever_scraper.close()
    
    @staticmethod
    def get_available_companies() -> dict[str, list[str]]:
        """Get list of available companies by source."""
        return {
            "greenhouse": GREENHOUSE_COMPANIES,
            "lever": LEVER_COMPANIES
        }
