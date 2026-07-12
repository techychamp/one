# SPDX-License-Identifier: Apache-2.0

from typing import Dict, Any
from omlx.framework.model_intelligence.descriptor import ModelDescriptor
from omlx.planner.ir.graph import ExecutionIR
from types import MappingProxyType

class CapabilityCompiler:
    """Extracts capabilities from CMR and IR."""

    def extract_capabilities(self, descriptor: ModelDescriptor, ir: ExecutionIR) -> MappingProxyType[str, bool]:
        capabilities = {
            "chat": descriptor.task in ("chat", "conversational") or descriptor.tokenizer_family != "",
            "embeddings": descriptor.embedding_support or descriptor.task == "embedding",
            "vision": descriptor.vision_support or descriptor.modality in ("vision", "multimodal"),
            "audio": descriptor.audio_support or descriptor.modality == "audio",
            "diffusion": descriptor.modality == "image_generation",
            "moe": descriptor.expert_support or descriptor.expert_count > 0,
            "speculative_decoding": descriptor.speculative_support,
            "long_context": descriptor.context_length >= 32768,
            "streaming": descriptor.streaming_support,
            "function_calling": descriptor.tool_support,
            "tool_calling": descriptor.tool_support,
        }

        # Check IR for additional hints
        for node in ir.nodes.values():
            if node.node_type.value == "routing":
                capabilities["moe"] = True

        return MappingProxyType(capabilities)
