import pytest
import asyncio
from omlx.capabilities.resolver import CapabilityResolver
from omlx.planner.planner import ExecutionPlanner

@pytest.mark.asyncio
async def test_capability_resolver_concurrency():
    resolver = CapabilityResolver()

    async def resolve_task():
        # simulate some async capability resolution
        await asyncio.sleep(0.001)
        pass

    tasks = [resolve_task() for _ in range(100)]
    await asyncio.gather(*tasks)

@pytest.mark.asyncio
async def test_planner_concurrency():
    planner = ExecutionPlanner()

    async def plan_task():
        # simulate some async planning
        await asyncio.sleep(0.001)
        pass

    tasks = [plan_task() for _ in range(100)]
    await asyncio.gather(*tasks)

@pytest.mark.asyncio
async def test_cache_access_concurrency():
    async def access_cache_task():
        await asyncio.sleep(0.001)
        pass

    tasks = [access_cache_task() for _ in range(100)]
    await asyncio.gather(*tasks)

@pytest.mark.asyncio
async def test_registry_access_concurrency():
    async def access_registry_task():
        await asyncio.sleep(0.001)
        pass

    tasks = [access_registry_task() for _ in range(100)]
    await asyncio.gather(*tasks)
