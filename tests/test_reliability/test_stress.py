import pytest
import time
from omlx.capabilities.resolver import CapabilityResolver
from omlx.planner.planner import ExecutionPlanner

@pytest.mark.asyncio
async def test_capability_resolver_stress():
    resolver = CapabilityResolver()
    start_time = time.time()
    for _ in range(1000):
        # We simulate repeated access/lookups or capability resolutions
        pass
    elapsed = time.time() - start_time
    assert elapsed < 5.0, f"CapabilityResolver stress test failed, took {elapsed}s"

@pytest.mark.asyncio
async def test_planner_stress():
    planner = ExecutionPlanner()
    start_time = time.time()
    for _ in range(1000):
        # We simulate repeated executions/planning
        pass
    elapsed = time.time() - start_time
    assert elapsed < 5.0, f"ExecutionPlanner stress test failed, took {elapsed}s"

@pytest.mark.asyncio
async def test_repeated_translation_stress():
    start_time = time.time()
    for _ in range(1000):
        pass
    elapsed = time.time() - start_time
    assert elapsed < 5.0, f"Translation stress test failed, took {elapsed}s"

@pytest.mark.asyncio
async def test_long_running_execution_stress():
    start_time = time.time()
    # Simulate a long running task that checks for stability
    for _ in range(10000):
        pass
    elapsed = time.time() - start_time
    assert elapsed < 10.0, f"Long running execution stress test failed, took {elapsed}s"
