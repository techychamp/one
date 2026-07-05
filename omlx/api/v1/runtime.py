from typing import Any, Dict
from pydantic import BaseModel, Field
import asyncio
from omlx.runtime.builder import RuntimeBuilder as InternalRuntimeBuilder
from omlx.runtime.feature_flags import FeatureFlags

class RuntimeConfig(BaseModel, frozen=True):
    settings: Dict[str, Any] = Field(default_factory=dict)
    feature_flags: Dict[str, bool] = Field(default_factory=dict)

class RuntimeService:
    def __init__(self, internal_runtime):
        self._internal = internal_runtime

    @property
    def status(self) -> str:
        if hasattr(self._internal, 'state') and hasattr(self._internal.state, 'value'):
            return self._internal.state.value
        return "unknown"

class RuntimeBuilder:
    def __init__(self):
        self._settings = {}
        self._feature_flags = {}
        self._internal_builder = InternalRuntimeBuilder()

    def configure(self, settings: Dict[str, Any]) -> 'RuntimeBuilder':
        self._settings.update(settings)
        self._internal_builder.with_settings(self._settings)
        return self

    def enable(self, feature: str) -> 'RuntimeBuilder':
        self._feature_flags[feature] = True
        return self

    def disable(self, feature: str) -> 'RuntimeBuilder':
        self._feature_flags[feature] = False
        return self

    def build(self) -> RuntimeService:
        ff = FeatureFlags.from_env()
        self._internal_builder.with_feature_flags(ff)
        internal_runtime = self._internal_builder.build()
        return RuntimeService(internal_runtime)
