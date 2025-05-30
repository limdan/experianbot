# experianbot

A Telegram bot that connects to the Experian API to serve clients for credit health checking.

## Features

- Securely stores and retrieves API credentials using system keyring
- Loads secrets from a `.env` file (never commit this file)
- Integrates with Experian API for credit health checks
- Telegram bot interface for user interaction

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/experianbot.git
cd experianbot/experianbot
```

### 2. Create a `.env` File

Create a `.env` file in the project directory with the following content:

```
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
EXPERIAN_API_BASE_URL=https://api.experian.com/credit-risk/v1
EXPERIAN_CLIENT_ID=your_experian_client_id
EXPERIAN_CLIENT_SECRET=your_experian_client_secret
EXPERIAN_USERNAME=your_experian_username
EXPERIAN_PASSWORD=your_experian_password
```

**Never commit your `.env` file. It is ignored by `.gitignore`.**

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Store Secrets in Keyring

Run the following command to load secrets from `.env` and store them securely in your system keyring:

```sh
python set_secrets.py
```

### 5. Run the Bot

```sh
python main.py
```

## Project Structure

```
experianbot/
├── config.py
├── main.py
├── set_secrets.py
├── requirements.txt
├── .env
└── README.md
```

## Security

- Secrets are never stored in code or committed to git.
- All credentials are loaded from `.env` and stored in your system keyring.

## License

MIT License

---

**Note:**  
Replace placeholder values in `.env` with your actual credentials.
