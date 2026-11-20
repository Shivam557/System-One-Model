# Open Decision Model (ODM) — Architecture

## 1. Purpose

The Open Decision Model (ODM) is an open-source project for building a reusable, structured decision-making engine.

ODM accepts a decision request, evaluates the supplied context and available options, and returns a structured result that another application can interpret.

The project aims to support games, autonomous agents, simulations, shopping systems, and other applications that need consistent decision interfaces.

## 2. Design Principles

- **Reusable:** One decision engine should support multiple applications.
- **Structured:** Inputs and outputs should follow explicit schemas.
- **Modular:** The core engine should remain separate from APIs, SDKs, and integrations.
- **Testable:** Decision behavior should be measurable through automated tests and benchmarks.
- **Reproducible:** Experiments should record configurations, seeds, and evaluation results.
- **Resource-conscious:** Initial development should support CPU-only machines with limited memory.
- **Safe by design:** ODM recommends or selects actions; the calling application remains responsible for executing them and enforcing permissions.

## 3. High-Level Architecture

The project is organized into five conceptual layers.

### 3.1 Decision Contract Layer

Defines the request and response formats shared by every integration.

A request can contain:
- A decision mode.
- Context or state information.
- A question or decision objective.
- Candidate options, when applicable.
- Constraints and optional metadata.

A response can contain:
- The selected value or candidate.
- A score or ranking when supported by the decision mode.
- A confidence estimate when available.
- Diagnostic metadata where appropriate.

### 3.2 Core Decision Layer

Provides the common interface for making decisions.

It validates requests, routes them to the appropriate decision mode, invokes the configured decision backend, and returns a structured result.

The core must not depend on a particular HTTP framework, MCP transport, or game engine.

### 3.3 Model Layer

Contains the learnable decision model and its inference components.

The initial research model will use PyTorch and a randomly initialized Transformer encoder. It will not rely on pretrained weights as a project dependency.

Training, evaluation, and inference will be kept separate so that model improvements can be measured independently.

### 3.4 Integration Layer

Exposes the same core decision functionality through:
- A Python SDK.
- An HTTP API.
- A Model Context Protocol (MCP) adapter.

These integrations are interfaces to the brain, not separate decision engines. They must not silently change the meaning of a decision request.

### 3.5 Evaluation Layer

Measures decision quality and operational performance.

Evaluation will cover:
- Correctness on controlled test cases.
- Candidate-selection quality.
- Latency and throughput.
- Confidence calibration.
- Reproducibility across experiments.

Performance claims must be supported by benchmarks on documented hardware and configurations.

## 4. Decision Modes

ODM plans to support four typed decision modes.

- **Noul:** A binary decision, such as true or false.
- **Choice:** Selection from a set of categorical options.
- **Score:** Assignment of an ordered score or rating.
- **Box:** Selection or prediction of a value within defined bounds.

The precise schemas, validation rules, and response formats will be defined in `docs/decision-contracts.md`.

## 5. Candidate Evaluation

Some requests may supply multiple candidate actions or options.

ODM may evaluate candidates in batches and rank them using model outputs. Batching can improve throughput, but it does not guarantee lower latency for every request.

The calling application supplies the candidates and decides what to do with the result. ODM does not independently execute arbitrary tools, spend money, or perform external actions.

## 6. Training and Research

The project will begin with controlled synthetic datasets and reproducible experiments.

Later stages may investigate:
- Supervised learning from labeled decision examples.
- Candidate-ranking objectives.
- Confidence calibration and expected calibration error (ECE).
- Reward-based learning and feedback-driven experiments.

Any RLCD-style implementation will be documented as an independent research approximation unless a specific public method can be reproduced from reliable documentation. ODM will not claim access to proprietary architectures, model weights, or undocumented training recipes.

## 7. Repository Organization

- `src/odm/` — reusable Python package and decision engine.
- `tests/` — automated tests.
- `configs/` — model and experiment configurations.
- `data/` — dataset documentation and local dataset locations.
- `docs/` — architecture and decision contracts.
- `experiments/` — training and evaluation experiments.
- `examples/` — example integrations and requests.
- `artifacts/` — designated location for selected model artifacts.

Generated datasets, checkpoints, and experiment outputs should not be committed unless explicitly required for a documented, reproducible example.

## 8. Development Sequence

Development will proceed incrementally:

1. Establish project structure and contracts.
2. Implement and test typed decision requests and responses.
3. Build the initial model and inference path.
4. Create datasets and a reproducible training pipeline.
5. Evaluate candidate ranking and performance.
6. Investigate calibration and feedback-based learning.
7. Add the Python SDK, HTTP API, and MCP adapter.
8. Document usage and prepare a versioned release.

## 9. Current Limitations

A randomly initialized model does not begin with general-purpose knowledge. Its decision quality must be learned and evaluated.

A universal request format makes ODM reusable at the interface level; it does not automatically make an untrained model competent across unrelated tasks.

Confidence values will not be treated as calibrated probabilities unless evaluation supports that interpretation.

The architecture is an evolving research and engineering plan. Implemented capabilities must be distinguished from planned features.
