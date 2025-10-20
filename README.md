# Hope Backend - Final Version 2

This is the backend for the Hope Lead Finder Platform with all fixes applied.

## Files Included:
- `app/` - FastAPI backend application
- `requirements.txt` - Python dependencies (Python 3.13 compatible)
- `start_server.py` - Server startup script (fixed for Railway deployment)
- `reddit_lead_finder.db` - SQLite database
- `.python-version` - Forces Python 3.11.9
- `runtime.txt` - Additional Python version specification
- `README.md` - This file

## Deployment:
This backend is designed to be deployed on Railway with:
- Correct host configuration (0.0.0.0) for external access
- Python 3.11.9 compatibility
- Updated package versions

## Environment Variables Required:
- `reddit_client_id` - Reddit API client ID
- `reddit_client_secret` - Reddit API client secret
- `reddit_user_agent` - Reddit user agent string
- `PYTHON_VERSION` - Set to 3.11.9 (optional, files will force this)

