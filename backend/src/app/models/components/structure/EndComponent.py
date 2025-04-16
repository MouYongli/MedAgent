import logging
import re
from typing import Dict, Any
from app.models.components.AbstractComponent import AbstractComponent

logging.basicConfig(level=logging.INFO)

class EndComponent(AbstractComponent, variant_name="end"):
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return_key = self.parameters.get("return_key", "")
        if not return_key:
            raise ValueError("EndComponent requires a 'return_key' parameter to know what to return.")

        final_value = AbstractComponent.resolve_template(return_key, data)

        data[f"{self.id}.response"] = final_value
        return data

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "return_key": {
                "type": "string",
                "description": "Path in the data dict to return as the final result (e.g., 'default_gen.response')"
            }
        }

    @classmethod
    def get_output_spec(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "end.response": {
                "type": "Any",
                "description": "The final value extracted using 'return_key', stored under this component's name"
            }
        }
