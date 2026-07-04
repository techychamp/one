from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from enum import Enum


class PluginCategory(Enum):
    CAPABILITY = "capability"
    VALIDATION = "validation"
    PLANNER = "planner"
    OPTIMIZATION = "optimization"
    LOWERING = "lowering"
    BACKEND = "backend"
    BACKEND_INTELLIGENCE = "backend_intelligence"
    VERIFICATION = "verification"
    TOOLING = "tooling"
    CLI = "cli"
    EXPORTER = "exporter"
    VISUALIZATION = "visualization"
    QUANTIZATION = "quantization"
    DIAGNOSTICS = "diagnostics"


class PluginLifecycleState(Enum):
    DISCOVERED = "discovered"
    REGISTERED = "registered"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    VALIDATED = "validated"
    ENABLED = "enabled"
    DISABLED = "disabled"
    EXPERIMENTAL = "experimental"
    DEPRECATED = "deprecated"
    FAILED = "failed"


@dataclass(frozen=True)
class PluginDescriptor:
    """
    Immutable metadata descriptor for a plugin.
    """
    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    category: PluginCategory

    # Version compatibility
    supported_compiler_versions: List[str] = field(default_factory=list)
    supported_runtime_versions: List[str] = field(default_factory=list)

    # Dependencies
    dependencies: Dict[str, str] = field(default_factory=dict)
    optional_dependencies: Dict[str, str] = field(default_factory=dict)

    # Capabilities and Extension Points
    provided_extension_points: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)

    # Additional metadata and diagnostics
    metadata: Dict[str, Any] = field(default_factory=dict)
    diagnostics: Dict[str, Any] = field(default_factory=dict)
