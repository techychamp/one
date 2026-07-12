import pytest
from omlx.compiler.providers.analyzer import MLXAnalyzer, HuggingFaceAnalyzer, LlamaCppAnalyzer
from omlx.compiler.providers.capability import SupportLevel, QuantizationSupport

def test_mlx_analyzer():
    analyzer = MLXAnalyzer()
    cap = analyzer.analyze()

    assert cap.provider == "mlx"
    assert "llama" in cap.architectures

    assert "attention" in cap.operators
    assert cap.operators["attention"].support == SupportLevel.SUPPORTED

    assert "moe" in cap.operators
    assert cap.operators["moe"].support == SupportLevel.SUPPORTED
    assert cap.operators["moe"].implementation_notes is not None

    assert cap.quantization["fp16"].support == QuantizationSupport.NATIVE
    assert cap.quantization["awq"].support == QuantizationSupport.ADAPTER

    assert cap.platform_constraints.apple_silicon_only is True
    assert cap.platform_constraints.windows_supported is False

    assert cap.adapter_requirements.needs_weight_conversion is True

def test_huggingface_analyzer():
    analyzer = HuggingFaceAnalyzer()
    cap = analyzer.analyze()

    assert cap.provider == "huggingface"
    assert "bert" in cap.architectures

    assert cap.quantization["awq"].support == QuantizationSupport.NATIVE
    assert cap.platform_constraints.apple_silicon_only is False
    assert cap.platform_constraints.windows_supported is True

    assert cap.adapter_requirements.needs_tensor_conversion is True
    assert cap.adapter_requirements.needs_scheduler_adapter is True

def test_llamacpp_analyzer():
    analyzer = LlamaCppAnalyzer()
    cap = analyzer.analyze()

    assert cap.provider == "llama.cpp"
    assert "ggml" in cap.tensor_layouts

    assert cap.quantization["q4"].support == QuantizationSupport.NATIVE
    assert cap.quantization["iq"].support == QuantizationSupport.NATIVE

    assert cap.platform_constraints.cpu_only is False
    assert cap.platform_constraints.windows_supported is True
