from typing import Dict, List, Optional
from .capability import ProviderCapability
import threading

class ProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, ProviderCapability] = {}
        self._lock = threading.RLock()

    def register(self, capability: ProviderCapability) -> None:
        with self._lock:
            self._providers[capability.provider] = capability

    def get_provider(self, name: str) -> Optional[ProviderCapability]:
        with self._lock:
            return self._providers.get(name)

    def get_all_providers(self) -> List[ProviderCapability]:
        with self._lock:
            return list(self._providers.values())

    def get_supported_architectures(self, provider_name: str) -> List[str]:
        with self._lock:
            provider = self._providers.get(provider_name)
            return provider.architectures if provider else []

    def unregister(self, name: str) -> None:
        with self._lock:
            if name in self._providers:
                del self._providers[name]

    def clear(self) -> None:
        with self._lock:
            self._providers.clear()

# Global registry instance
_registry = ProviderRegistry()

def get_registry() -> ProviderRegistry:
    return _registry
