# SPDX-License-Identifier: Apache-2.0

from typing import Dict, Any, List
from omlx.framework.model_intelligence.descriptor import ModelDescriptor
from omlx.planner.ir.graph import ExecutionIR
from types import MappingProxyType

class DiagnosticsEngine:
    """Identifies unsupported features and missing metadata."""

    def analyze_unsupported(self, descriptor: ModelDescriptor, ir: ExecutionIR) -> tuple[str, ...]:
        unsupported: List[str] = []

        # We don't have a definitive list of unsupported operators here,
        # but we can check for common issues or metadata flags indicating problems

        for node_id, node in ir.nodes.items():
            if node.metadata.get("unsupported", False):
                unsupported.append(f"unsupported_operator:{node.node_type.value}")

        if not descriptor.tokenizer_family and descriptor.task in ("chat", "text_generation"):
            unsupported.append("missing_tokenizer")

        return tuple(sorted(list(set(unsupported))))
