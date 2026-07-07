from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from .diagnostics import SchedulingDiagnostics
from .statistics import SchedulingStatistics

class ExecutionPhaseType(Enum):
    DEVICE_PREPARATION = "Device Preparation"
    CACHE_PREPARATION = "Cache Preparation"
    MEMORY_PREPARATION = "Memory Preparation"
    BATCH_PREPARATION = "Batch Preparation"
    ROUTING_PREPARATION = "Routing Preparation"
    DIFFUSION_PREPARATION = "Diffusion Preparation"
    COMPUTE = "Compute"
    SYNCHRONIZATION = "Synchronization"
    COMPLETION = "Completion"

@dataclass(frozen=True)
class SynchronizationPoint:
    name: str
    dependencies: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class DependencyBarrier:
    name: str
    dependencies: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ExecutionBarrier:
    name: str
    dependencies: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ExecutionPhase:
    name: str
    phase_type: Optional[ExecutionPhaseType] = None
    operations: List[str] = field(default_factory=list)
    barriers: List[DependencyBarrier] = field(default_factory=list)
    sync_points: List[SynchronizationPoint] = field(default_factory=list)

@dataclass(frozen=True)
class ExecutionPhaseGraph:
    phases: List[ExecutionPhase] = field(default_factory=list)
    barriers: List[ExecutionBarrier] = field(default_factory=list)
    sync_points: List[SynchronizationPoint] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class DependencyGraph:
    operations: Dict[str, Any] = field(default_factory=dict)
    phases: List[ExecutionPhase] = field(default_factory=list)
    barriers: List[DependencyBarrier] = field(default_factory=list)
    sync_points: List[SynchronizationPoint] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

# Aliases for Scheduler terminology
SchedulerDiagnostics = SchedulingDiagnostics
SchedulerStatistics = SchedulingStatistics
