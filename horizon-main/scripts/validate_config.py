import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.legacy_config import validate_config, COMPOSIO_API_KEY, GROQ_API_KEY

print("Validating Configuration...")
validate_config()

composio_ok = COMPOSIO_API_KEY and COMPOSIO_API_KEY != "your_composio_api_key_here"
groq_ok = GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here"

print(f"COMPOSIO_API_KEY: {'OK' if composio_ok else 'MISSING'}")
print(f"GROQ_API_KEY: {'OK' if groq_ok else 'MISSING'}")
print("Configuration valid!" if (composio_ok and groq_ok) else "Please check .env file")
