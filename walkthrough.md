# IMP-002: RuntimeBuilder & Composition Root

## Architecture Report
- The `RuntimeBuilder` and `Runtime` classes have been implemented in `omlx/runtime/builder.py`.
- The `RuntimeContext` acts as an immutable configuration object.
- The `Runtime` object acts as the Composition Root, owning components like `engine_pool`, `settings`, and `feature_flags`.
- `omlx/server.py` has been updated to initialize the `Runtime` using `RuntimeBuilder` during `init_server()`, and `_server_state` now delegates `engine_pool` access to the runtime object if present.

## Verification Report
- The tests for `RuntimeBuilder` have been executed and passed.
- No execution logic or models have been altered.
- All legacy behavior is preserved using `_server_state` delegation.

## Rollback Procedure
To rollback, simply revert `omlx/server.py` to remove the `RuntimeBuilder` instantiation in `init_server()` and `get_engine_pool()`, and delete `omlx/runtime/builder.py`.

## Recommendations for IMP-003
- Proceed with migrating `ExecutionPlanner` and `ModelAdapters` to be owned by the `Runtime`.
- Start removing direct usages of `_server_state` across the repository in favor of dependency injection via API routes (e.g. `FastAPI Depends()`).
