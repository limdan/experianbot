import logging
from telethon import events, Button
from state_manager import StateManager
from experian_api import call_experian_credit_risk_api

logger = logging.getLogger(__name__)

class TelegramBot:
    """
    Handles Telegram bot interactions and manages conversation flow.
    """
    def __init__(self, client, state_manager: StateManager):
        self.client = client
        self.state_manager = state_manager
        self._register_handlers()

    def _register_handlers(self):
        """Registers all event handlers for the Telegram bot."""
        self.client.add_event_handler(self.start_handler, events.NewMessage(pattern='/start'))
        self.client.add_event_handler(self.check_credit_start, events.NewMessage(pattern='/check_credit'))
        self.client.add_event_handler(self.handle_user_input, events.NewMessage)
        self.client.add_event_handler(self.handle_callback_query, events.CallbackQuery)

    async def start_handler(self, event):
        """Handles the /start command."""
        user_id = event.sender_id
        self.state_manager.set_state(user_id, 'initial')
        await event.respond(
            "Hello! I can help you check credit risk data via Experian. "
            "**Please be aware:** This process involves collecting sensitive personal information "
            "which will be sent to Experian for analysis. By proceeding, you consent to this. "
            "\n\nTo begin, type /check_credit."
        )
        logger.info(f"User {user_id} started the bot.")

    async def check_credit_start(self, event):
        """Initiates the credit check process."""
        user_id = event.sender_id
        self.state_manager.set_state(user_id, 'ask_first_name')
        await event.respond("Okay, let's start the credit check. What is your **first name**?")
        logger.info(f"User {user_id} initiated credit check.")

    async def handle_user_input(self, event):
        """Handles subsequent user input based on the current conversation state."""
        user_id = event.sender_id
        current_state = self.state_manager.get_state(user_id)

        if not current_state or event.text.startswith('/'): # Ignore commands if not in a specific flow
            return

        step = current_state['step']
        user_input = event.text

        if step == 'ask_first_name':
            self.state_manager.update_data(user_id, 'first_name', user_input)
            self.state_manager.set_state(user_id, 'ask_last_name')
            await event.respond("Thanks! What is your **last name**?")
        elif step == 'ask_last_name':
            self.state_manager.update_data(user_id, 'last_name', user_input)
            self.state_manager.set_state(user_id, 'ask_address')
            await event.respond("Please provide your **street address** (e.g., 123 Main St).")
        elif step == 'ask_address':
            self.state_manager.update_data(user_id, 'address', user_input)
            self.state_manager.set_state(user_id, 'ask_city')
            await event.respond("What is your **city**?")
        elif step == 'ask_city':
            self.state_manager.update_data(user_id, 'city', user_input)
            self.state_manager.set_state(user_id, 'ask_state')
            await event.respond("What is your **state/province** (e.g., CA, NY)?")
        elif step == 'ask_state':
            self.state_manager.update_data(user_id, 'state', user_input)
            self.state_manager.set_state(user_id, 'ask_zip_code')
            await event.respond("What is your **zip/postal code**?")
        elif step == 'ask_zip_code':
            self.state_manager.update_data(user_id, 'zip_code', user_input)
            self.state_manager.set_state(user_id, 'ask_dob')
            await event.respond("What is your **date of birth** (YYYY-MM-DD)?")
        elif step == 'ask_dob':
            self.state_manager.update_data(user_id, 'dob', user_input)
            self.state_manager.set_state(user_id, 'ask_ssn_consent')
            # Crucial: Ask for SSN consent and explain its sensitivity
            await event.respond(
                "To get the most accurate credit risk data, we typically need your **Social Security Number (SSN)**. "
                "**WARNING:** Providing your SSN is highly sensitive. It will be transmitted securely to Experian. "
                "We do not store your SSN. "
                "Do you consent to provide your SSN? (Yes/No)",
                buttons=[
                    [Button.inline("Yes, provide SSN", b'consent_ssn_yes')],
                    [Button.inline("No, skip SSN", b'consent_ssn_no')]
                ]
            )
        elif step == 'ask_ssn':
            self.state_manager.update_data(user_id, 'ssn', user_input)
            await self._process_experian_request(event, user_id)
        else:
            # Fallback for unhandled states or if user types something unexpected
            await event.respond("I'm not sure what you mean. Please use /start or /check_credit to begin.")
            self.state_manager.clear_state(user_id) # Clear state
            logger.warning(f"User {user_id} entered unexpected input in step {step}: {user_input}")

    async def handle_callback_query(self, event):
        """Handles button clicks for consent."""
        user_id = event.sender_id
        current_state = self.state_manager.get_state(user_id)

        if not current_state or current_state['step'] != 'ask_ssn_consent':
            await event.answer("This action is no longer valid or you are not in the correct step.", alert=True)
            logger.warning(f"User {user_id} clicked invalid button in step {current_state.get('step') if current_state else 'N/A'}.")
            return

        data = event.data.decode('utf-8')

        if data == 'consent_ssn_yes':
            self.state_manager.set_state(user_id, 'ask_ssn')
            await event.edit("Please enter your **Social Security Number (SSN)**. (e.g., XXX-XX-XXXX).")
            logger.info(f"User {user_id} consented to provide SSN.")
        elif data == 'consent_ssn_no':
            self.state_manager.update_data(user_id, 'ssn', None) # Explicitly set to None
            await event.edit("You chose not to provide your SSN. Proceeding without it.")
            logger.info(f"User {user_id} skipped providing SSN.")
            await self._process_experian_request(event, user_id)

        await event.answer() # Dismiss the loading indicator on the button

    async def _process_experian_request(self, event, user_id):
        """
        Sends the collected data to Experian API and responds to the user.
        """
        await event.respond("Thank you for the information. I'm now processing your request with Experian. This may take a moment...")

        customer_data = self.state_manager.get_state(user_id)['data']
        logger.info(f"Collected data for Experian API call for user {user_id}: {customer_data}")

        experian_response = await call_experian_credit_risk_api(customer_data)

        if experian_response and not experian_response.get('error'):
            # --- Process Experian Response ---
            # This part is highly dependent on the actual Experian API response structure.
            # You'll need to parse the JSON and extract relevant information.
            # For demonstration, we'll just show a simplified mock response.

            mock_credit_score = experian_response.get('creditScore', 'N/A')
            mock_risk_level = experian_response.get('riskLevel', 'Unknown')
            mock_summary = experian_response.get('summary', 'No detailed summary available.')

            response_message = (
                "Here is the credit risk data from Experian:\n\n"
                f"**Credit Score:** {mock_credit_score}\n"
                f"**Risk Level:** {mock_risk_level}\n"
                f"**Summary:** {mock_summary}\n\n"
                "*(This data is for informational purposes only and not financial advice.)*"
            )
            logger.info(f"Successfully processed Experian response for user {user_id}.")
        else:
            error_message = experian_response.get('error', 'An unknown error occurred.')
            response_message = (
                f"I encountered an error while retrieving data from Experian: {error_message}\n"
                "Please try again later or contact support if the issue persists."
            )
            logger.error(f"Experian API call failed for user {user_id}: {error_message}")

        await event.respond(response_message)
        self.state_manager.clear_state(user_id) # Clear user state after completion

