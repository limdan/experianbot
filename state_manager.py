# --- State Management ---
# In a real application, you might use a database (e.g., Firestore) to store
# conversation state for persistence across bot restarts or for more complex flows.

class StateManager:
    """
    Manages the conversation state for each user.
    Currently uses an in-memory dictionary.
    """
    def __init__(self):
        self.user_states = {} # {user_id: {'step': 'initial', 'data': {}}}

    def get_state(self, user_id: int) -> dict:
        """Retrieves the current state for a given user."""
        return self.user_states.get(user_id, {'step': 'initial', 'data': {}})

    def set_state(self, user_id: int, step: str, data: dict = None): # type: ignore
        """Sets or updates the state for a given user."""
        if user_id not in self.user_states:
            self.user_states[user_id] = {'step': step, 'data': {}}
        else:
            self.user_states[user_id]['step'] = step
            if data:
                self.user_states[user_id]['data'].update(data)
            
    def update_data(self, user_id: int, key: str, value: any): # type: ignore
        """Updates a specific piece of data within the user's current state."""
        if user_id in self.user_states:
            self.user_states[user_id]['data'][key] = value
        else:
            # Initialize state if it doesn't exist
            self.user_states[user_id] = {'step': 'initial', 'data': {key: value}}

    def clear_state(self, user_id: int):
        """Clears the state for a given user."""
        self.user_states.pop(user_id, None)
