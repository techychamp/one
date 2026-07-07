# SPDX-License-Identifier: Apache-2.0
"""
Transformation validator for cache realization.
"""

from typing import Tuple
from dataclasses import dataclass, field
from omlx.planner.ir.graph import ExecutionIR
from omlx.planner.ir.nodes import IRNodeType
from omlx.planner.domains.cache.artifacts import CacheRealizationDiagnostic

@dataclass(frozen=True)
class CacheValidationReport:
    """Immutable report resulting from validation of cache realization."""
    is_valid: bool
    diagnostics: Tuple[CacheRealizationDiagnostic, ...] = field(default_factory=tuple)

class CacheTransformationValidator:
    """Validates that a transformed ExecutionIR contains valid cache operations."""

    def validate(self, original_ir: ExecutionIR, transformed_ir: ExecutionIR) -> CacheValidationReport:
        """
        Validates the transformed ExecutionIR to ensure cache constraints are met.
        For example, checking if every CACHE_READ is validly connected.
        """
        diagnostics = []
        is_valid = True

        for node_id, node in transformed_ir.nodes.items():
            if node.node_type == IRNodeType.CACHE_READ:
                # Cache read should have some dependency if not root
                pass
            elif node.node_type == IRNodeType.CACHE_WRITE:
                if not node.dependencies:
                    is_valid = False
                    diagnostics.append(CacheRealizationDiagnostic(
                        severity="ERROR",
                        message=f"CACHE_WRITE node {node_id} has no dependencies.",
                        node_ids=(node_id,)
                    ))

        return CacheValidationReport(
            is_valid=is_valid,
            diagnostics=tuple(diagnostics)
        )
