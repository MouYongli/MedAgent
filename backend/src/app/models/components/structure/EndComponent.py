import logging
from typing import Dict, Any

from app.models.components.AbstractComponent import AbstractComponent
from app.utils.helper import render_template

logging.basicConfig(level=logging.INFO)


class EndComponent(AbstractComponent, variant_name="end"):
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        generation_key = self.parameters.get("generation_key", "")
        if not generation_key:
            raise ValueError("EndComponent requires a 'generation_key' parameter to know what to return.")
        final_value = render_template(generation_key, data)
        data[f"{self.id}.response"] = final_value

        retrieval_key = self.parameters.get("retrieval_key", "")
        if not retrieval_key:
            logging.info(f"EndComponent has no configured 'retrieval_key', so no return value to be expected")
            data[f"{self.id}.retrieval"] = None
        else:
            retrieval_value = render_template(retrieval_key, data)
            data[f"{self.id}.retrieval"] = retrieval_value
        return data

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "generation_key": {
                "type": "string",
                "description": "Path in the data dict to return as the final generation result (e.g., 'default_gen.response')"
            },
            "retrieval_key": {
                "type": "string",
                "description": "Path in the data dict to return as the retrieved entities, OPTIONAL!"
            }
        }

    @classmethod
    def get_output_spec(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "end.response": {
                "type": "Any",
                "description": "The final value extracted using 'generation_key', stored under this component's name"
            },
            "end.retrieval": {
                "type": "Any",
                "description": "Forwards the retrieval result as specified in 'retrieval key'. Just like the key, this output is optional!"
            }
        }
