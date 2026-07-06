from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List
import uuid

from omlx.planner.domains.bundle import PlanningBundle

@dataclass(frozen=True)
class SessionDescriptor:
    """Immutable definition of the session request."""
    session_id: str
    client_id: Optional[str] = None
    priority: int = 0

@dataclass(frozen=True)
class SessionMetadata:
    """Immutable key-value pairs associated with the session."""
    created_at: float
    tags: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class SessionStatistics:
    """Immutable summary of execution statistics."""
    total_duration: float = 0.0
    tokens_generated: int = 0
    memory_peak: int = 0

@dataclass(frozen=True)
class SessionValidationReport:
    """Immutable diagnostic report of the session parameters."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

@dataclass
class RuntimeSession:
    """
    Coordinates the execution lifecycle for a single generation/execution request.
    Owns the execution context but does not perform execution itself.
    """
    session_id: str
    state: str = "created"

    # Owned immutable artifacts
    descriptor: Optional[SessionDescriptor] = None
    metadata: Optional[SessionMetadata] = None
    statistics: Optional[SessionStatistics] = None
    validation_report: Optional[SessionValidationReport] = None

    # Attached execution resources
    planning_bundle: Optional[PlanningBundle] = None
    execution_context: Optional[Any] = None # Will be ExecutionContext
    device_context: Optional[Any] = None # Will be DeviceContext
    memory_context: Optional[Any] = None # Will be MemoryContext
    cache_session: Optional[Any] = None
    observation_session: Optional[Any] = None
    generation_strategy: Optional[Any] = None

    @classmethod
    def create(cls) -> "RuntimeSession":
        return cls(session_id=str(uuid.uuid4()))
