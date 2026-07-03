# Architecture Recommendations & Assessment

## Architecture Recommendations

1. **Decouple Scheduler from `BatchGenerator`**: The Scheduler currently relies heavily on `mlx-lm`'s internal `BatchGenerator`. To support more exotic models (e.g., Diffusion, custom MoE strategies) without heavy monkey-patching, OMLX should define its own abstract execution node runner interface.
2. **Standardize Patching**: `omlx/patches` is a critical stability risk. Establish a formal upstreaming process or a plugin-based patching system so the core engine does not break when `mlx-lm` bumps its version.
3. **Formalize Memory Primitives**: Relying on timed delays for IOKit memory clearing (`_DEFERRED_CLEAR_DELAY`) is fragile. Investigate tighter integration with Apple's Metal Performance Shaders for deterministic memory reclamation.
4. **Expand Experimental Diffusion Integration**: The experimental diffusion backend should be fully promoted and tested against the standard `EngineCore` lifecycle, integrating it seamlessly into the `EnginePool`.

## GO / NO-GO Assessment

**Decision**: **GO**

**Justification**:
The repository architecture is well-structured, discoverable, and successfully implements complex concepts like continuous batching and Paged SSD caching on top of MLX.
* Critical runtime ownership between `EnginePool`, `EngineCore`, and `Scheduler` is clear and verifiable via the codebase.
* Extension points (Capabilities, Plugins, Profiles) are established and mostly stable.
* Testing coverage is high, particularly for the core scheduler and cache components, providing a strong safety net for future development.

No major architectural contradictions were discovered that would prevent the integration of future capabilities (Diffusion LMs, Streaming MoE). The path forward is clear and documented in the Checkpoint Roadmap.
