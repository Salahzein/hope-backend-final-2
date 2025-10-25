from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

# Simplified subreddit mappings for beta launch
# 3 primary subreddits + 1 backup per business/industry type
SIMPLIFIED_SUBREDDIT_MAPPINGS: Dict[str, Dict[str, List[str]]] = {
    # Business Types (Specific)
    "SaaS Companies": {
        "primary": ["SaaS", "startups", "Entrepreneur"],
        "backup": ["IndieDev"]
    },
    "App Developers": {
        "primary": ["SaaS", "startups", "Entrepreneur"],
        "backup": ["IndieDev"]
    },
    # ... (keeping other mappings the same)
}

# In-memory storage for user request counts
user_request_counts: Dict[str, int] = {}

def get_beta_subreddits(business_type: str, use_backup: bool = False) -> List[str]:
    """Get subreddits for beta launch - 3 primary + optional backup"""
    
    # DIAGNOSTIC LOGGING
    logger.info(f"🔍 BETA SYSTEM DEBUG START")
    logger.info(f"   business_type='{business_type}', use_backup={use_backup}")
    logger.info(f"   Total user_request_counts entries: {len(user_request_counts)}")
    logger.info(f"   All user_ids in memory: {list(user_request_counts.keys())}")
    logger.info(f"   Full user_request_counts: {user_request_counts}")
    print(f"🔍 BETA SYSTEM DEBUG: business_type='{business_type}', use_backup={use_backup}")
    print(f"   user_request_counts: {user_request_counts}")
    
    if business_type not in SIMPLIFIED_SUBREDDIT_MAPPINGS:
        logger.warning(f"❌ Business type '{business_type}' not found in beta mappings, using fallback")
        print(f"❌ BETA SYSTEM DEBUG: Business type '{business_type}' not found in beta mappings, using fallback")
        from app.services.business_mapping import get_subreddits_for_business
        fallback_subreddits = get_subreddits_for_business(business_type)[:3]  # Take first 3
        logger.info(f"🔄 FALLBACK TRIGGERED: Returning {fallback_subreddits}")
        print(f"🔄 BETA SYSTEM DEBUG: Fallback subreddits: {fallback_subreddits}")
        return fallback_subreddits
    
    mapping = SIMPLIFIED_SUBREDDIT_MAPPINGS[business_type]
    subreddits = mapping["primary"].copy()
    
    if use_backup:
        subreddits.extend(mapping["backup"])
    
    logger.info(f"✅ BETA SYSTEM: Using subreddits: {subreddits}")
    logger.info(f"🔍 BETA SYSTEM DEBUG END")
    print(f"✅ BETA SYSTEM DEBUG: Using subreddits: {subreddits}")
    return subreddits

# Keep old function for backward compatibility but redirect to new system
def get_tiered_subreddits(business_type: str, request_number: int) -> List[str]:
    """Legacy function - redirects to new beta system"""
    logger.info(f"📞 TIERED_CALLED: business_type='{business_type}', request_number={request_number}")
    print(f"📞 TIERED_CALLED DEBUG: business_type='{business_type}', request_number={request_number}")
    return get_beta_subreddits(business_type, use_backup=False)

def get_user_request_count(user_id: str) -> int:
    """Get the current request count for a user"""
    count = user_request_counts.get(user_id, 0)
    logger.info(f"📊 GET COUNT: user_id='{user_id}' → count={count}")
    print(f"📊 GET COUNT DEBUG: user_id='{user_id}' → count={count}")
    return count

def increment_user_request_count(user_id: str) -> int:
    """Increment and return the request count for a user"""
    current_count = user_request_counts.get(user_id, 0)
    new_count = current_count + 1
    user_request_counts[user_id] = new_count
    logger.info(f"📈 INCREMENT COUNT: user_id='{user_id}' → {current_count} → {new_count}")
    logger.info(f"   State after increment: {user_request_counts}")
    print(f"📈 INCREMENT COUNT DEBUG: user_id='{user_id}' → {current_count} → {new_count}")
    print(f"   State after increment: {user_request_counts}")
    return new_count

def reset_user_request_count(user_id: str):
    """Reset the request count for a user"""
    old_count = user_request_counts.get(user_id, 0)
    if user_id in user_request_counts:
        del user_request_counts[user_id]
    logger.info(f"🔄 RESET COUNT: user_id='{user_id}' → {old_count} → 0")
    print(f"🔄 RESET COUNT DEBUG: user_id='{user_id}' → {old_count} → 0")

def get_current_tier(business_type: str, request_number: int) -> int:
    """Get the current tier number for display purposes"""
    return 1  # Always tier 1 for beta

def get_beta_info(business_type: str) -> Dict[str, any]:
    """Get beta system information including subreddits and quality note"""
    subreddits = get_beta_subreddits(business_type, use_backup=False)
    
    return {
        "tier": 1,  # Always tier 1 for beta (highest quality)
        "subreddits": subreddits,
        "quality_note": "Beta Quality - Most relevant subreddits for optimal results",
        "is_final_tier": True,
        "posts_per_subreddit": 500,
        "total_posts": len(subreddits) * 500
    }

# Keep old function for backward compatibility
def get_tier_info(business_type: str, request_number: int) -> Dict[str, any]:
    """Legacy function - redirects to new beta system"""
    return get_beta_info(business_type)

