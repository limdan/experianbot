# 🛡️ ExperianBot

A secure and user-friendly Telegram bot that connects to the Experian API to perform credit health checks for clients.

---

## ✨ Features

- **🔐 Secure Secrets Management:** Uses your system keyring to store API credentials safely.
- **📁 Environment-Based Configuration:** Loads configuration from a `.env` file (never committed to version control).
- **🔗 Experian API Integration:** Communicates with Experian's Credit Risk API.
- **💬 Telegram Bot Interface:** Allows clients to interact via Telegram for real-time credit inquiries.

---

## ⚙️ Setup Guide

### 1. 📥 Clone the Repository

```sh
git clone https://github.com/yourusername/experianbot.git
cd experianbot/experianbot
```

### 2. 🧾 Create a `.env` File

In the root of the project directory, create a `.env` file with the following content:

```ini
# Telegram Credentials
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Experian API Credentials
EXPERIAN_API_BASE_URL=https://api.experian.com/credit-risk/v1
EXPERIAN_CLIENT_ID=your_experian_client_id
EXPERIAN_CLIENT_SECRET=your_experian_client_secret
EXPERIAN_USERNAME=your_experian_username
EXPERIAN_PASSWORD=your_experian_password
```

> ⚠️ **Do not commit `.env` to source control — it's excluded via `.gitignore` for security.**

### 3. 📦 Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. 🔐 Store Secrets in Keyring

```sh
python set_secrets.py
```

This script will load your credentials from `.env` and securely store them in your system keyring.

### 5. 🚀 Run the Bot

```sh
python main.py
```

---

## 📁 Project Structure

```
experianbot/
├── config.py         # Handles configuration and secret retrieval
├── main.py           # Telegram bot logic
├── set_secrets.py    # Loads .env and stores credentials in keyring
├── requirements.txt  # Python dependencies
├── .env              # Local environment config (excluded from Git)
└── README.md         # Project documentation
```

---

## 🔒 Security Best Practices

- **No secrets in codebase:** All credentials are loaded from `.env` and stored in your system keyring.
- **.env is git-ignored:** Your secrets are never committed to version control.
- **Follows best practices:** Secure handling of bot and API credentials.

---

## 📄 License

This project is licensed under the MIT License.

---

## 📝 Notes

- Ensure you have valid access to the Experian API.
- Replace all placeholder values in `.env` with your actual credentials.
- For any issues, please open an issue or pull request on GitHub.

---