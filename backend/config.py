"""Configuration and environment variables."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI
    openai_api_key: str = ""
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # App settings
    debug: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# =============================================================================
# COMPANY LISTS - PRIORITIZED FOR INDIA
# =============================================================================

# PRIORITY 1: MNCs / Big Tech with India Offices (Greenhouse)
GREENHOUSE_MNCS_INDIA = [
    # Big Tech with large India presence
    "google",
    "meta",
    "amazon",
    "microsoft",
    "apple",
    "netflix",
    "uber",
    "linkedin",
    "salesforce",
    "adobe",
    "oracle",
    "vmware",
    "cisco",
    "nvidia",
    "intel",
    "qualcomm",
    "samsung",
    
    # Data & Cloud with India offices
    "databricks",
    "snowflake",
    "mongodb",
    "elastic",
    "confluent",
    "datadog",
    "splunk",
    "newrelic",
    "pagerduty",
    
    # Fintech MNCs with India offices
    "stripe",
    "paypal",
    "visa",
    "mastercard",
    "square",
    "plaid",
    "coinbase",
    
    # Enterprise SaaS with India offices
    "atlassian",
    "servicenow",
    "workday",
    "twilio",
    "zendesk",
    "hubspot",
    "okta",
    "crowdstrike",
    "zscaler",
    
    # AI/ML companies with India presence
    "openai",
    "anthropic",
    
    # Product companies with India offices
    "figma",
    "canva",
    "notion",
    "airtable",
    "asana",
    "dropbox",
    "box",
    "docusign",
    "zoom",
    "slack",
]

# PRIORITY 1: MNCs / Big Tech with India Offices (Lever)
LEVER_MNCS_INDIA = [
    "atlassian",
    "netflix",
    "spotify",
    "notion",
    "figma",
    "airtable",
    "vercel",
    "supabase",
    "linear",
    "retool",
    "planetscale",
    "neon",
    "miro",
]

# PRIORITY 2: Indian Unicorns & Startups (Greenhouse)
GREENHOUSE_COMPANIES_INDIA = [
    # Fintech
    "razorpay",
    "groww",
    "cred",
    "slice",
    "jupiter-money",
    "fi-money",
    "smallcase",
    "niyo",
    "rupeek",
    "lendingkart",
    
    # E-commerce & Consumer
    "swiggy",
    "zomato",
    "meesho",
    "nykaa",
    "myntra",
    "udaan",
    "bigbasket",
    "dunzo",
    "blinkit",
    "urbancompany",
    
    # Mobility & Logistics
    "ola",
    "rapido",
    "delhivery",
    "blackbuck",
    "rivigo",
    
    # EdTech
    "byjus",
    "unacademy",
    "vedantu",
    "upgrad",
    "eruditus",
    "physicswallah",
    "scaler",
    
    # SaaS & B2B
    "browserstack",
    "druva",
    "whatfix",
    "moengage",
    "clevertap",
    "leadsquared",
    "zoho",
    "freshworks",
    "chargebee",
    
    # HealthTech
    "pharmeasy",
    "practo",
    "healthifyme",
    "cult-fit",
    
    # Others
    "dream11",
    "sharechat",
    "dailyhunt",
    "inmobi",
    "media-net",
]

# PRIORITY 2: Indian Startups (Lever)
LEVER_COMPANIES_INDIA = [
    "flipkart",
    "phonepe",
    "paytm",
    "postman",
    "hasura",
    "chargebee",
    "freshworks",
    "clevertap",
    "helpshift",
    "wingify",
    "haptik",
    "yellow-ai",
    "sprinklr",
    "gupshup",
]

# PRIORITY 3: Europe Remote-friendly Companies (Greenhouse)
GREENHOUSE_COMPANIES_EUROPE = [
    # Remote-first / Europe HQ
    "spotify",
    "klarna",
    "revolut",
    "wise",
    "n26",
    "monzo",
    "deliveroo",
    "zalando",
    "messagebird",
    "mollie",
    "adyen",
    "booking",
    "gitlab",
    "automattic",
    "canonical",
    "hotjar",
    "buffer",
    "doist",
    "zapier",
]

# PRIORITY 3: Europe Remote-friendly (Lever)
LEVER_COMPANIES_EUROPE = [
    "remote",    # Remote.com
    "oyster",
    "deel",
    "lattice",
    "loom",
    "netlify",
]

# =============================================================================
# COMBINED LISTS (MNCs first, then Indian startups, then Europe remote)
# =============================================================================

GREENHOUSE_COMPANIES = (
    GREENHOUSE_MNCS_INDIA +      # Priority 1: MNCs with India offices
    GREENHOUSE_COMPANIES_INDIA + # Priority 2: Indian startups
    GREENHOUSE_COMPANIES_EUROPE  # Priority 3: Europe remote
)

LEVER_COMPANIES = (
    LEVER_MNCS_INDIA +           # Priority 1: MNCs with India offices
    LEVER_COMPANIES_INDIA +      # Priority 2: Indian startups
    LEVER_COMPANIES_EUROPE       # Priority 3: Europe remote
)
