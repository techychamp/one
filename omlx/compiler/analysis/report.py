# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any
import json
import dataclasses

@dataclass(frozen=True)
class CapabilityReport:
    """Immutable capability report."""
    architecture: str
    capabilities: MappingProxyType[str, bool] = field(default_factory=lambda: MappingProxyType({}))
    features: MappingProxyType[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    requirements: tuple[str, ...] = field(default_factory=tuple)
    constraints: MappingProxyType[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    unsupported: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self):
        if not isinstance(self.capabilities, MappingProxyType):
            object.__setattr__(self, 'capabilities', MappingProxyType(self.capabilities))
        if not isinstance(self.features, MappingProxyType):
            object.__setattr__(self, 'features', MappingProxyType(self.features))
        if not isinstance(self.requirements, tuple):
            object.__setattr__(self, 'requirements', tuple(self.requirements))
        if not isinstance(self.constraints, MappingProxyType):
            object.__setattr__(self, 'constraints', MappingProxyType(self.constraints))
        if not isinstance(self.unsupported, tuple):
            object.__setattr__(self, 'unsupported', tuple(self.unsupported))

    def to_dict(self) -> dict[str, Any]:
        return {
            "architecture": self.architecture,
            "capabilities": dict(self.capabilities),
            "features": dict(self.features),
            "requirements": list(self.requirements),
            "constraints": dict(self.constraints),
            "unsupported": list(self.unsupported)
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CapabilityReport":
        return cls(
            architecture=data["architecture"],
            capabilities=MappingProxyType(data.get("capabilities", {})),
            features=MappingProxyType(data.get("features", {})),
            requirements=tuple(data.get("requirements", [])),
            constraints=MappingProxyType(data.get("constraints", {})),
            unsupported=tuple(data.get("unsupported", []))
        )
