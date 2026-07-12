<p align="center">
  <img src="docs/assets/logo.png" width="180" alt="One Logo">
</p>

<h1 align="center">One</h1>

<p align="center">
<b>Compiler-Native AI Execution Platform</b><br>
Plan Once • Execute Anywhere
</p>

<p align="center">

![macOS](https://img.shields.io/badge/macOS-Supported-black)
![Linux](https://img.shields.io/badge/Linux-Roadmap-blue)
![Windows](https://img.shields.io/badge/Windows-Roadmap-blue)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB)
![SwiftUI](https://img.shields.io/badge/SwiftUI-Native-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![MIT](https://img.shields.io/badge/License-MIT-green)
![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-Optimized-black)

</p>

---

# Why One?

**One** is a compiler-native AI execution platform that transforms high-level execution intent into deterministic execution plans capable of running across multiple AI runtimes, hardware platforms, and model formats.

Instead of binding applications to a single inference engine, One introduces a planning layer that separates **intent**, **planning**, **execution**, and **observation**, enabling a unified architecture across diverse AI ecosystems.

---

# Why the Rename?

**One** is the evolution of **oMLX**.

The original project focused on MLX-based local inference. As the architecture expanded beyond a single backend into a compiler-native execution platform, the project outgrew its original name.

The new name reflects the vision:

- **One Runtime**
- **One Architecture**
- **One Planning System**
- **Many Platforms**
- **Many Backends**
- **Many Models**

The history, contributors, and architectural foundations of **oMLX** remain acknowledged and preserved.

---

# Vision

> Build a universal execution layer for AI.

Applications should express **what** they want to accomplish—not **how** a particular runtime executes it.

One compiles execution intent into optimized execution plans that can target multiple inference engines without changing application code.

---

# How One Compares

| Project | Primary Focus |
|---------|----------------|
| Ollama | Local model management and inference |
| llama.cpp | High-performance inference engine |
| MLX | Apple Silicon tensor framework |
| vLLM | High-throughput LLM serving |
| **One** | Compiler-native AI execution platform with planning, execution strategies, and backend abstraction |

---

# Key Features

- Compiler-native execution pipeline
- Immutable execution descriptors
- Planning domains
- Execution strategies
- Runtime abstraction
- Backend adapters
- Native desktop application
- Web dashboard
- CLI
- OpenAI-compatible API
- Plugin architecture
- Model management
- Observability
- Benchmarking
- Quantization workflows

---

# Architecture

```text
                Intelligence
                     │
                     ▼
         Immutable Descriptors
                     │
                     ▼
            Planning Domains
                     │
                     ▼
             Planning Bundle
                     │
                     ▼
                Compiler
                     │
                     ▼
                 Runtime
                     │
          Execution Strategy
                     │
                     ▼
            Execution Engine
                     │
                     ▼
            Backend Adapter
                     │
                     ▼
                AI Backend

                     │

              Observation
```

## Philosophy

```text
Intent
   │
   ▼
Planning
   │
   ▼
Execution
   │
   ▼
Observation
```

---

# Screenshots

> Placeholder for:

- Native Desktop App
- Web Dashboard
- Chat
- Models
- Downloads
- Benchmarks
- Settings

---

# Quick Start

```bash
git clone https://github.com/your-org/one.git
cd one
pip install -e .
one serve
```

---

# Installation

Instructions for Python package installation, source builds, and platform-specific installers will be documented here.

---

# Native Desktop App

SwiftUI-based desktop experience for local AI execution, model management, downloads, benchmarking, and observability.

---

# Web Dashboard

A browser-based interface for managing models, monitoring execution, interacting with chat, and configuring runtime settings.

---

# CLI

```bash
one chat
one serve
one models
one benchmark
```

---

# Supported Models

Supports local and remote foundation models through backend adapters.

---

# Supported Formats

- MLX
- GGUF
- Safetensors
- Hugging Face
- ONNX *(Roadmap)*

---

# Supported Backends

## Current

- MLX

## Roadmap

- llama.cpp
- CUDA
- TensorRT
- ROCm
- OpenVINO
- Core ML
- ONNX Runtime
- Vulkan

---

# Supported Platforms

| Platform | Status |
|----------|--------|
| macOS | ✅ |
| Linux | 🚧 |
| Windows | 🚧 |

---

# Documentation

- Architecture
- Compiler
- Runtime
- Scheduler
- Execution Engine
- Backend Adapters
- Planning
- Plugins
- API
- Native App

---

# Roadmap

## Compiler
- Planning optimization
- Incremental compilation

## Runtime
- Multi-backend scheduling
- Distributed execution

## Planning
- Advanced planning domains
- Cross-runtime optimization

## Execution
- Strategy expansion
- Dynamic backend selection

## Observation
- Runtime tracing
- Metrics and diagnostics

## Interfaces
- Desktop
- Web
- CLI
- SDKs

---

# Contributing

Contributions are welcome.

Please open an issue to discuss major architectural changes before submitting large pull requests.

---

# Credits

**One** is the evolution of the original **oMLX** project.

The original architecture, implementation, and contributors remain acknowledged.

The rename reflects the expansion from an MLX-centric inference system into a backend-independent compiler-native AI execution platform.

---

# License

MIT License

---

<p align="center">

## One

**Compiler-Native AI Execution Platform**

**Plan Once. Execute Anywhere.**

</p>
