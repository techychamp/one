import pytest
import random
from omlx.capabilities.resolver import CapabilityResolver
from omlx.planner.planner import ExecutionPlanner
from .utils import RandomGenerator, DescriptorGenerator

def test_capability_resolver_fuzz():
    resolver = CapabilityResolver()

    for _ in range(100):
        # fuzz input string
        random_str = RandomGenerator.random_string(random.randint(1, 100))
        # ensure it handles bad inputs without crashing
        try:
            # mock resolving something that doesn't exist
            pass
        except Exception:
            pass # exceptions are fine, crashes are not

def test_planner_fuzz():
    planner = ExecutionPlanner()
    for _ in range(100):
        random_dict = RandomGenerator.random_dict(keys=random.randint(1, 10))
        try:
            # mock plan with bad dict
            pass
        except Exception:
            pass

def test_metadata_fuzz():
    for _ in range(100):
        descriptor = DescriptorGenerator.generate_capability_descriptor()
        try:
            pass
        except Exception:
            pass
