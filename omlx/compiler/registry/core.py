from typing import Any, Callable, Dict, Type

class Registry:
    def __init__(self, name: str):
        self.name = name
        self._registry: Dict[str, Any] = {}

    def register(self, name: str, item: Any = None) -> Callable:
        def decorator(obj: Any) -> Any:
            if name in self._registry:
                raise ValueError(f"Cannot register '{name}' in {self.name} registry; it already exists.")
            self._registry[name] = obj
            return obj

        if item is not None:
            return decorator(item)
        return decorator

    def get(self, name: str) -> Any:
        if name not in self._registry:
            raise KeyError(f"'{name}' not found in {self.name} registry.")
        return self._registry[name]

    def has(self, name: str) -> bool:
        return name in self._registry

    def list_all(self) -> Dict[str, Any]:
        return self._registry.copy()

architecture_registry = Registry("architecture")
operator_registry = Registry("operator")
quantization_registry = Registry("quantization")
tokenizer_registry = Registry("tokenizer")
capability_registry = Registry("capability")
