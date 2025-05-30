import os
import logging
import keyring # Import keyring

# --- Configuration ---
# Get your API ID and API Hash from my.telegram.org
# Get your bot token from BotFather on Telegram (start a chat with @BotFather)
# These can still be environment variables or fetched via keyring if preferred.
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Define service names for keyring storage
# It's recommended to use distinct service names for different credentials
SERVICE_TELEGRAM_API_ID = 'telegram_bot_api_id'
SERVICE_TELEGRAM_API_HASH = 'telegram_bot_api_hash'
SERVICE_TELEGRAM_BOT_TOKEN = 'telegram_bot_token'

SERVICE_EXPERIAN_API_BASE_URL = 'experian_api_base_url'
SERVICE_EXPERIAN_CLIENT_ID = 'experian_client_id'
SERVICE_EXPERIAN_CLIENT_SECRET = 'experian_client_secret'
SERVICE_EXPERIAN_USERNAME = 'experian_username'
SERVICE_EXPERIAN_PASSWORD = 'experian_password'

# Default base URL for Experian API if not found in keyring
DEFAULT_EXPERIAN_API_BASE_URL = 'https://api.experian.com/credit-risk/v1'

# --- Logging Setup ---
# Configure logging for the entire application
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO) # Set to INFO for more detailed bot logs

def get_secret(service_id: str, username: str = 'default_user') -> str | None:
    """
    Retrieves a secret from the keyring.
    """
    try:
        secret = keyring.get_password(service_id, username)
        if secret:
            logging.info(f"Secret for service '{service_id}' retrieved successfully.")  # Do not log the secret itself
        else:
            logging.warning(f"Secret for service '{service_id}' not found in keyring.")
        return secret
    except Exception as e:
        logging.error(f"Error retrieving secret for service '{service_id}' from keyring: {e}")
        return None

def set_secret(service_id: str, secret: str, username: str = 'default_user'):
    """
    Sets a secret in the keyring.
    """
    try:
        keyring.set_password(service_id, username, secret)
        logging.info(f"Secret for service '{service_id}' set successfully.")  # Do not log the secret itself
    except Exception as e:
        logging.error(f"Error setting secret for service '{service_id}' in keyring: {e}")