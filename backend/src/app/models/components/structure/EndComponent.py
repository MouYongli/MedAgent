from typing import Dict, Any
from app.models.components.AbstractComponent import AbstractComponent


class EndComponent(AbstractComponent, variant_name="end"):
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"response": data.get("response", "")}

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {}
