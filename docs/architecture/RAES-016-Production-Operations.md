# RAES-016 — Production Readiness, Operations & Release Architecture

## Context
The oMLX architecture is largely complete, establishing the core execution flows, capability registries, plugin subsystems, and architectural constraints. RAES-016 does not redefine the runtime. It defines how oMLX is operated safely in production, serving as the operational handbook for deploying, maintaining, verifying, monitoring, benchmarking, releasing, and recovering oMLX in real-world environments.

---

## 1. Production Readiness Audit
A successful production deployment of oMLX requires transitioning from development assumptions to production rigor.

### Identified Areas:
*   **Production Assumptions**: Resources must be bounded; hardware capabilities are immutable at startup (via `ExecutionEnvironment`); configurations load deterministically.
*   **Development Assumptions**: Overly verbose logging, lazy model downloads without checksum verification, and implicit global states (like `_server_state`) are removed.
*   **Debugging Code**: Debugging endpoints must be disabled or guarded behind strict authentication in production.
*   **Feature Flags**: Defined via the `CapabilityRegistry` (e.g., `OMLX_USE_NEW_RESOLVER`) to allow safe rollout of new execution paths (e.g., Streaming MoE) alongside stable features.
*   **Logging & Metrics**: Shift from unstructured print statements to structured JSON logging (e.g., `structlog`) and metrics via OpenTelemetry integration.
*   **Health Endpoints**: Must differentiate between API liveness, model readiness (health), and worker capacity.
*   **Configuration Loading**: Strict precedence established (Env Vars > CLI > API > Config Files > Profiles > Defaults).
*   **Benchmark Tooling**: Moving from local scripts to automated CI benchmark gates.
*   **Profiling Tools**: Memory and GPU usage profiling should be opt-in, not continuously active, to minimize overhead.
*   **CI Integration & GitHub Workflows**: Shift from simple unit tests to multi-stage CI pipelines encompassing HF Equivalence, golden asset verification, and performance bounds.
*   **Release Tooling, Packaging, & Installation Scripts**: Move from source-based ad-hoc installs to versioned artifacts, PyPI packages, Docker images, and Homebrew formulae.
*   **Dependency Management**: Deterministic dependency locking for MLX, transformers, and FastAPI.

### Production Readiness Matrix
| Component | Development State | Production State | Gap to Close |
| :--- | :--- | :--- | :--- |
| **Model Fetching** | Dynamic HF Hub downloads | Pre-fetched, cached, hash-verified | Implement strict offline/verified model loading |
| **Telemetry** | stdout / print | OpenTelemetry, Structured Logs | Add OTel exporter, standardize log context |
| **Hardware Constraints** | Assumed unlimited | Bounded by `ExecutionEnvironment` limits | Enforce Memory Budgeting and backpressure |
| **Startup** | Single thread blocking | Parallel pre-flight, lazy capability eval | Optimize Plugin initialization times |

---

## 2. Operational Architecture

The operational architecture defines the lifecycle from code to production execution.

```mermaid
flowchart TD
    Developer([Developer]) --> CI[CI Pipeline]
    CI --> Verification[Verification Pipeline]
    Verification --> Benchmark[Benchmark Pipeline]
    Benchmark --> ReleaseValidation[Release Validation]
    ReleaseValidation --> ArtifactPublishing[Artifact Publishing]
    ArtifactPublishing --> Deployment[Deployment]
    Deployment --> RuntimeMonitoring[Runtime Monitoring]
    RuntimeMonitoring --> Maintenance[Maintenance & Iteration]
```

---

## 3. Deployment Architecture

oMLX targets various deployment topologies, prioritizing Apple Silicon but retaining future-proof flexibility.

```mermaid
graph TD
    subgraph Client/Edge
        Desktop[Apple Silicon Desktop]
        AirGapped[Offline Air-Gapped Systems]
    end
    subgraph Server/Cloud
        Linux[Linux Server]
        Docker[Docker Containers]
        K8s[Kubernetes Cluster]
    end
    subgraph Hardware Backends
        Metal[Apple Metal]
        CUDA[Nvidia CUDA]
        ROCm[AMD ROCm]
    end
    Desktop --> Metal
    Linux --> CUDA
    Linux --> ROCm
    Docker --> Linux
    K8s --> Docker
```

### Deployment Strategies:
*   **Local Development**: Requirements: macOS/Linux, Python 3.10+. Supported: All features. Limitations: Single node.
*   **Apple Silicon Desktop**: Recommended config: M2/M3/M4 Max/Ultra. High memory bandwidth is crucial. Full MLX support.
*   **Linux Server / CUDA / ROCm**: Requirements: Fallback to PyTorch/XLA if MLX not available (or future MLX Linux support).
*   **Docker / Kubernetes**: Requirements: Containerized runtime. Supports stateless autoscaling. Resource limits must map to `ExecutionEnvironment` budgets.
*   **Distributed Cluster / Cloud**: Distributed inference via future remote worker plugins.
*   **Offline Air-Gapped**: Requires pre-downloaded Model Adapters, weights, and configurations. No dynamic Hub fetching permitted.

---

## 4. Runtime Reliability

Supervision and recovery ensure the inference server remains available despite partial failures.

```mermaid
stateDiagram-v2
    [*] --> Startup
    Startup --> Healthy: Initialization Complete
    Healthy --> Degraded: Worker Crash / OOM Warning
    Degraded --> Recovery: Graceful Restart / Request Draining
    Recovery --> Healthy: Resources Reallocated
    Degraded --> Critical: Unrecoverable Fault
    Critical --> Shutdown: System Exit
    Shutdown --> [*]
```

### Key Mechanisms:
*   **Worker Supervision**: An outer process or orchestration layer (like Kubernetes/systemd) supervises the oMLX process. Internally, the `EnginePool` supervises `EngineCore` instances.
*   **Graceful Shutdown & Request Draining**: Stop accepting new requests, finish executing active batches, clean up KV caches, and exit cleanly.
*   **Crash Recovery**: Terminate stuck inference loops (timeout policy), clear corrupted Metal memory, and restart the worker.
*   **Partial Failure Handling**: If an optional Plugin fails initialization, mark it degraded but continue serving core inference (if configured to tolerate it).
*   **Retry & Timeout Policies**: Configured at the API routing layer; failed requests return a 503 rather than holding connections indefinitely.

---

## 5. Health Monitoring

Differentiating between subsystem health states allows orchestrators to route traffic intelligently.

```mermaid
flowchart LR
    Probe(Health Probe) --> Core[EngineCore]
    Core --> H1{Model Health}
    Core --> H2{GPU/Mem Health}
    Core --> H3{Plugin Health}
    Core --> H4{Scheduler Health}
```

### Defined States:
*   **Healthy**: System is ready and operating within standard latency/memory bounds.
*   **Warning**: System is functional but nearing memory capacity or experiencing elevated P99 latency.
*   **Critical**: Deadlock, persistent OOM, or hardware failure. Requires restart.
*   **Recovery**: System is actively draining requests or reloading a model. Not accepting new traffic.

---

## 6. Observability Architecture

Observability provides deep visibility without degrading inference throughput.

```mermaid
flowchart TD
    App[oMLX Runtime] --> Log[Structured Logging]
    App --> Metrics[Metrics Counter]
    App --> Traces[OpenTelemetry Traces]
    Log --> Agg[Log Aggregation]
    Metrics --> Prom[Prometheus/Grafana]
    Traces --> Jaeger[Jaeger / APM]
```

### Components:
*   **Metrics**: Track TTFT (Time To First Token), TPS (Tokens Per Second), Latency (P50/P95/P99), Cache Hit Rate, Scheduler Overhead.
*   **Tracing**: Trace the lifecycle of a request from API -> Scheduler -> Execution Planner -> Backend -> Response.
*   **Diagnostics**: Crash dumps capture the `ExecutionEnvironment` and `ExecutionGraph` to diagnose failed executions.

---

## 7. Performance Architecture

Production benchmarking must be continuous.

### Tracked Metrics:
*   **Throughput & Latency**: TTFT, TPS, end-to-end latency.
*   **Resource Utilization**: Peak Memory, GPU/CPU Utilization.
*   **Overhead**: Scheduler queueing time, Execution Pipeline traversal time, IR Optimization Cost, Plugin Initialization Cost.

---

## 8. Capacity Planning

*   **Memory Budgeting**: The system calculates total available RAM and reserves a fixed percentage for KV cache, model weights, and OS overhead, enforcing strict backpressure when bounds are reached.
*   **Queue Sizing**: Maximum queue depth prevents unbounded memory growth from pending requests.
*   **Autoscaling**: Rely on metrics (e.g., active queue depth) exported to K8s HPA to scale stateless replicas.

---

## 9. Security Architecture

*   **Plugin Trust Model**: Plugins must be explicitly registered and ideally signed.
*   **Model Validation**: Models loaded from disk must match expected SHA256 hashes to prevent execution of tampered tensors.
*   **Configuration Validation**: Strict parsing of inputs (e.g., Pydantic models) to prevent injection attacks at the API layer.
*   **Sandboxing**: Limit file system access to the defined model cache directories.

---

## 10. Release Engineering

```mermaid
flowchart LR
    Dev[Development] --> Nightly[Nightly]
    Nightly --> Exp[Experimental]
    Exp --> Alpha[Alpha]
    Alpha --> Beta[Beta]
    Beta --> Stable[Stable/LTS]
```

### Promotion Criteria:
*   To Beta: Feature complete, passes HF Equivalence, no critical bugs.
*   To Stable: Proven under benchmark loads, documentation complete, passes all CI regression gates.

---

## 11. CI/CD Architecture

```mermaid
flowchart TD
    PR[Pull Request] --> UT[Unit Tests]
    PR --> Lint[Code Quality/Lint]
    UT --> IT[Integration Tests]
    IT --> Arch[Architecture Validation]
    Arch --> HF[HF Equivalence & Golden Assets]
    HF --> Perf[Performance Gates]
    Perf --> Merge[Merge to Main]
```

Gates include Model Adapter validation, Execution Graph generation checks, and Plugin compatibility testing.

---

## 12. Distribution Architecture

oMLX artifacts are distributed via:
*   **PyPI**: Standard `pip install omlx` (Source/Wheel).
*   **Docker**: Pre-configured environments (`ghcr.io/omlx/...`).
*   **Homebrew**: `brew install omlx` for macOS native execution.
*   **GitHub Releases**: Pre-compiled binary bundles.

---

## 13. Disaster Recovery

```mermaid
flowchart TD
    Fail[Failure Detected] --> Diagnose{Failure Type}
    Diagnose --> |Corrupted Cache| Clean[Purge Cache & Restart]
    Diagnose --> |Worker Crash| Restart[Restart Worker Process]
    Diagnose --> |Bad Plugin| Isolate[Disable Plugin & Fallback]
    Diagnose --> |Broken Model| Rollback[Rollback to Last Known Good Model]
```
Partial deployments are automatically rolled back if health checks fail to reach 'Healthy' within a grace period.

---

## 14. Maintenance Strategy

*   **Cache Cleanup**: Automated scripts to prune unused models/KV cache data.
*   **Baseline Refresh**: Periodically update golden assets and HF equivalence baselines as upstream `transformers` or `mlx` libraries change.
*   **Dependency Upgrades**: Lock dependencies tightly but schedule monthly reviews for performance patches.

---

## 15. Documentation Architecture

Structure for public documentation:
*   **Developer Docs**: Contributing, building from source.
*   **Architecture Docs**: RAES specs, component ownership.
*   **Operator Handbook**: Deployment guides, capacity planning, configuration reference.
*   **Troubleshooting Guide**: Common errors, metric definitions.
*   **Plugin & Adapter Docs**: How to extend the runtime.

---

## 16. Production Readiness Checklist

*   [ ] Architecture Complete (RAES-001 through RAES-016 adhered to)
*   [ ] Verification Passing (Unit, Integration, HF Equivalence)
*   [ ] Benchmarks Passing (No TPS regressions)
*   [ ] Health Checks Configured
*   [ ] Structured Logging & Metrics Enabled
*   [ ] Rollback Procedures Documented
*   [ ] Security Review Completed (Input validation, Model hashes)

---

## 17. Future Operational Roadmap

The operational architecture natively supports future extensions (e.g., Diffusion, Streaming MoE, Distributed Inference) without structural changes, as these are exposed via the `CapabilityRegistry` and `ExecutionPlanner`. The monitoring stack simply sees new capabilities; it does not require redesigning K8s deployments or health probes.

---

## 18. Verification Strategy

Operational verification goes beyond unit tests:
*   **Deployment Validation**: Ensuring Docker/Brew packages install and run correctly on fresh systems.
*   **Recovery Validation**: Injecting faults (e.g., killing the EngineCore) and verifying the Supervisor restarts it.
*   **Capacity Validation**: Load testing to ensure backpressure mechanisms prevent OOM errors under high concurrency.

---

## 19. Rollback Strategy

*   **Feature Flags**: Rapidly toggle execution logic (e.g., turn off a speculative adapter) via configuration, without a binary release.
*   **Release Rollback**: Keep previous Docker tags/PyPI versions immutable so orchestrators can instantly revert.
*   **Configuration Rollback**: Store configurations as code (GitOps) to allow fast reversion of memory limits or scheduler queue sizes.
