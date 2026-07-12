import pytest
from omlx.compiler.providers.capability import (
    ProviderCapability, OperatorCapability, QuantizationCapability,
    PlatformConstraints, AdapterRequirements, SupportLevel, QuantizationSupport
)
from omlx.compiler.providers.validation import ProviderValidator

@pytest.fixture
def validator():
    return ProviderValidator()

def test_validation_success(validator):
    cap = ProviderCapability(
        provider="valid_provider",
        version="1.0",
        architectures=["llama"],
        operators={"attention": OperatorCapability(support=SupportLevel.SUPPORTED)},
        quantization={"fp16": QuantizationCapability(support=QuantizationSupport.NATIVE)}
    )

    issues = validator.validate(cap)
    assert len(issues) == 0
    assert validator.is_valid(cap) is True

def test_validation_missing_required(validator):
    cap = ProviderCapability(
        provider="",
        version=""
    )

    issues = validator.validate(cap)
    assert len(issues) > 0
    assert validator.is_valid(cap) is False

    fields = [i.field for i in issues]
    assert "provider" in fields
    assert "version" in fields

def test_validation_warnings(validator):
    # Missing architectures, operators, quantization should raise warnings
    cap = ProviderCapability(
        provider="test",
        version="1.0"
    )

    issues = validator.validate(cap)
    assert len(issues) > 0
    assert validator.is_valid(cap) is True # Warnings don't make it invalid

    severities = [i.severity for i in issues]
    assert all(s == "warning" for s in severities)

    fields = [i.field for i in issues]
    assert "architectures" in fields
    assert "operators" in fields
    assert "quantization" in fields

def test_validation_platform_contradictions(validator):
    # Apple Silicon and CUDA
    cap1 = ProviderCapability(
        provider="test",
        version="1.0",
        platform_constraints=PlatformConstraints(apple_silicon_only=True, cuda_required=True)
    )
    issues1 = validator.validate(cap1)
    assert validator.is_valid(cap1) is False
    assert any(i.severity == "error" and i.field == "platform_constraints" for i in issues1)

    # CPU only and Metal
    cap2 = ProviderCapability(
        provider="test",
        version="1.0",
        platform_constraints=PlatformConstraints(cpu_only=True, metal_required=True)
    )
    issues2 = validator.validate(cap2)
    assert validator.is_valid(cap2) is False
    assert any(i.severity == "error" and i.field == "platform_constraints" for i in issues2)
