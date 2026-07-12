from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

class SupportLevel(Enum):
    SUPPORTED = "supported"
    PARTIAL = "partial"
    UNSUPPORTED = "unsupported"

class QuantizationSupport(Enum):
    NATIVE = "native"
    ADAPTER = "adapter"
    UNSUPPORTED = "unsupported"

@dataclass(frozen=True)
class OperatorCapability:
    support: SupportLevel
    implementation_notes: Optional[str] = None

@dataclass(frozen=True)
class QuantizationCapability:
    support: QuantizationSupport
    implementation_notes: Optional[str] = None

@dataclass(frozen=True)
class PlatformConstraints:
    apple_silicon_only: bool = False
    cuda_required: bool = False
    cpu_only: bool = False
    metal_required: bool = False
    linux_only: bool = False
    windows_supported: bool = True

@dataclass(frozen=True)
class AdapterRequirements:
    needs_tensor_conversion: bool = False
    needs_weight_conversion: bool = False
    needs_tokenizer_adapter: bool = False
    needs_sampling_adapter: bool = False
    needs_scheduler_adapter: bool = False

@dataclass(frozen=True)
class ProviderCapability:
    provider: str
    version: str
    architectures: List[str] = field(default_factory=list)
    operators: Dict[str, OperatorCapability] = field(default_factory=dict)
    tensor_layouts: List[str] = field(default_factory=list)
    quantization: Dict[str, QuantizationCapability] = field(default_factory=dict)
    execution_modes: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    platform_constraints: PlatformConstraints = field(default_factory=PlatformConstraints)
    adapter_requirements: AdapterRequirements = field(default_factory=AdapterRequirements)
