import pytest
from omlx.capabilities.descriptor import CapabilityDescriptor, ExecutionFamily, CacheLayoutType, AttentionType
from omlx.planner.planner import ExecutionPlanner
from omlx.planner.compatibility import ExecutionProfileAdapter
from omlx.inference.execution_profile import ExecutionProfile

def test_execution_profile_adapter():
    descriptor = CapabilityDescriptor(
        execution_family=ExecutionFamily.AUTOREGRESSIVE,
        supported_modalities=("text",),
        attention_types=(AttentionType.CAUSAL,),
        cache_layout=CacheLayoutType.PAGED,
        supports_streaming=True,
        supports_speculative=False,
        execution_hints={"attention_mode": "custom_causal"}
    )

    planner = ExecutionPlanner()
    plan = planner.plan(descriptor)

    profile = ExecutionProfileAdapter.adapt(plan)

    assert isinstance(profile, ExecutionProfile)
    assert profile.backend_name == "autoregressive"
    assert profile.attention_mode == "custom_causal"
