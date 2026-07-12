# SPDX-License-Identifier: Apache-2.0

from typing import Dict, Any
from omlx.framework.model_intelligence.descriptor import ModelDescriptor
from omlx.planner.ir.graph import ExecutionIR
from types import MappingProxyType

class ConstraintCompiler:
    """Compiles execution constraints."""

    def compile_constraints(self, descriptor: ModelDescriptor, ir: ExecutionIR) -> MappingProxyType[str, Any]:
        constraints = {}

        # Estimate minimum RAM (very rough estimation based on parameter count)
        # Assuming FP16/BF16 by default (~2 bytes per param) + 20% overhead
        if descriptor.parameter_count > 0:
            bytes_required = descriptor.parameter_count * 2 * 1.2
            gb_required = bytes_required / (1024 ** 3)
            constraints["minimum_memory"] = f"{gb_required:.1f}GB"

        if descriptor.context_length > 0:
            constraints["maximum_sequence_length"] = descriptor.context_length

        if descriptor.backend_requirements:
            constraints["preferred_backend"] = descriptor.backend_requirements[0]

        # Inspect IR for specific constraints
        required_precisions = set()
        for node in ir.nodes.values():
            if "precision" in node.metadata:
                required_precisions.add(node.metadata["precision"])
            if node.metadata.get("dynamic_shapes", False):
                constraints["dynamic_shapes"] = True

        if required_precisions:
            constraints["required_precision"] = list(required_precisions)

        return MappingProxyType(constraints)

    def compile_requirements(self, descriptor: ModelDescriptor, ir: ExecutionIR, features: MappingProxyType[str, Any]) -> tuple[str, ...]:
        requirements = set()

        if descriptor.kv_cache_support:
            requirements.add("kv_cache")
        if descriptor.tokenizer_family:
            requirements.add("tokenizer")
        if "rope" in features:
            requirements.add("rotary_embedding")
        if "flash_attention" in features:
            requirements.add("flash_attention")
        if "vision_encoder" in features:
            requirements.add("vision_encoder")
        if descriptor.task in ("chat", "text_generation"):
            requirements.add("sampling")

        return tuple(sorted(list(requirements)))
