import pytest
from omlx.compiler.providers.capability import (
    ProviderCapability, OperatorCapability, QuantizationCapability,
    PlatformConstraints, AdapterRequirements, SupportLevel, QuantizationSupport
)

def test_provider_capability_initialization():
    cap = ProviderCapability(
        provider="test_provider",
        version="1.0"
    )
    assert cap.provider == "test_provider"
    assert cap.version == "1.0"
    assert len(cap.architectures) == 0
    assert len(cap.operators) == 0
    assert len(cap.tensor_layouts) == 0
    assert len(cap.quantization) == 0
    assert len(cap.execution_modes) == 0
    assert len(cap.capabilities) == 0

    # Check defaults
    assert cap.platform_constraints.windows_supported is True
    assert cap.platform_constraints.apple_silicon_only is False
    assert cap.adapter_requirements.needs_tensor_conversion is False

def test_provider_capability_with_data():
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

    assert "llama" in cap.architectures
    assert cap.operators["attention"].support == SupportLevel.SUPPORTED
    assert cap.operators["attention"].implementation_notes == "test note"
    assert cap.quantization["fp16"].support == QuantizationSupport.NATIVE
    assert cap.platform_constraints.apple_silicon_only is True
    assert cap.platform_constraints.metal_required is True
    assert cap.adapter_requirements.needs_weight_conversion is True

def test_capability_immutability():
    cap = ProviderCapability(
        provider="test",
        version="1.0"
    )
    # dataclass with frozen=True raises Exception on modification
    with pytest.raises(Exception): # usually FrozenInstanceError
        cap.provider = "new_provider"
