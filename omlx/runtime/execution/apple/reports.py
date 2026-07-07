from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

@dataclass(frozen=True)
class AppleExecutionReport:
    operation_id: str
    latency_ms: float
    status: str
    error_message: Optional[str] = None
    diagnostics: Tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class UnifiedMemoryReport:
    memory_policy_applied: str
    bytes_transferred: int = 0
    synchronization_events: int = 0
    diagnostics: Tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class PlacementExecutionReport:
    placement_strategy_applied: str
    actual_device: str
    diagnostics: Tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class AppleRuntimeStatistics:
    total_execution_latency_ms: float = 0.0
    total_memory_transfers: int = 0
    total_placement_validations: int = 0

@dataclass(frozen=True)
class AppleRuntimeDiagnostics:
    execution_reports: Tuple[AppleExecutionReport, ...] = field(default_factory=tuple)
    memory_report: Optional[UnifiedMemoryReport] = None
    placement_report: Optional[PlacementExecutionReport] = None
    statistics: AppleRuntimeStatistics = field(default_factory=AppleRuntimeStatistics)
