"""API route definitions."""

from fastapi import APIRouter, HTTPException
from api.schemas import ProfileRequest, AnalyzeResponse, ErrorResponse
from agent.job_search_agent import JobSearchAgent
from services.job_aggregator import JobAggregator

router = APIRouter(prefix="/api", tags=["jobs"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def analyze_profile(profile: ProfileRequest) -> AnalyzeResponse:
    """
    Analyze user profile and return matched jobs.
    
    This endpoint:
    1. Expands the user's profile using AI to infer skills and target titles
    2. Fetches jobs from Greenhouse and Lever job boards
    3. Ranks jobs by match score using AI
    4. Returns deduplicated, ranked job listings
    """
    try:
        agent = JobSearchAgent()
        result = await agent.analyze(profile)
        await agent.close()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing profile: {str(e)}"
        )


@router.get("/companies")
async def get_available_companies() -> dict:
    """
    Get list of available companies that can be searched.
    
    Returns companies organized by job board source.
    """
    return JobAggregator.get_available_companies()


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "job-search-api"}


