from abc import ABC, abstractmethod
from .capability import (
    ProviderCapability, OperatorCapability, QuantizationCapability,
    PlatformConstraints, AdapterRequirements, SupportLevel, QuantizationSupport
)

class ProviderAnalyzer(ABC):
    @abstractmethod
    def analyze(self) -> ProviderCapability:
        """Analyze the provider and return its capabilities."""
        pass

class MLXAnalyzer(ProviderAnalyzer):
    def analyze(self) -> ProviderCapability:
        return ProviderCapability(
            provider="mlx",
            version="0.31.2", # Matches pyproject.toml
            architectures=["llama", "qwen", "gemma", "mistral", "phi3", "mixtral", "starcoder2"],
            operators={
                "attention": OperatorCapability(support=SupportLevel.SUPPORTED),
                "linear": OperatorCapability(support=SupportLevel.SUPPORTED),
                "rmsnorm": OperatorCapability(support=SupportLevel.SUPPORTED),
                "mlp": OperatorCapability(support=SupportLevel.SUPPORTED),
                "moe": OperatorCapability(support=SupportLevel.SUPPORTED, implementation_notes="Supported via mlx.core block sparse matrix multiplication"),
                "embedding": OperatorCapability(support=SupportLevel.SUPPORTED),
                "sampling": OperatorCapability(support=SupportLevel.SUPPORTED),
                "kv_cache": OperatorCapability(support=SupportLevel.SUPPORTED),
                "vision_encoder": OperatorCapability(support=SupportLevel.PARTIAL, implementation_notes="Supported through mlx-vlm"),
                "audio_encoder": OperatorCapability(support=SupportLevel.PARTIAL, implementation_notes="Supported through mlx-audio"),
                "diffusion_block": OperatorCapability(support=SupportLevel.PARTIAL, implementation_notes="Experimental"),
            },
            tensor_layouts=["row_major", "col_major"],
            quantization={
                "fp32": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "fp16": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "bf16": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "fp8": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "q4": QuantizationCapability(support=QuantizationSupport.NATIVE, implementation_notes="Group size 64/128"),
                "q8": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "awq": QuantizationCapability(support=QuantizationSupport.ADAPTER, implementation_notes="Requires format conversion"),
                "gptq": QuantizationCapability(support=QuantizationSupport.ADAPTER, implementation_notes="Requires format conversion")
            },
            execution_modes=["eager", "compiled"],
            capabilities=["streaming", "embeddings", "tool_calling", "speculative_decoding"],
            platform_constraints=PlatformConstraints(
                apple_silicon_only=True,
                metal_required=True,
                cuda_required=False,
                cpu_only=False,
                linux_only=False,
                windows_supported=False
            ),
            adapter_requirements=AdapterRequirements(
                needs_tensor_conversion=False,
                needs_weight_conversion=True,
                needs_tokenizer_adapter=True,
                needs_sampling_adapter=False,
                needs_scheduler_adapter=False
            )
        )

class HuggingFaceAnalyzer(ProviderAnalyzer):
    def analyze(self) -> ProviderCapability:
        return ProviderCapability(
            provider="huggingface",
            version="4.0",
            architectures=["llama", "qwen", "gemma", "mistral", "bert", "gpt2"],
            operators={
                "attention": OperatorCapability(support=SupportLevel.SUPPORTED),
                "linear": OperatorCapability(support=SupportLevel.SUPPORTED),
                "rmsnorm": OperatorCapability(support=SupportLevel.SUPPORTED),
                "mlp": OperatorCapability(support=SupportLevel.SUPPORTED),
                "embedding": OperatorCapability(support=SupportLevel.SUPPORTED),
                "sampling": OperatorCapability(support=SupportLevel.SUPPORTED),
                "kv_cache": OperatorCapability(support=SupportLevel.SUPPORTED),
                "vision_encoder": OperatorCapability(support=SupportLevel.SUPPORTED),
                "audio_encoder": OperatorCapability(support=SupportLevel.SUPPORTED),
            },
            tensor_layouts=["row_major"],
            quantization={
                "fp32": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "fp16": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "bf16": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "fp8": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "awq": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "gptq": QuantizationCapability(support=QuantizationSupport.NATIVE)
            },
            execution_modes=["eager"],
            capabilities=["streaming", "embeddings"],
            platform_constraints=PlatformConstraints(
                apple_silicon_only=False,
                metal_required=False,
                cuda_required=False,
                cpu_only=False,
                linux_only=False,
                windows_supported=True
            ),
            adapter_requirements=AdapterRequirements(
                needs_tensor_conversion=True,
                needs_weight_conversion=True,
                needs_tokenizer_adapter=True,
                needs_sampling_adapter=True,
                needs_scheduler_adapter=True
            )
        )

class LlamaCppAnalyzer(ProviderAnalyzer):
    def analyze(self) -> ProviderCapability:
        return ProviderCapability(
            provider="llama.cpp",
            version="1.0",
            architectures=["llama", "qwen", "gemma", "mistral", "phi3", "mixtral"],
            operators={
                "attention": OperatorCapability(support=SupportLevel.SUPPORTED),
                "linear": OperatorCapability(support=SupportLevel.SUPPORTED),
                "rmsnorm": OperatorCapability(support=SupportLevel.SUPPORTED),
                "mlp": OperatorCapability(support=SupportLevel.SUPPORTED),
                "moe": OperatorCapability(support=SupportLevel.SUPPORTED),
                "embedding": OperatorCapability(support=SupportLevel.SUPPORTED),
                "sampling": OperatorCapability(support=SupportLevel.SUPPORTED),
                "kv_cache": OperatorCapability(support=SupportLevel.SUPPORTED),
                "vision_encoder": OperatorCapability(support=SupportLevel.PARTIAL),
            },
            tensor_layouts=["ggml"],
            quantization={
                "fp32": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "fp16": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "q4": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "q5": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "q6": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "q8": QuantizationCapability(support=QuantizationSupport.NATIVE),
                "iq": QuantizationCapability(support=QuantizationSupport.NATIVE)
            },
            execution_modes=["compiled"],
            capabilities=["streaming", "embeddings", "tool_calling", "speculative_decoding"],
            platform_constraints=PlatformConstraints(
                apple_silicon_only=False,
                metal_required=False,
                cuda_required=False,
                cpu_only=False,
                linux_only=False,
                windows_supported=True
            ),
            adapter_requirements=AdapterRequirements(
                needs_tensor_conversion=True,
                needs_weight_conversion=True,
                needs_tokenizer_adapter=True,
                needs_sampling_adapter=True,
                needs_scheduler_adapter=True
            )
        )
