from uuid import uuid4

class Conversation:
    def __init__(self):
        self.id = str(uuid4())
        self.messages = []
        self.response_count = 0

    def add_message(self, sender: str, content: str):
        self.messages.append({'sender': sender, 'content': content})

    def get_response(self):
        self.response_count += 1
        return f"This is answer #{self.response_count}"
