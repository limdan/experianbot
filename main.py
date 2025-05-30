import asyncio
import logging
from telethon import TelegramClient

# Import configurations and modules
from config import (
    TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN,
    get_secret, SERVICE_TELEGRAM_API_ID, SERVICE_TELEGRAM_API_HASH, SERVICE_TELEGRAM_BOT_TOKEN
)
from state_manager import StateManager
from telegram_bot import TelegramBot

logger = logging.getLogger(__name__)

async def main():
    """
    Main function to initialize and run the Telegram bot.
    """
    # Attempt to retrieve Telegram credentials from keyring first
    telegram_api_id = get_secret(SERVICE_TELEGRAM_API_ID) or TELEGRAM_API_ID
    telegram_api_hash = get_secret(SERVICE_TELEGRAM_API_HASH) or TELEGRAM_API_HASH
    telegram_bot_token = get_secret(SERVICE_TELEGRAM_BOT_TOKEN) or TELEGRAM_BOT_TOKEN

    # Ensure at least one source (keyring or environment variable) provides credentials
    if not all([telegram_api_id, telegram_api_hash, telegram_bot_token]):
        logger.error("ERROR: Telegram API credentials (API ID, API Hash, Bot Token) are not configured.")
        logger.error("Please set them either as environment variables or in your system's keyring using set_secrets.py.")
        exit(1)

    # Initialize Telegram Client
    # 'bot_session' is the session name, change if you need multiple bot sessions
    client = TelegramClient('bot_session', telegram_api_id, telegram_api_hash)  # type: ignore

    # Initialize State Manager
    state_manager = StateManager()

    # Initialize Telegram Bot with the client and state manager
    bot = TelegramBot(client, state_manager)

    # Start the Telegram client
    try:
        logger.info("Starting Telegram bot client...")
        await client.start(bot_token=telegram_bot_token) # type: ignore
        logger.info("Telegram bot client started successfully.")
        print("Bot is running. Send /start to your bot.")
        await client.run_until_disconnected() # type: ignore
    except Exception as e:
        logger.critical(f"An error occurred while starting or running the bot: {e}")
        print(f"An error occurred: {e}")
    finally:
        if client.is_connected():
            logger.info("Disconnecting Telegram client.")
            await client.disconnect() # type: ignore

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt).")
        print("Bot stopped by user.")
    except Exception as e:
        logger.critical(f"An unhandled error occurred in main execution: {e}")
        print(f"An unhandled error occurred: {e}")