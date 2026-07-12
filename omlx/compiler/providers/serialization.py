import json
from typing import Dict, Any
from .capability import (
    ProviderCapability, OperatorCapability, QuantizationCapability,
    PlatformConstraints, AdapterRequirements, SupportLevel, QuantizationSupport
)

class ProviderSerializer:
    @staticmethod
    def to_dict(capability: ProviderCapability) -> Dict[str, Any]:
        return {
            "provider": capability.provider,
            "version": capability.version,
            "architectures": capability.architectures,
            "operators": {
                k: {
                    "support": v.support.value,
                    "implementation_notes": v.implementation_notes
                } for k, v in capability.operators.items()
            },
            "tensor_layouts": capability.tensor_layouts,
            "quantization": {
                k: {
                    "support": v.support.value,
                    "implementation_notes": v.implementation_notes
                } for k, v in capability.quantization.items()
            },
            "execution_modes": capability.execution_modes,
            "capabilities": capability.capabilities,
            "platform_constraints": {
                "apple_silicon_only": capability.platform_constraints.apple_silicon_only,
                "cuda_required": capability.platform_constraints.cuda_required,
                "cpu_only": capability.platform_constraints.cpu_only,
                "metal_required": capability.platform_constraints.metal_required,
                "linux_only": capability.platform_constraints.linux_only,
                "windows_supported": capability.platform_constraints.windows_supported
            },
            "adapter_requirements": {
                "needs_tensor_conversion": capability.adapter_requirements.needs_tensor_conversion,
                "needs_weight_conversion": capability.adapter_requirements.needs_weight_conversion,
                "needs_tokenizer_adapter": capability.adapter_requirements.needs_tokenizer_adapter,
                "needs_sampling_adapter": capability.adapter_requirements.needs_sampling_adapter,
                "needs_scheduler_adapter": capability.adapter_requirements.needs_scheduler_adapter
            }
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> ProviderCapability:
        operators = {
            k: OperatorCapability(
                support=SupportLevel(v["support"]),
                implementation_notes=v.get("implementation_notes")
            ) for k, v in data.get("operators", {}).items()
        }
        quantization = {
            k: QuantizationCapability(
                support=QuantizationSupport(v["support"]),
                implementation_notes=v.get("implementation_notes")
            ) for k, v in data.get("quantization", {}).items()
        }
        platform_data = data.get("platform_constraints", {})
        platform_constraints = PlatformConstraints(
            apple_silicon_only=platform_data.get("apple_silicon_only", False),
            cuda_required=platform_data.get("cuda_required", False),
            cpu_only=platform_data.get("cpu_only", False),
            metal_required=platform_data.get("metal_required", False),
            linux_only=platform_data.get("linux_only", False),
            windows_supported=platform_data.get("windows_supported", True)
        )
        adapter_data = data.get("adapter_requirements", {})
        adapter_requirements = AdapterRequirements(
            needs_tensor_conversion=adapter_data.get("needs_tensor_conversion", False),
            needs_weight_conversion=adapter_data.get("needs_weight_conversion", False),
            needs_tokenizer_adapter=adapter_data.get("needs_tokenizer_adapter", False),
            needs_sampling_adapter=adapter_data.get("needs_sampling_adapter", False),
            needs_scheduler_adapter=adapter_data.get("needs_scheduler_adapter", False)
        )

        return ProviderCapability(
            provider=data["provider"],
            version=data["version"],
            architectures=data.get("architectures", []),
            operators=operators,
            tensor_layouts=data.get("tensor_layouts", []),
            quantization=quantization,
            execution_modes=data.get("execution_modes", []),
            capabilities=data.get("capabilities", []),
            platform_constraints=platform_constraints,
            adapter_requirements=adapter_requirements
        )

    @staticmethod
    def to_json(capability: ProviderCapability) -> str:
        return json.dumps(ProviderSerializer.to_dict(capability), indent=2)

    @staticmethod
    def from_json(json_str: str) -> ProviderCapability:
        return ProviderSerializer.from_dict(json.loads(json_str))
