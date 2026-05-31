"""
Application Settings with Type Safety and Validation

This module uses Pydantic for strong typing and validation of all configuration values.
All sensitive data is loaded from environment variables.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ComposioSettings(BaseModel):
    """Composio API configuration"""
    
    api_key: str = Field(..., description="Composio API key from https://app.composio.dev/settings")
    
    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v or v == "your_composio_api_key_here":
            raise ValueError("COMPOSIO_API_KEY must be set in .env file")
        return v


class GmailSettings(BaseModel):
    """Gmail integration configuration"""
    
    user_id: str = Field(..., description="Gmail user ID from Composio dashboard")
    account_id: str = Field(..., description="Gmail account ID from Composio")
    auth_config_id: str = Field(..., description="Gmail auth config ID")
    
    @field_validator('user_id', 'account_id', 'auth_config_id')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or v.startswith("your_"):
            raise ValueError(f"Gmail configuration incomplete. Check .env file")
        return v


class LinkedInSettings(BaseModel):
    """LinkedIn integration configuration"""
    
    connected_account_id: str = Field(default="", description="LinkedIn connected account ID")
    entity_id: str = Field(default="", description="LinkedIn entity ID")
    auth_token: str = Field(default="", description="LinkedIn auth token")
    api_enabled: bool = Field(default=False, description="Whether LinkedIn API is properly configured")
    
    @field_validator('api_enabled')
    @classmethod
    def validate_api_enabled(cls, v: bool, info) -> bool:
        """Validate that if API is enabled, credentials are present"""
        if v and not info.data.get('connected_account_id'):
            raise ValueError("LinkedIn API enabled but credentials missing")
        return v


class GoogleSheetsSettings(BaseModel):
    """Google Sheets integration configuration"""
    
    auth_config_id: str = Field(..., description="Google Sheets auth config ID")
    account_id: str = Field(..., description="Google Sheets account ID")
    user_id: str = Field(..., description="Google Sheets user ID")


class GoogleCalendarSettings(BaseModel):
    """Google Calendar integration configuration"""
    
    account_id: str = Field(..., description="Google Calendar account ID")
    user_id: str = Field(..., description="Google Calendar user ID")
    auth_config_id: str = Field(..., description="Google Calendar auth config ID")


class LLMSettings(BaseModel):
    """LLM configuration for AI processing"""
    
    groq_api_key: str = Field(..., description="Groq API key from https://console.groq.com/keys")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key (backup)")
    primary_model: str = Field(default="llama-3.1-8b-instant", description="Primary Groq model")
    backup_model: str = Field(default="llama-3.1-70b-versatile", description="Backup model")
    alternative_model: str = Field(default="meta-llama/llama-4-scout-17b-16e-instruct", description="Alternative model")
    
    @field_validator('groq_api_key')
    @classmethod
    def validate_groq_key(cls, v: str) -> str:
        if not v or v == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY must be set in .env file")
        return v


class Settings(BaseModel):
    """Complete application settings with validation"""
    
    # Core settings
    composio: ComposioSettings
    gmail: GmailSettings
    linkedin: LinkedInSettings
    google_sheets: GoogleSheetsSettings
    google_calendar: GoogleCalendarSettings
    llm: LLMSettings
    
    # Application settings
    debug_mode: bool = Field(default=False, description="Enable debug logging")
    max_retries: int = Field(default=3, ge=1, le=10, description="Maximum API retry attempts")
    timeout_seconds: int = Field(default=30, ge=5, le=120, description="API timeout in seconds")
    
    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        extra = "forbid"  # Don't allow extra fields


def get_settings() -> Settings:
    """
    Load and validate all application settings from environment variables.
    
    Returns:
        Settings: Validated application configuration
        
    Raises:
        ValueError: If required environment variables are missing or invalid
        
    Example:
        >>> settings = get_settings()
        >>> print(settings.composio.api_key[:10] + "...")
    """
    try:
        return Settings(
            composio=ComposioSettings(
                api_key=os.getenv("COMPOSIO_API_KEY", "")
            ),
            gmail=GmailSettings(
                user_id=os.getenv("GMAIL_USER_ID", ""),
                account_id=os.getenv("GMAIL_ACCOUNT_ID", ""),
                auth_config_id=os.getenv("GMAIL_AUTH_CONFIG_ID", "")
            ),
            linkedin=LinkedInSettings(
                connected_account_id=os.getenv("LINKEDIN_CONNECTED_ACCOUNT_ID", ""),
                entity_id=os.getenv("LINKEDIN_ENTITY_ID", ""),
                auth_token=os.getenv("COMPOSIO_LINKEDIN_AUTH", ""),
                api_enabled=os.getenv("LINKEDIN_API_ENABLED", "false").lower() == "true"
            ),
            google_sheets=GoogleSheetsSettings(
                auth_config_id=os.getenv("GOOGLE_SHEETS_AUTH_CONFIG_ID", ""),
                account_id=os.getenv("GOOGLE_SHEETS_ACCOUNT_ID", ""),
                user_id=os.getenv("GOOGLE_SHEETS_USER_ID", os.getenv("GMAIL_USER_ID", ""))
            ),
            google_calendar=GoogleCalendarSettings(
                account_id=os.getenv("GOOGLE_CALENDAR_ACCOUNT_ID", ""),
                user_id=os.getenv("GOOGLE_CALENDAR_USER_ID", os.getenv("GMAIL_USER_ID", "")),
                auth_config_id=os.getenv("GOOGLE_CALENDAR_AUTH_CONFIG_ID", "")
            ),
            llm=LLMSettings(
                groq_api_key=os.getenv("GROQ_API_KEY", ""),
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                primary_model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
                backup_model=os.getenv("GROQ_MODEL_BACKUP", "llama-3.1-70b-versatile"),
                alternative_model=os.getenv("GROQ_MODEL_ALTERNATIVE", "meta-llama/llama-4-scout-17b-16e-instruct")
            ),
            debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "30"))
        )
    except Exception as e:
        raise ValueError(
            f"Configuration error: {str(e)}\n"
            "Please ensure all required environment variables are set in .env file.\n"
            "Copy .env.example to .env and fill in your credentials."
        )


# Convenience function for backward compatibility
def validate_config() -> bool:
    """
    Validate configuration and return True if valid.
    
    Returns:
        bool: True if configuration is valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    try:
        get_settings()
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False
