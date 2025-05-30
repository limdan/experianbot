import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# set_secrets.py
import keyring
from dotenv import load_dotenv
import os
from config import (
    SERVICE_TELEGRAM_API_ID, SERVICE_TELEGRAM_API_HASH, SERVICE_TELEGRAM_BOT_TOKEN,
    SERVICE_EXPERIAN_API_BASE_URL, SERVICE_EXPERIAN_CLIENT_ID,
    SERVICE_EXPERIAN_CLIENT_SECRET, SERVICE_EXPERIAN_USERNAME, SERVICE_EXPERIAN_PASSWORD
)

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

EXPERIAN_API_BASE_URL = os.getenv('EXPERIAN_API_BASE_URL')
EXPERIAN_CLIENT_ID = os.getenv('EXPERIAN_CLIENT_ID')
EXPERIAN_CLIENT_SECRET = os.getenv('EXPERIAN_CLIENT_SECRET')
EXPERIAN_USERNAME = os.getenv('EXPERIAN_USERNAME')
EXPERIAN_PASSWORD = os.getenv('EXPERIAN_PASSWORD')

# Set Telegram secrets
keyring.set_password(SERVICE_TELEGRAM_API_ID, 'default_user', TELEGRAM_API_ID) # type: ignore
keyring.set_password(SERVICE_TELEGRAM_API_HASH, 'default_user', TELEGRAM_API_HASH) # type: ignore
keyring.set_password(SERVICE_TELEGRAM_BOT_TOKEN, 'default_user', TELEGRAM_BOT_TOKEN) # type: ignore

# Set Experian secrets
keyring.set_password(SERVICE_EXPERIAN_API_BASE_URL, 'default_user', EXPERIAN_API_BASE_URL) # type: ignore
keyring.set_password(SERVICE_EXPERIAN_CLIENT_ID, 'default_user', EXPERIAN_CLIENT_ID) # type: ignore
keyring.set_password(SERVICE_EXPERIAN_CLIENT_SECRET, 'default_user', EXPERIAN_CLIENT_SECRET) # type: ignore
keyring.set_password(SERVICE_EXPERIAN_USERNAME, 'default_user', EXPERIAN_USERNAME) # type: ignore
keyring.set_password(SERVICE_EXPERIAN_PASSWORD, 'default_user', EXPERIAN_PASSWORD) # type: ignore

print("Secrets have been stored in your system's keyring.")
print("You can now run main.py without setting these as environment variables.")