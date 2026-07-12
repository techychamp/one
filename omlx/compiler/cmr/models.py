from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Set

@dataclass
class CanonicalModelRepresentation:
    architecture: str
    tensor_metadata: Dict[str, Any] = field(default_factory=dict)
    tokenizer_metadata: Dict[str, Any] = field(default_factory=dict)
    vocabulary: Dict[str, int] = field(default_factory=dict)
    quantization_metadata: Dict[str, Any] = field(default_factory=dict)
    capabilities: Set[str] = field(default_factory=set)
    special_tokens: Dict[str, int] = field(default_factory=dict)
    multimodal_metadata: Dict[str, Any] = field(default_factory=dict)
    generation_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['capabilities'] = list(self.capabilities)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CanonicalModelRepresentation':
        if 'capabilities' in data:
            data['capabilities'] = set(data['capabilities'])
        return cls(**data)
