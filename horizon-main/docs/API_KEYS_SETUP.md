# 🔑 API Keys Setup Guide

## For Local Development

Your API keys should go in the `.env` file in the root directory.

### Current Setup:

The `.env` file should contain your API keys:

```bash
# Core API Keys
COMPOSIO_API_KEY=your_composio_api_key
GROQ_API_KEY=your_groq_api_key

# Gmail Configuration
GMAIL_USER_ID=your_gmail_entity_id
GMAIL_ACCOUNT_ID=your_gmail_account_id
GMAIL_AUTH_CONFIG_ID=your_gmail_auth_config

# ... and all other credentials (see .env.example)
```

### Test Your Setup:

```bash
# Activate virtual environment
.\comp\Scripts\Activate.ps1  # Windows
# source comp/bin/activate    # macOS/Linux

# Test configuration
python scripts/validate_config.py

# Test full pipeline
python ai_recruiter_pipeline.py
```

### Security Notes:

1. ✅ **`.env` file is in `.gitignore`** - Won't be committed to GitHub
2. ✅ **All credentials loaded from environment variables** - No hardcoded keys in code
3. ✅ **`.env.example` template provided** - For other developers to copy

### For New Users:

If someone else wants to use this project:

1. Copy `.env.example` to `.env`
2. Replace placeholder values with their own API keys
3. Get credentials from:
   - **Composio**: https://app.composio.dev/settings
   - **Groq**: https://console.groq.com/keys
   - **Gmail/Calendar/Sheets/LinkedIn**: Connect in Composio Dashboard

### File Structure:

```
📁 Project Root
├── .env                       # ← Your REAL API keys go here (LOCAL ONLY)
├── .env.example               # ← Template for others
├── src/config/
│   ├── settings.py            # ← Pydantic models (type-safe)
│   ├── legacy_config.py       # ← Loads from .env
│   └── validator.py           # ← Validates configuration
├── scripts/
│   └── validate_config.py     # ← Test your configuration
└── .gitignore                 # ← Protects .env from being committed
```

## 🚀 You're All Set!

Your local environment is ready to run with all the API keys configured securely.