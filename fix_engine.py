with open("omlx/runtime/execution/engine.py", "r") as f:
    content = f.read()

replacement = """        with get_observer().observe_phase("Execution", "Engine", "execute"):
            try:
                # Cache Lifecycle Hook - Activation
                if context.cache_plan:
                    from omlx.runtime.execution.cache_session import CacheSession
                    # In a real implementation this would come from a session manager
                    cache_session = CacheSession(context.cache_plan)
                    cache_session.activate()
                    logger.debug(f"Activated cache session for plan: {context.cache_plan.plan_id}")

                result = self._executor.execute(context.backend_operation_graph, context)
                get_observer().track_artifact("ExecutionResult", result)

                # Cache Lifecycle Hook - Deactivation
                if context.cache_plan and 'cache_session' in locals():
                    cache_session.deactivate()
                    logger.debug("Deactivated cache session")

                return result"""

content = content.replace("""        with get_observer().observe_phase("Execution", "Engine", "execute"):
            try:
                result = self._executor.execute(context.backend_operation_graph, context)
                get_observer().track_artifact("ExecutionResult", result)
                return result""", replacement)

with open("omlx/runtime/execution/engine.py", "w") as f:
    f.write(content)
