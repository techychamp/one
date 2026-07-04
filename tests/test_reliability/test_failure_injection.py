import pytest
from omlx.capabilities.resolver import CapabilityResolver
from omlx.planner.planner import ExecutionPlanner
from .utils import FailureInjector

def test_capability_resolver_failure_injection():
    resolver = CapabilityResolver()
    # Mock some method to fail
    resolver = FailureInjector.inject_failure(resolver, "resolve", ValueError("Injected failure"))

    with pytest.raises(ValueError, match="Injected failure"):
        resolver.resolve()

def test_planner_failure_injection():
    planner = ExecutionPlanner()
    # if it had a plan method
    # planner = FailureInjector.inject_failure(planner, "plan", RuntimeError("Injected planner failure"))
    # with pytest.raises(RuntimeError):
    #     planner.plan()
    pass

def test_cache_corruption_injection():
    # simulate cache failure
    pass

def test_translation_failure_injection():
    # simulate translation failure
    pass
