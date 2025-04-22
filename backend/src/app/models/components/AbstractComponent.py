from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
import copy


class AbstractComponent(ABC):
    variants: Dict[str, Type['AbstractComponent']] = {}
    default_parameters: Dict[str, Any] = {}

    def __new__(cls, name: str, inputs: Dict[str, Any], outputs: Dict[str, Any],
                parameters: Optional[Dict[str, Any]] = None, variant: Optional[str] = None) -> 'AbstractComponent':
        if variant:
            if variant not in cls.variants:
                raise ValueError(f"Variant '{variant}' is not registered for component '{cls.__name__}'")
            subclass = cls.variants[variant]
            instance = super(AbstractComponent, subclass).__new__(subclass)
        else:
            if cls.variants:
                raise ValueError(
                    f"Component '{cls.__name__}' requires a variant. Available: {list(cls.variants.keys())}"
                )
            instance = super().__new__(cls)
        return instance

    def __init__(self, name: str, inputs: Dict[str, Any], outputs: Dict[str, Any],
                 parameters: Optional[Dict[str, Any]] = None, variant: Optional[str] = None):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self._variant = variant or "base"

        merged_params = copy.deepcopy(self.default_parameters)
        if parameters:
            merged_params.update(parameters)
        self.parameters = merged_params

    @classmethod
    def register_variant(cls, name: str, variant_cls: Type['AbstractComponent']):
        cls.variants[name] = variant_cls

    def __init_subclass__(cls, variant_name: Optional[str] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if variant_name:
            AbstractComponent.variants[variant_name] = cls

    @abstractmethod
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "variant": self._variant,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "parameters": self.parameters
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AbstractComponent':
        return cls(
            name=data["name"],
            inputs=data.get("inputs", {}),
            outputs=data.get("outputs", {}),
            parameters=data.get("parameters", {}),
            variant=data.get("variant")
        )

    def get_variant_name(self) -> str:
        return self._variant
