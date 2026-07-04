import threading
from typing import Dict, List, Optional, Type, Any, Set
from .descriptor import PluginDescriptor, PluginLifecycleState
from .context import PluginContext
from .contracts import ExtensionPoint

class PluginRegistry:
    """
    Registry for managing plugin discovery, registration, and lifecycle.
    Becomes immutable after startup.
    """
    def __init__(self):
        self._lock = threading.RLock()

        # Map of plugin ID -> PluginDescriptor
        self._descriptors: Dict[str, PluginDescriptor] = {}

        # Map of plugin ID -> Lifecycle State
        self._plugin_states: Dict[str, PluginLifecycleState] = {}

        # Map of plugin ID -> PluginContext
        self._plugin_contexts: Dict[str, PluginContext] = {}

        # Map of Extension Class -> List of registered extension instances
        self._extensions_by_type: Dict[Type[ExtensionPoint], List[ExtensionPoint]] = {}

        self._is_sealed = False

        # Diagnostics reports
        self._diagnostics: Dict[str, Any] = {
            "registration": {},
            "dependency": {},
            "validation": {},
            "compatibility": {},
            "lifecycle": {},
            "health": {},
            "discovery": {}
        }

    def _check_sealed(self):
        if self._is_sealed:
            raise RuntimeError("PluginRegistry is sealed and cannot be modified.")

    def seal(self) -> None:
        """Lock the registry to prevent further modification after startup."""
        with self._lock:
            self._is_sealed = True

    def register_plugin(self, descriptor: PluginDescriptor, context: PluginContext) -> None:
        """Register a plugin with its descriptor and context."""
        with self._lock:
            self._check_sealed()

            if descriptor.plugin_id in self._descriptors:
                self._diagnostics["registration"][descriptor.plugin_id] = "Duplicate plugin ID detected."
                raise ValueError(f"Plugin ID {descriptor.plugin_id} is already registered.")

            self._descriptors[descriptor.plugin_id] = descriptor
            self._plugin_states[descriptor.plugin_id] = PluginLifecycleState.REGISTERED
            self._plugin_contexts[descriptor.plugin_id] = context
            self._diagnostics["registration"][descriptor.plugin_id] = "Success"
            self._diagnostics["lifecycle"][descriptor.plugin_id] = PluginLifecycleState.REGISTERED.value

    def transition_state(self, plugin_id: str, new_state: PluginLifecycleState) -> None:
         """Transition the lifecycle state of a plugin."""
         with self._lock:
              self._check_sealed()

              if plugin_id not in self._descriptors:
                   raise ValueError(f"Plugin ID {plugin_id} not found.")

              self._plugin_states[plugin_id] = new_state
              self._diagnostics["lifecycle"][plugin_id] = new_state.value

    def validate_dependencies(self) -> None:
        """Validate dependencies for all registered plugins."""
        with self._lock:
             self._check_sealed()

             for plugin_id, descriptor in self._descriptors.items():
                 # Check required dependencies
                 for req_plugin_id, req_version in descriptor.dependencies.items():
                     if req_plugin_id not in self._descriptors:
                         self._diagnostics["dependency"][plugin_id] = f"Missing required dependency: {req_plugin_id}"
                         self.transition_state(plugin_id, PluginLifecycleState.FAILED)
                     # (Version constraint checking would go here)

                 # Check optional dependencies
                 for opt_plugin_id, opt_version in descriptor.optional_dependencies.items():
                     if opt_plugin_id not in self._descriptors:
                         if plugin_id not in self._diagnostics["dependency"]:
                             self._diagnostics["dependency"][plugin_id] = []
                         if isinstance(self._diagnostics["dependency"][plugin_id], list):
                             self._diagnostics["dependency"][plugin_id].append(f"Missing optional dependency: {opt_plugin_id}")

             # Perform topological sort / circular dependency check
             self._check_circular_dependencies()

    def _check_circular_dependencies(self) -> None:
        # Simplified circular dependency check
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            descriptor = self._descriptors.get(node)
            if descriptor:
                for neighbor in descriptor.dependencies:
                    if neighbor not in visited:
                        if dfs(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True

            rec_stack.remove(node)
            return False

        for plugin_id in self._descriptors:
            if plugin_id not in visited:
                if dfs(plugin_id):
                    self._diagnostics["dependency"]["global"] = f"Circular dependency detected involving {plugin_id}"
                    self.transition_state(plugin_id, PluginLifecycleState.FAILED)
                    # Note: in a real implementation we'd fail all involved plugins

    def get_extensions(self, extension_type: Type[ExtensionPoint]) -> List[ExtensionPoint]:
        """Retrieve all registered extensions of a specific type."""
        with self._lock:
            # We must gather extensions from all plugin contexts
            extensions = []
            for context in self._plugin_contexts.values():
                for ext in context.get_registered_extensions():
                    if isinstance(ext, extension_type):
                        extensions.append(ext)
            return extensions

    def get_descriptor(self, plugin_id: str) -> Optional[PluginDescriptor]:
        with self._lock:
             return self._descriptors.get(plugin_id)

    def get_state(self, plugin_id: str) -> Optional[PluginLifecycleState]:
         with self._lock:
              return self._plugin_states.get(plugin_id)

    def generate_diagnostics_report(self) -> Dict[str, Any]:
        """Return the collected diagnostics report."""
        with self._lock:
            return self._diagnostics.copy()
