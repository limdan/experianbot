import httpx
import json
import logging
from config import (
    get_secret,
    SERVICE_EXPERIAN_API_BASE_URL,
    SERVICE_EXPERIAN_CLIENT_ID,
    SERVICE_EXPERIAN_CLIENT_SECRET,
    SERVICE_EXPERIAN_USERNAME,
    SERVICE_EXPERIAN_PASSWORD,
    DEFAULT_EXPERIAN_API_BASE_URL
)

logger = logging.getLogger(__name__)

async def get_experian_access_token():
    """
    Retrieves Experian API credentials from keyring and gets an access token.
    """
    # Retrieve credentials from keyring
    experian_api_base_url = get_secret(SERVICE_EXPERIAN_API_BASE_URL) or DEFAULT_EXPERIAN_API_BASE_URL
    experian_client_id = get_secret(SERVICE_EXPERIAN_CLIENT_ID)
    experian_client_secret = get_secret(SERVICE_EXPERIAN_CLIENT_SECRET)
    experian_username = get_secret(SERVICE_EXPERIAN_USERNAME)
    experian_password = get_secret(SERVICE_EXPERIAN_PASSWORD)

    if not all([experian_client_id, experian_client_secret, experian_username, experian_password]):
        logger.error("Experian API credentials are not fully configured in keyring. Cannot get access token.")
        return None

    # Example URL, check Experian docs for the correct authentication endpoint
    auth_url = f"{experian_api_base_url}/oauth2/v1/token"
    payload = {
        "username": experian_username,
        "password": experian_password,
        "client_id": experian_client_id,
        "client_secret": experian_client_secret,
        "grant_type": "password" # Or client_credentials, depending on Experian's setup
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(auth_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            token_data = response.json()
            return token_data.get('access_token')
    except httpx.RequestError as e:
        logger.error(f"Error requesting Experian access token: {e}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from Experian token response: {response.text}") # type: ignore
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during Experian token request: {e}")
        return None

async def call_experian_credit_risk_api(customer_data: dict):
    """
    Placeholder function to call the Experian Credit Risk API.
    This is where you'd send the collected customer_data.
    """
    logger.info(f"Attempting to call Experian API with data: {customer_data}")

    access_token = await get_experian_access_token()
    if not access_token:
        return {"error": "Failed to authenticate with Experian API."}

    # Retrieve base URL from keyring or use default
    experian_api_base_url = get_secret(SERVICE_EXPERIAN_API_BASE_URL) or DEFAULT_EXPERIAN_API_BASE_URL

    # Example endpoint for a consumer credit report (this is a placeholder)
    # You MUST consult Experian's documentation for the correct endpoint and payload.
    credit_report_url = f"{experian_api_base_url}/consumer/credit-report"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Construct the payload based on Experian's API documentation
    # This is a generic example; actual fields will vary.
    experian_payload = {
        "firstName": customer_data.get('first_name'),
        "lastName": customer_data.get('last_name'),
        "address": customer_data.get('address'),
        "city": customer_data.get('city'),
        "state": customer_data.get('state'),
        "zipCode": customer_data.get('zip_code'),
        "dateOfBirth": customer_data.get('dob'), # Format might be 'YYYY-MM-DD'
        "ssn": customer_data.get('ssn') # Handle SSN with extreme care and only if absolutely necessary and legally permissible
    }

    try:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(credit_report_url, json=experian_payload, headers=headers, timeout=30)
            response.raise_for_status() # Raise an exception for HTTP errors
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Error calling Experian Credit Risk API: {e}")
        return {"error": f"Network or API communication error: {e}"}
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from Experian Credit Risk response: {response.text}") # type: ignore
        return {"error": "Invalid response from Experian API."}
    except Exception as e:
        logger.error(f"An unexpected error occurred during Experian API call: {e}")
        return {"error": f"An unexpected error occurred: {e}"}

