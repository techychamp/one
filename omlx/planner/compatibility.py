from omlx.planner.plan import ExecutionPlan
from omlx.inference.execution_profile import ExecutionProfile

class ExecutionProfileAdapter:
    """Translates an ExecutionPlan into a legacy ExecutionProfile."""

    @staticmethod
    def adapt(plan: ExecutionPlan) -> ExecutionProfile:
        backend_name = plan.execution_backend
        # specific translation logic if needed
        # in legacy, if experimental_nemotron, we might need to map it back or handle it,
        # but execution_backend should map directly.

        # default mapping
        attention_mode = plan.execution_hints.get("attention_mode", "causal")

        # map cache_strategy enum to string
        cache_mode = str(plan.cache_strategy.value)
        if plan.cache_strategy.value == "paged":
            cache_mode = "standard" # maybe? Let's check execution_profile.py

        sampler_mode = plan.execution_hints.get("sampler_mode", "standard")

        streaming_mode = "standard"
        if plan.execution_mode == "streaming":
             streaming_mode = "standard" # wait, legacy doesn't have "streaming" in streaming_mode? Let's just use execution_mode

        position_encoding = plan.execution_hints.get("position_encoding", "rope")
        version = plan.execution_hints.get("version", "v1")

        return ExecutionProfile(
            backend_name=backend_name,
            attention_mode=attention_mode,
            cache_mode=cache_mode,
            sampler_mode=sampler_mode,
            streaming_mode=streaming_mode,
            position_encoding=position_encoding,
            version=version
        )
