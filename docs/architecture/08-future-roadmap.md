# Future Integration Audit

This audit determines how future capabilities could integrate into OMLX without architecture redesigns.

## 1. Diffusion Language Models (e.g., Nemotron Labs Diffusion, Diffusion Gemma)
* **Integration Point**: `omlx/inference/backends/`. An `ExperimentalDiffusionBackend` already exists.
* **Mechanism**: Implement a `DiffusionBackend` that adheres to the `ExecutionBackend` interface.
* **Graph**: Use `build_diffusion_graph` in `omlx/inference/execution_graph.py` (which includes `DENOISE` nodes).
* **API**: Add capabilities in `CapabilityRegistry` to route requests to the new backend.

## 2. Nemotron Triage / Verification Execution
* **Integration Point**: `omlx/inference/execution_graph.py` and `omlx/model_profiles.py`.
* **Mechanism**: Add a `VERIFY` `GraphNodeType`. The execution strategy can intercept generation steps to run verification models over the drafted output.
* **Profiles**: Use model profiles to define verification thresholds.

## 3. Streaming MoE
* **Integration Point**: `omlx/models/` and `omlx/custom_kernels/`.
* **Mechanism**: Custom metal kernels (e.g. `glm_moe_dsa`) are already supported via C++ bindings. Streaming MoE will require adding new kernels and registering the model adapter to utilize them during the `FORWARD` pass.

## 4. Future Execution Algorithms / Dynamic Execution Planning
* **Integration Point**: `omlx/scheduler.py` (`SchedulerHooks`).
* **Mechanism**: The scheduler already supports `SchedulingPolicy`. A dynamic planner could be implemented as a new policy or a hook that evaluates context/memory state before `add_request` or `step`.

## 5. Capability Negotiation & Profiles
* **Integration Point**: `omlx/registry/capability_registry.py`.
* **Mechanism**: Ensure any new model type registers its execution graph requirements (e.g., requires Diffusion vs Autoregressive) during plugin discovery.
