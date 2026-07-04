# Model Adapter Architecture Plan

## Executive Summary

This document outlines the architectural plan for introducing a Model Adapter Architecture into oMLX. The primary goal is to decouple model-specific quirks, monkey patches, and lifecycle management from the generic runtime (`ExecutionEngine`, `ExecutionBackend`, `Scheduler`, `EngineCore`). The new design supports future model families (Diffusion, Streaming MoE, Verification) without requiring invasive changes to the core scheduling or execution loop.

## 1. Repository Audit: Current State

Our audit of the codebase reveals model-specific logic leaked into several layers:

1. **Monkey Patches (`omlx/patches/`)**:
   - `maybe_apply_pre_load_patches` in `omlx/utils/model_loading.py` dispatches model-specific pre-load patches (e.g., DeepSeek V4, Llama 4, GLM DSA, Step 3.7).
   - Patches are deeply tied to `config.json` `model_type` values.

2. **Engines (`omlx/engine/`)**:
   - `BatchedEngine`, `DFlashEngine`, `VLMBatchedEngine` have hardcoded checks for `model_type` strings to toggle features (e.g., `model_type == "gemma4"`, `is_qwen`, etc.).
   - Modality mapping and hardware capability toggles are hardcoded in engine classes.
   - Specific VLM prompt engineering rules, chat template overrides, and image processing constraints exist in `vlm.py`.

3. **Inference Pipeline (`omlx/inference/`)**:
   - Specific model properties are currently exposed or leaked to pipeline construction.

4. **Configuration & Capabilities**:
   - Architecture detection and STS family mapping are hardcoded in `sts.py` and `api/utils.py`.

**Inventory of areas to extract to adapters**:
- Model loading hook pre/post initialization
- Architecture detection and configuration validation
- Tokenizer preparation and quirks
- RoPE scaling logic and overrides
- Attention mask generation rules (e.g., block masks, streaming)
- KV cache layout specifications
- Expert routing/Streaming MoE constraints
- Chat template quirks and image/audio token handling
- Hardware/optimizations hints

## 2. Adapter Architecture

### Design Philosophy
The runtime components (`Scheduler`, `EngineCore`, `ExecutionBackend`, `ExecutionEngine`) will remain untouched. Instead, models will be managed by a `BaseModelAdapter`. The adapter will act as the unified interface between a specific model architecture and the runtime pipeline.

### Adapter Hierarchy

We will use **composition over multiple inheritance** to handle models with overlapping capabilities (e.g., Vision + MoE, Diffusion + Verification) to avoid the diamond problem. However, the foundational families will be defined as an inheritance tree.

```text
BaseModelAdapter
        │
        ├──────── DenseTransformerAdapter
        │
        ├──────── DiffusionAdapter
        │
        ├──────── MoEAdapter
        │
        ├──────── VisionAdapter
        │
        ├──────── AudioAdapter
        │
        └──────── EmbeddingAdapter
```

**Reasoning for Composition**:
For composite models (e.g., "Vision + MoE"), a `ModelAdapter` might instantiate or delegate to a `VisionCapability` and an `MoECapability` internally. The runtime only queries the unified adapter interface.

### Adapter Responsibilities

The adapter defines:
1. `prepare_config(config_dict)`: Fixes up raw `config.json`.
2. `apply_patches()`: Applies any necessary monkey-patches before model load.
3. `load_model(weights_path)`: Actually instantiates the model object.
4. `prepare_tokenizer(tokenizer)`: Handles tokenizer quirks (special tokens, chat templates).
5. `get_execution_hints()`: Returns hardware, caching, or scaling hints.
6. `build_attention_mask(context)`: Generates required mask tensors.
7. `get_capabilities()`: Returns a `ModelCapabilityProfile`.

## 3. Future Execution Families Integration

The design cleanly isolates future functionality:

- **Nemotron Labs Diffusion / DiffusionGemma**: Will implement `DiffusionAdapter`, providing iterative denoising metadata, block masks, and custom scheduling hooks via the adapter interface, not by changing `ExecutionBackend`.
- **Nemotron Triage**: Will use an adapter that provides verification hooks and draft generation metadata.
- **Streaming MoE**: An `MoEAdapter` will provide expert routing and partial loading hints that the `ExecutionBackend` uses without knowing it's an MoE.

## 4. Interaction with Runtime

**Current Flow**:
Model Load -> Engine Instantiation -> Backend Execution

**New Flow**:
Model Discovery -> Registry resolves `BaseModelAdapter` -> Adapter configures capabilities -> Profile built -> `ExecutionBackend` initialized with Profile -> `ExecutionEngine` executed.

The `ExecutionBackend` will query the adapter for masks, cache layouts, and processing instructions, remaining agnostic to whether the model is a Transformer or a Diffusion model.

## 5. Interaction with Verification Framework

Adapters will expose a verification metadata interface:
- `get_verification_metadata()`: Returns expected tolerance levels, golden prompt sets, and HF equivalency targets.
- This allows `verification_framework.md` to automatically pull testing parameters directly from the adapter rather than maintaining parallel config files.

## 6. Risk Analysis

1. **Adapter Explosion**: Risk of creating a new adapter for every minor model variation. *Mitigation*: Group by architecture families, use composable capability traits instead of deep inheritance.
2. **Upstream MLX Changes**: Breaking changes in MLX could break adapters. *Mitigation*: Adapters isolate the blast radius; runtime remains safe.
3. **Monkey Patch Isolation**: Unloading patches is hard. *Mitigation*: Adapters should document patch scopes clearly; ideally patches are applied once per worker process.

## 7. Verification Plan (No Implementation)

- **Adapter Registration Test**: Verify models resolve to the correct adapter subclass.
- **Configuration Parsing Test**: Verify adapters correctly transform raw `config.json` inputs.
- **Metadata Exposure Test**: Ensure `get_execution_hints` and `get_capabilities` return valid schemas.
- **Tokenizer Handling Test**: Test that tokenizer special tokens are correctly configured by the adapter.
- **Runtime Compatibility Test**: Mock the adapter interface and ensure `ExecutionBackend` can process a dummy forward pass without architecture-specific code.

## 8. Files to Modify / Create

**NEW**:
- `omlx/adapter/base.py`: Defines `BaseModelAdapter` and capability interfaces.
- `omlx/adapter/transformer.py`: `DenseTransformerAdapter`.
- `omlx/adapter/moe.py`: `MoEAdapter`.
- `omlx/adapter/vlm.py`: `VisionAdapter`.
- `omlx/adapter/factory.py`: Registration and resolution logic.
- `omlx/adapter/models/`: Directory for specific model implementations if they can't fit generic families.

**MODIFIED**:
- `omlx/utils/model_loading.py`: Delegate pre-load patches to the adapter factory.
- `omlx/engine_pool.py`: Use adapter for metadata extraction instead of hardcoding `model_type` checks.
- `omlx/engine/vlm.py` (and others): Remove `is_qwen`, `model_type == "gemma4"` logic, delegate to adapter.

**UNTOUCHED**:
- `Scheduler`
- `ExecutionBackend`
- `ExecutionEngine`
- `Server`

## Recommendation for Next Checkpoint
The next checkpoint should focus exclusively on creating `omlx/adapter/base.py`, `omlx/adapter/factory.py`, and porting one simple model (e.g., a standard dense transformer) to the adapter architecture to validate the interface before migrating complex VLMs or MoEs.

## 9. Rollback Strategy

Since the adapter migration touches model initialization and monkey patches, any issues could prevent models from loading.

**Strategy**:
1. **Side-by-Side Implementation**: The `AdapterFactory` and initial adapters (e.g., `DenseTransformerAdapter`) will be introduced alongside existing `load_text_model` and engine factory logic.
2. **Feature Flagging**: The migration will be gated behind an environment variable (e.g., `OMLX_USE_ADAPTERS=1`). If the flag is absent or `0`, the system will fall back to the legacy `model_type` string checking and patch dispatch in `model_loading.py`.
3. **Incremental Migration**: Models will be migrated to the adapter system one family at a time (e.g., Dense Transformers first, then MoE, then VLM, then Diffusion). This allows for reverting specific model families without rolling back the entire architecture.
4. **Fast Revert**: If an adapter causes regression in production, removing the adapter registration mapping for that `model_type` will instantly revert it to the legacy codepath.
