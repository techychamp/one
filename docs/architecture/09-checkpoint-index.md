# Engineering Checkpoint Map

This roadmap breaks down future work into isolated, verifiable repository-specific engineering checkpoints.

## Checkpoint 1: Diffusion Execution Backend Promotion
* **Goal**: Stabilize the experimental diffusion backend for production use.
* **Purpose**: Support upcoming Diffusion Language Models (Nemotron Labs, Diffusion Gemma).
* **Allowed Files**: `omlx/inference/backends/diffusion_backend.py`, `omlx/inference/strategies/diffusion.py`, `tests/test_diffusion_backend.py`.
* **Forbidden Files**: `omlx/scheduler.py`, `omlx/engine_core.py`.
* **Dependencies**: Stable MLX tensor definitions for noise scheduling.
* **Verification**: `pytest tests/test_diffusion_backend.py`.
* **Rollback Strategy**: Revert to `ExperimentalDiffusionBackend`.
* **Exit Criteria**: Diffusion inference runs end-to-end without crashing on standard noise schedules.

## Checkpoint 2: Verification Execution Graph Nodes
* **Goal**: Implement `VERIFY` nodes for the execution graph.
* **Purpose**: Enable Nemotron Triage and self-correction strategies.
* **Allowed Files**: `omlx/inference/execution_graph.py`, `omlx/inference/strategies/triage.py`.
* **Forbidden Files**: Core caching logic, API routes.
* **Dependencies**: Execution graph stability.
* **Verification**: Unit tests proving graph traversal through a `VERIFY` node.
* **Rollback Strategy**: Drop triage strategy registry.
* **Exit Criteria**: Strategy successfully conditionally drops or accepts tokens based on verify outputs.

## Checkpoint 3: Streaming MoE Kernel Integration
* **Goal**: Add metal primitives for Streaming MoE.
* **Purpose**: Improve latency for large mixture-of-experts models.
* **Allowed Files**: `omlx/custom_kernels/streaming_moe/`, `omlx/models/streaming_moe.py`.
* **Forbidden Files**: `omlx/scheduler.py`.
* **Dependencies**: Upstream MLX C++ APIs.
* **Verification**: `tests/test_hardware_benchmark.py` custom runs.
* **Rollback Strategy**: Fallback to standard MLX linear layers.
* **Exit Criteria**: Kernel compiles and outperforms naive execution.

## Checkpoint 4: Dynamic Scheduler Policies
* **Goal**: Implement resource-aware dynamic execution planning.
* **Purpose**: Optimize throughput vs TTFT dynamically based on memory pressure.
* **Allowed Files**: `omlx/scheduler.py`, `tests/test_scheduler_admission.py`.
* **Forbidden Files**: `omlx/engine_core.py`, `omlx/api/`.
* **Dependencies**: Memory Monitor reliability.
* **Verification**: Extensive load testing via `test_scheduler.py`.
* **Rollback Strategy**: Default to FCFS policy.
* **Exit Criteria**: System avoids OOM under heavy load by dynamically shrinking batch sizes.
