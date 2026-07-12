import pytest
import json
from omlx.compiler.providers.capability import (
    ProviderCapability, OperatorCapability, QuantizationCapability,
    PlatformConstraints, AdapterRequirements, SupportLevel, QuantizationSupport
)
from omlx.compiler.providers.serialization import ProviderSerializer

def test_serialization_roundtrip():
    op_cap = OperatorCapability(support=SupportLevel.SUPPORTED, implementation_notes="test note")
    quant_cap = QuantizationCapability(support=QuantizationSupport.NATIVE)
    plat_cons = PlatformConstraints(apple_silicon_only=True, metal_required=True)
    adapt_req = AdapterRequirements(needs_weight_conversion=True)

    cap = ProviderCapability(
        provider="test_provider",
        version="1.0",
        architectures=["llama", "mistral"],
        operators={"attention": op_cap},
        tensor_layouts=["row_major"],
        quantization={"fp16": quant_cap},
        execution_modes=["eager"],
        capabilities=["streaming"],
        platform_constraints=plat_cons,
        adapter_requirements=adapt_req
    )

    # Serialize to JSON
    json_str = ProviderSerializer.to_json(cap)

    # Deserialize back
    cap_restored = ProviderSerializer.from_json(json_str)

    # Verify
    assert cap_restored.provider == cap.provider
    assert cap_restored.version == cap.version
    assert cap_restored.architectures == cap.architectures
    assert cap_restored.operators["attention"].support == SupportLevel.SUPPORTED
    assert cap_restored.operators["attention"].implementation_notes == "test note"
    assert cap_restored.quantization["fp16"].support == QuantizationSupport.NATIVE
    assert cap_restored.platform_constraints.apple_silicon_only is True
    assert cap_restored.platform_constraints.metal_required is True
    assert cap_restored.adapter_requirements.needs_weight_conversion is True

def test_minimal_serialization():
    cap = ProviderCapability(
        provider="minimal",
        version="0.1"
    )
    json_str = ProviderSerializer.to_json(cap)
    cap_restored = ProviderSerializer.from_json(json_str)

    assert cap_restored.provider == "minimal"
    assert cap_restored.version == "0.1"
    assert len(cap_restored.architectures) == 0
    assert len(cap_restored.operators) == 0
    # check defaults were preserved/restored correctly
    assert cap_restored.platform_constraints.windows_supported is True
