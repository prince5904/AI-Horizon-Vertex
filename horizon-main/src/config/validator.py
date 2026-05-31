#!/usr/bin/env python3
"""
Configuration Validation Script
Checks if all environment variables are properly loaded
"""

try:
    from .legacy_config import validate_config, COMPOSIO_API_KEY, GROQ_API_KEY
    
    print("🔧 Validating AI Recruiter Configuration...")
    print("=" * 50)
    
    # Test configuration loading
    validate_config()
    
    # Check if keys are loaded (without printing them)
    composio_status = "✅ Loaded" if COMPOSIO_API_KEY and COMPOSIO_API_KEY != "your_composio_api_key_here" else "❌ Missing/Default"
    groq_status = "✅ Loaded" if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here" else "❌ Missing/Default"
    
    print(f"COMPOSIO_API_KEY: {composio_status}")
    print(f"GROQ_API_KEY: {groq_status}")
    
    print("\n🎉 Configuration validation complete!")
    print("📚 Run 'python ultimate_ai_recruiter_pipeline.py' to start processing candidates")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you've installed requirements: pip install -r requirements_minimal.txt")
    
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    print("💡 Please check your .env file configuration")
    
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    print("💡 Please check your setup and try again")