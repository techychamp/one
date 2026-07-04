import importlib
import importlib.metadata
import logging
from typing import Dict, List, Optional
from .registry import PluginRegistry
from .context import PluginContext
from .descriptor import PluginDescriptor, PluginLifecycleState

logger = logging.getLogger(__name__)

class PluginManager:
    """
    Manages the lifecycle, discovery, and loading of oMLX plugins.
    """
    def __init__(self, runtime_context, feature_flags, compiler_metadata=None, backend_metadata=None):
        self._registry = PluginRegistry()
        self._runtime_context = runtime_context
        self._feature_flags = feature_flags
        self._compiler_metadata = compiler_metadata or {}
        self._backend_metadata = backend_metadata or {}

    @property
    def registry(self) -> PluginRegistry:
        return self._registry

    def discover_plugins(self, entry_point_group: str = "omlx.plugins") -> None:
        """
        Discover plugins using Python's entry_points mechanism.
        Does not load them dynamically here to respect constraints,
        but reads their metadata/descriptors.
        """
        # Note: constraint says "No dynamic loading required" and "Do NOT implement network plugin discovery"
        # We will assume plugins are statically registered or discovered via importlib.metadata but not
        # dynamically downloaded or reloaded.

        try:
            entry_points = importlib.metadata.entry_points()
            # Handle different Python versions
            if hasattr(entry_points, "select"):
                eps = entry_points.select(group=entry_point_group)
            else:
                eps = entry_points.get(entry_point_group, [])

            for ep in eps:
                try:
                    plugin_module = ep.load()

                    # Expected standard: plugin module provides `get_descriptor()` and `initialize_plugin()`
                    if hasattr(plugin_module, "get_descriptor") and hasattr(plugin_module, "initialize_plugin"):
                        descriptor = plugin_module.get_descriptor()
                        if isinstance(descriptor, PluginDescriptor):
                            # Create context
                            context = PluginContext(
                                runtime_context=self._runtime_context,
                                feature_flags=self._feature_flags,
                                registries=self._registry,
                                compiler_metadata=self._compiler_metadata,
                                backend_metadata=self._backend_metadata
                            )

                            self._registry.register_plugin(descriptor, context)
                            self._registry.transition_state(descriptor.plugin_id, PluginLifecycleState.DISCOVERED)

                            # Initialize plugin (allow it to register extensions into context)
                            plugin_module.initialize_plugin(context)
                            self._registry.transition_state(descriptor.plugin_id, PluginLifecycleState.INITIALIZED)

                        else:
                            logger.warning(f"Entry point {ep.name} did not return a valid PluginDescriptor")

                except Exception as e:
                    logger.error(f"Failed to load plugin from entry point {ep.name}: {e}")
        except Exception as e:
            logger.warning(f"Error during plugin discovery: {e}")

    def validate_and_seal(self) -> None:
        """
        Validates the dependency graph and seals the registry.
        """
        self._registry.validate_dependencies()

        # Transition healthy plugins to loaded/enabled (if validation passed)
        for plugin_id in self._registry._descriptors:
            if self._registry.get_state(plugin_id) not in (PluginLifecycleState.FAILED, PluginLifecycleState.DISABLED):
                self._registry.transition_state(plugin_id, PluginLifecycleState.ENABLED)

        self._registry.seal()

    def get_diagnostics(self) -> Dict:
        return self._registry.generate_diagnostics_report()
