from typing import List, Dict

# Business-specific keyword mappings for content filtering - HYPER-FOCUS VERSION
BUSINESS_MAPPINGS: Dict[str, Dict[str, List[str]]] = {
    "SaaS Companies": {
        "keywords": ["saas", "software", "app", "platform", "subscription", "mrr", "arr", "users", "customers", "startup", "founder"],
        "subreddits": ["SaaS", "startups", "IndieHackers"]
    },
    "App Developers": {
        "keywords": ["app", "developer", "mobile app", "web app", "coding", "programming", "software development", "ios", "android", "frontend", "backend", "fullstack"],
        "subreddits": ["startups", "IndieHackers", "EntrepreneurRideAlong"]
    },
    "E-commerce Stores": {
        "keywords": ["ecommerce", "online store", "shopify", "amazon", "selling", "products", "inventory", "sales", "customers"],
        "subreddits": ["ecommerce", "Shopify", "EntrepreneurRideAlong"]
    },
    "Jobs and Hiring": {
        "keywords": ["job search", "resume help", "interview advice", "job leads", "career change", "unemployment", "job application", "hiring process", "job market", "career advice", "job openings", "job hunting tips"],
        "subreddits": ["jobs", "jobhunting", "layoffs"]
    }
}

# Industry-specific keyword mappings for content filtering - HYPER-FOCUS VERSION
INDUSTRY_MAPPINGS: Dict[str, Dict[str, List[str]]] = {
    "SaaS / Tech": {
        "keywords": ["saas", "software", "app", "platform", "subscription", "mrr", "arr", "users", "customers", "startup", "founder"],
        "subreddits": ["SaaS", "startups", "IndieHackers"]
    },
    "E-commerce": {
        "keywords": ["ecommerce", "online store", "shopify", "amazon", "selling", "products", "inventory", "sales", "customers"],
        "subreddits": ["ecommerce", "Shopify", "EntrepreneurRideAlong"]
    }
}

def get_business_options():
    """Get list of available business options - HYPER-FOCUS VERSION"""
    return list(BUSINESS_MAPPINGS.keys())

def get_industry_options():
    """Get list of available industry options - HYPER-FOCUS VERSION"""
    return list(INDUSTRY_MAPPINGS.keys())

def get_subreddits_for_business(business: str) -> list:
    """Get subreddits for a specific business"""
    if business in BUSINESS_MAPPINGS:
        return BUSINESS_MAPPINGS[business]["subreddits"]
    return []

def get_subreddits_for_industry(industry: str) -> list:
    """Get subreddits for a specific industry"""
    if industry in INDUSTRY_MAPPINGS:
        return INDUSTRY_MAPPINGS[industry]["subreddits"]
    return []

def get_keywords_for_business(business: str) -> list:
    """Get keywords for a specific business"""
    if business in BUSINESS_MAPPINGS:
        return BUSINESS_MAPPINGS[business]["keywords"]
    return []

def get_keywords_for_industry(industry: str) -> list:
    """Get keywords for a specific industry"""
    if industry in INDUSTRY_MAPPINGS:
        return INDUSTRY_MAPPINGS[industry]["keywords"]
    return []

def validate_business_selection(business: str) -> bool:
    """Validate if business selection is valid"""
    return business in BUSINESS_MAPPINGS

def validate_industry_selection(industry: str) -> bool:
    """Validate if industry selection is valid"""
    return industry in INDUSTRY_MAPPINGS
