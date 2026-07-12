# SPDX-License-Identifier: Apache-2.0

from typing import Dict, Any
from omlx.framework.model_intelligence.descriptor import ModelDescriptor
from omlx.planner.ir.graph import ExecutionIR
from types import MappingProxyType

class FeatureDetector:
    """Detects architectural features."""

    def detect_features(self, descriptor: ModelDescriptor, ir: ExecutionIR) -> MappingProxyType[str, Any]:
        features = {}

        # Based on descriptor
        if descriptor.attention_type:
            features["attention_type"] = descriptor.attention_type
            if descriptor.attention_type == "gqa":
                features["gqa"] = True

        if descriptor.moe_information:
            features["moe_routing"] = True

        if descriptor.vision_support:
            features["vlm"] = True
            features["vision_encoder"] = True

        if descriptor.audio_support:
            features["audio_encoder"] = True

        # Analyze IR nodes for features
        has_attention = False
        for node in ir.nodes.values():
            if node.node_type.value == "attention":
                has_attention = True
                if node.metadata.get("flash_attention", False):
                    features["flash_attention"] = True
                if node.metadata.get("rope", False):
                    features["rope"] = node.metadata.get("rope_type", "static")
                if node.metadata.get("sliding_window", False):
                    features["sliding_window"] = True
                if node.metadata.get("cross_attention", False):
                    features["cross_attention"] = True
            elif node.node_type.value == "routing":
                features["moe_routing"] = True
            elif node.node_type.value == "diffusion":
                features["diffusion_blocks"] = True

        if has_attention and "rope" not in features and descriptor.architecture in ("llama", "mistral", "qwen", "gemma"):
            features["rope"] = "static" # default fallback

        return MappingProxyType(features)
