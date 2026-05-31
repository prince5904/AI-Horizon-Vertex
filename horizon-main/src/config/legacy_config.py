"""
Minimal Configuration for Composio + Groq Enrichment
All credentials loaded from .env file for security
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# LinkedIn Integration
LINKEDIN_CONNECTED_ACCOUNT_ID = os.getenv("LINKEDIN_CONNECTED_ACCOUNT_ID", "")
LINKEDIN_ENTITY_ID = os.getenv("LINKEDIN_ENTITY_ID", "")
COMPOSIO_LINKEDIN_AUTH = os.getenv("COMPOSIO_LINKEDIN_AUTH", "")
LINKEDIN_API_ENABLED = os.getenv("LINKEDIN_API_ENABLED", "false").lower() == "true"  # Set to "true" when properly configured

# Gmail Integration Credentials
GMAIL_USER_ID = os.getenv("GMAIL_USER_ID", "")
GMAIL_ACCOUNT_ID = os.getenv("GMAIL_ACCOUNT_ID", "")
GMAIL_AUTH_CONFIG_ID = os.getenv("GMAIL_AUTH_CONFIG_ID", "")

# User ID for Composio (fallback to Gmail User ID if not specified)
USER_ID = os.getenv("GMAIL_USER_ID", os.getenv("LINKEDIN_ENTITY_ID", ""))

# Google Sheets Integration
GOOGLE_SHEETS_AUTH_CONFIG_ID = os.getenv("GOOGLE_SHEETS_AUTH_CONFIG_ID", "")
GOOGLE_SHEETS_ACCOUNT_ID = os.getenv("GOOGLE_SHEETS_ACCOUNT_ID", "")
GOOGLE_SHEETS_USER_ID = os.getenv("GOOGLE_SHEETS_USER_ID", os.getenv("GMAIL_USER_ID", ""))

# Google Calendar Integration
GOOGLE_CALENDAR_ACCOUNT_ID = os.getenv("GOOGLE_CALENDAR_ACCOUNT_ID", "")
GOOGLE_CALENDAR_USER_ID = os.getenv("GOOGLE_CALENDAR_USER_ID", os.getenv("GMAIL_USER_ID", ""))
GOOGLE_CALENDAR_AUTH_CONFIG_ID = os.getenv("GOOGLE_CALENDAR_AUTH_CONFIG_ID", "")

# LLM Settings  
GROQ_MODEL = "llama-3.1-8b-instant"  # Reliable primary model
GROQ_MODEL_BACKUP = "llama-3.1-70b-versatile"  # Backup model
GROQ_MODEL_ALTERNATIVE = "meta-llama/llama-4-scout-17b-16e-instruct"  # Alternative for specific tasks

# Validation
def validate_config():
    """Validate that required environment variables are set"""
    required_vars = {
        "COMPOSIO_API_KEY": COMPOSIO_API_KEY,
        "GROQ_API_KEY": GROQ_API_KEY,
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. Please check your .env file.")
    
    print("✅ Configuration loaded successfully")
    return True