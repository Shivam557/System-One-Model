# Open Decision Model (ODM)

**An open-source, reusable decision-making engine for applications, agents, games, and simulations.**

ODM is a research and engineering project to build a model that accepts structured decision requests and returns structured results. It is designed to be reusable through a Python SDK, HTTP API, and Model Context Protocol (MCP) adapter.

> **Development status:** Early development. The project foundation and initial decision contracts are documented. The neural model, training pipeline, and integrations are planned and have not yet been implemented.

## Vision

Build one reusable decision-making brain that different applications can call instead of creating a separate decision interface for every use case.

An application supplies the context, objective, candidate options, and constraints. ODM evaluates the request and returns a structured decision. The calling application remains responsible for permissions, safety checks, and executing any action.

## Planned Decision Modes

| Mode | Purpose | Example |
|---|---|---|
| Noul | Binary decision | Is this option eligible? |
| Choice | Categorical selection | Which route should be selected? |
| Score | Ordered rating | How suitable is this candidate? |
| Box | Bounded numeric value | What target value is within these limits? |

The exact schemas and validation rules are documented in [`docs/decision-contracts.md`](docs/decision-contracts.md).

## Planned Architecture

The project is designed around five main layers:

1. **Decision contracts** — shared request and response formats.
2. **Core decision engine** — validates requests and coordinates decisions.
3. **Model** — a small, randomly initialized Transformer-based model built with PyTorch.
4. **Integrations** — Python SDK, HTTP API, and MCP adapter.
5. **Evaluation and training** — datasets, training experiments, benchmarks, and confidence calibration.

See [`docs/architecture.md`](docs/architecture.md) for the architecture plan.

## Project Roadmap

- [x] Establish the Python package and repository structure.
- [x] Configure initial tests and linting.
- [x] Document the planned architecture and decision contracts.
- [ ] Implement typed decision requests and responses.
- [ ] Build the initial neural decision model.
- [ ] Create datasets and a reproducible training pipeline.
- [ ] Evaluate decision quality and inference performance.
- [ ] Investigate confidence calibration and feedback-based learning.
- [ ] Add the Python SDK, HTTP API, and MCP adapter.
- [ ] Publish examples and prepare a versioned release.

A planned feature is not considered implemented until it has working code and appropriate tests.

## Requirements

- Python 3.11 or newer.
- Git.
- Conda is recommended for local environment management.

The initial development target is CPU-only hardware. Actual model size, memory use, latency, and decision quality will be measured as the project develops.

## Development Setup

Clone the repository and enter its directory:

```bash
git clone <your-github-repository-url>
cd System-One-Model
```

Create and activate the Conda environment:

```bash
conda create -n odm python=3.11
conda activate odm
```

Install the project and development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the tests:

```bash
pytest -v
```

Run the linter:

```bash
ruff check src tests
```

The editable installation allows Python to use the source code in your working repository without reinstalling the package after every code change.

## Repository Structure

```text
System-One-Model/
├── artifacts/       # Selected model artifacts
├── configs/         # Model and experiment configurations
├── data/            # Dataset guidance and local data
├── docs/            # Architecture and decision contracts
├── examples/        # Usage examples
├── experiments/     # Training and evaluation experiments
├── src/
│   └── odm/         # ODM Python package
├── tests/           # Automated tests
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

Large datasets, model checkpoints, secrets, and generated experiment outputs should not be committed by default.

## Design Principles

- **Reusable:** one decision interface for multiple applications.
- **Structured:** explicit request schemas and predictable result formats.
- **Modular:** separate the core model from its integrations.
- **Testable:** verify behavior with automated tests and controlled experiments.
- **Reproducible:** track configurations, seeds, and evaluation results.
- **Resource-conscious:** begin with small models suitable for CPU experimentation.
- **Controlled execution:** the model returns decisions; external systems retain control over action execution.

## Research and Limitations

A randomly initialized Transformer does not begin with general-purpose knowledge. It must learn from training data, and its abilities must be established through evaluation.

Supporting several decision modes does not by itself guarantee competence across unrelated tasks.

Performance, generalization, and confidence calibration will be reported only when supported by experiments. Any exploration of RLCD-style or reward-based learning will be documented according to the methods actually implemented.

## Contributing

The project is being developed incrementally. Contributions should include clear explanations, tests for new behavior, and reproducible instructions for experiments.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE) for details.
