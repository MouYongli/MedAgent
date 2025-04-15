from typing import Dict, Any

from app.models.components.AbstractComponent import AbstractComponent

from app.models.chat import Chat, MessageType, ConversationMessage


class StartComponent(AbstractComponent, variant_name="start"):
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        chat = AbstractComponent.resolve_data_path("chat", data)
        if not isinstance(chat, Chat):
            raise TypeError(f"Chat object must be of type 'Chat', but is {type(chat)}")

        data[self.id] = {"chat": chat}

        if not chat.messages:
            raise ValueError("Chat history is empty, expected at least one message")
        last_message: ConversationMessage = chat.messages[-1]
        if last_message.messageType != MessageType.QUESTION:
            raise ValueError("Last message must be of type QUESTION")

        data[self.id]["current_user_input"] = last_message.content

        return data

    @classmethod
    def get_input_spec(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "chat": {
                "type": "Chat",
                "description": "Chat instance holding message history and system reference"
            }
        }

    @classmethod
    def get_output_spec(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "start.chat": {
                "type": "Chat",
                "description": "Reference to the chat object under the 'start' namespace (or whatever the id of the component is)"
            },
            "start.current_user_input": {
                "type": "string",
                "description": "Content of the last user message (must be of type QUESTION) under the 'start' namespace (or whatever the id of the component is)"
            }
        }

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {}
