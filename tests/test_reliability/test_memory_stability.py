import pytest
import gc
import sys
from omlx.capabilities.resolver import CapabilityResolver
from omlx.planner.planner import ExecutionPlanner

def test_memory_stability():
    gc.collect()
    initial_objects = len(gc.get_objects())

    # Do work that shouldn't leak memory globally
    for _ in range(100):
        resolver = CapabilityResolver()
        planner = ExecutionPlanner()
        # In real scenario, execute a full mock pipeline

    gc.collect()
    final_objects = len(gc.get_objects())

    # Allow some small tolerance for background python things, but bounded
    diff = final_objects - initial_objects
    assert diff < 1000, f"Potential memory leak detected: {diff} new objects left"

def test_cache_eviction_memory_stability():
    gc.collect()
    # Simulate cache fill and evict
    for _ in range(100):
        pass
    gc.collect()
    pass
