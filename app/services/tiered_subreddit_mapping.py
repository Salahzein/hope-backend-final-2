from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

# TIERED SUBREDDIT MAPPINGS - 4 Tiers per business/industry
# Tier 1 = Most relevant, Tier 4 = Less relevant
TIERED_SUBREDDIT_MAPPINGS: Dict[str, Dict[int, List[str]]] = {
    # Business Types
    "SaaS Companies": {
        1: ["SaaS", "startups", "Entrepreneur"],  # Most relevant (PRIMARY)
        2: ["IndieHackers", "microSaaS", "EntrepreneurRideAlong"],
        3: ["smallbusiness", "Entrepreneur", "business"],
        4: ["business", "startup_ideas", "entrepreneurridealong"]
    },
    "App Developers": {
        1: ["SaaS", "startups", "Entrepreneur"],
        2: ["IndieHackers", "EntrepreneurRideAlong", "programming"],
        3: ["webdev", "learnprogramming", "web_design"],
        4: ["freelance", "forhire", "careers"]
    },
    "E-commerce Stores": {
        1: ["ecommerce", "dropshipping", "Shopify"],
        2: ["AmazonSeller", "Entrepreneur", "smallbusiness"],
        3: ["marketing", "SEO", "digital_marketing"],
        4: ["business", "freelance", "entrepreneur"]
    },
    "Marketing Agencies": {
        1: ["marketing", "SEO", "digital_marketing"],
        2: ["PPC", "socialmedia", "content_marketing"],
        3: ["Entrepreneur", "business", "smallbusiness"],
        4: ["freelance", "forhire", "webdev"]
    },
    "Freelance Designers": {
        1: ["freelance", "graphic_design", "Design"],
        2: ["DesignCritiques", "web_design", "UI_Design"],
        3: ["Entrepreneur", "smallbusiness", "marketing"],
        4: ["forhire", "workonline", "careers"]
    },
    "Coffee Shops / Cafés": {
        1: ["CoffeeShopOwners", "Coffee", "Barista"],
        2: ["smallbusiness", "Entrepreneur", "restaurant"],
        3: ["marketing", "SEO", "LocalSEO"],
        4: ["business", "finance", "investing"]
    },
    "Online Course Creators": {
        1: ["online_instructors", "InstructionalDesign", "edtech"],
        2: ["Entrepreneur", "marketing", "digital_marketing"],
        3: ["business", "smallbusiness", "SEO"],
        4: ["webdev", "web_design", "content_marketing"]
    },
    "Local Service Businesses": {
        1: ["smallbusiness", "Entrepreneur", "LocalSEO"],
        2: ["marketing", "SEO", "PPC"],
        3: ["business", "finance", "investing"],
        4: ["webdev", "web_design", "forhire"]
    },
    "Consultants / Coaches": {
        1: ["consulting", "Coaching", "Entrepreneur"],
        2: ["business", "smallbusiness", "marketing"],
        3: ["freelance", "forhire", "careers"],
        4: ["webdev", "web_design", "content_marketing"]
    },
    "Jobs and Hiring": {
        1: ["jobs", "jobhunting", "jobsearch"],
        2: ["careers", "resumes", "GetEmployed"],
        3: ["Remotework", "RemoteJobs", "Ukjobs"],
        4: ["careerguidance", "jobsearchhacks", "Unemployment"]
    },
    
    # Industry Types
    "SaaS / Tech": {
        1: ["SaaS", "startups", "Entrepreneur"],
        2: ["IndieHackers", "microSaaS", "EntrepreneurRideAlong"],
        3: ["smallbusiness", "Entrepreneur", "business"],
        4: ["business", "startup_ideas", "entrepreneurridealong"]
    },
    "E-commerce": {
        1: ["ecommerce", "dropshipping", "Shopify"],
        2: ["AmazonSeller", "Entrepreneur", "smallbusiness"],
        3: ["marketing", "SEO", "digital_marketing"],
        4: ["business", "freelance", "entrepreneur"]
    },
    "Marketing & Advertising": {
        1: ["marketing", "SEO", "digital_marketing"],
        2: ["PPC", "socialmedia", "content_marketing"],
        3: ["Entrepreneur", "business", "smallbusiness"],
        4: ["freelance", "forhire", "webdev"]
    },
    "Education / Edtech": {
        1: ["online_instructors", "InstructionalDesign", "edtech"],
        2: ["Entrepreneur", "marketing", "digital_marketing"],
        3: ["business", "smallbusiness", "SEO"],
        4: ["webdev", "web_design", "content_marketing"]
    },
    "Food & Beverage": {
        1: ["CoffeeShopOwners", "Coffee", "Barista"],
        2: ["smallbusiness", "Entrepreneur", "restaurant"],
        3: ["marketing", "SEO", "LocalSEO"],
        4: ["business", "finance", "investing"]
    },
    "Local Services": {
        1: ["smallbusiness", "Entrepreneur", "LocalSEO"],
        2: ["marketing", "SEO", "PPC"],
        3: ["business", "finance", "investing"],
        4: ["webdev", "web_design", "forhire"]
    },
    "Finance / Fintech": {
        1: ["Fintech", "PersonalFinance", "FinancialPlanning"],
        2: ["investing", "Entrepreneur", "smallbusiness"],
        3: ["business", "finance", "marketing"],
        4: ["webdev", "web_design", "forhire"]
    },
    "Freelancers / Creatives": {
        1: ["freelance", "graphic_design", "Design"],
        2: ["DesignCritiques", "web_design", "UI_Design"],
        3: ["Entrepreneur", "smallbusiness", "marketing"],
        4: ["forhire", "workonline", "careers"]
    },
    "Consulting / Coaching": {
        1: ["consulting", "Coaching", "Entrepreneur"],
        2: ["business", "smallbusiness", "marketing"],
        3: ["freelance", "forhire", "careers"],
        4: ["webdev", "web_design", "content_marketing"]
    }
}

# In-memory storage for user request counts
user_request_counts: Dict[str, int] = {}

def get_tiered_subreddits(business_type: str, request_number: int) -> List[str]:
    """
    Get subreddits for a specific tier based on request number
    
    Args:
        business_type: The business/industry type (e.g., "SaaS Companies")
        request_number: The request number (1-4)
        
    Returns:
        List of subreddits for the specified tier
    """
    logger.info(f"🔍 TIERED SYSTEM: business_type='{business_type}', request_number={request_number}")
    
    # Determine tier from request number - cycles through tiers 1-4 indefinitely
    tier = ((request_number - 1) % 4) + 1
    
    # Check if business type exists in tiered mappings
    if business_type in TIERED_SUBREDDIT_MAPPINGS:
        tier_mapping = TIERED_SUBREDDIT_MAPPINGS[business_type]
        subreddits = tier_mapping.get(tier, tier_mapping[1])  # Fallback to tier 1 if tier doesn't exist
        logger.info(f"✅ TIERED SYSTEM: Using tier {tier} subreddits for '{business_type}': {subreddits}")
        return subreddits
    else:
        # Fallback for unknown business types
        logger.warning(f"⚠️ Business type '{business_type}' not found in tiered mappings, using default")
        return ["Entrepreneur", "startups", "smallbusiness"]

def get_user_request_count(user_id: str) -> int:
    """Get the current request count for a user"""
    count = user_request_counts.get(user_id, 0)
    logger.info(f"📊 GET COUNT: user_id='{user_id}' → count={count}")
    return count

def increment_user_request_count(user_id: str) -> int:
    """Increment and return the request count for a user"""
    current_count = user_request_counts.get(user_id, 0)
    new_count = current_count + 1
    user_request_counts[user_id] = new_count
    logger.info(f"📈 INCREMENT COUNT: user_id='{user_id}' → {current_count} → {new_count}")
    return new_count

def reset_user_request_count(user_id: str):
    """Reset the request count for a user"""
    old_count = user_request_counts.get(user_id, 0)
    if user_id in user_request_counts:
        del user_request_counts[user_id]
    logger.info(f"🔄 RESET COUNT: user_id='{user_id}' → {old_count} → 0")

def get_tier_info(business_type: str, request_number: int) -> Dict[str, any]:
    """Get tier information including subreddits and quality note"""
    tier = min(request_number, 4)
    subreddits = get_tiered_subreddits(business_type, request_number)
    
    quality_notes = {
        1: "Beta Quality - Most relevant subreddits for optimal results",
        2: "Good Quality - Relevant subreddits for quality results",
        3: "Moderate Quality - Additional subreddits for broader coverage",
        4: "Basic Quality - Expanded subreddits for comprehensive results"
    }
    
    return {
        "tier": tier,
        "subreddits": subreddits,
        "quality_note": quality_notes.get(tier, quality_notes[1]),
        "is_final_tier": tier == 4,
        "posts_per_subreddit": 500,
        "total_posts": len(subreddits) * 500
    }















