from typing import Dict, Any
from app.models.components.AbstractComponent import AbstractComponent


class StartComponent(AbstractComponent, variant_name="start"):
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return data  # Pass through chat or any other init data

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {}
