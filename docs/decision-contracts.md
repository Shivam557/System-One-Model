# ODM Decision Contracts

## 1. Purpose

This document defines the planned input and output contracts for the Open Decision Model (ODM).

Every integration must use the same underlying decision semantics. The Python SDK, HTTP API, and MCP adapter must not invent different interpretations of a decision.

These contracts describe the initial design. They will be implemented and tested in later development stages.

## 2. General Decision Request

A decision request contains the information ODM needs to evaluate a problem.

Conceptual JSON example:

```json
{
  "request_id": "example-001",
  "mode": "choice",
  "objective": "Select the most suitable route",
  "context": {
    "weather": "clear",
    "time_available_minutes": 30
  },
  "candidates": [
    {
      "id": "route-a",
      "description": "Short route with heavy traffic"
    },
    {
      "id": "route-b",
      "description": "Longer route with light traffic"
    }
  ],
  "constraints": {},
  "metadata": {}
}
```

### Request fields

- `request_id`: Optional identifier supplied by the caller.
- `mode`: Required decision mode.
- `objective`: Description of the decision to make.
- `context`: Information relevant to the decision.
- `candidates`: Optional list of available choices or actions.
- `constraints`: Optional restrictions the decision must respect.
- `metadata`: Optional application-specific information.

The initial implementation will validate the mode and required fields. More detailed validation rules will be added alongside the typed request models.

## 3. Noul — Binary Decisions

Noul represents a decision with two possible outcomes: `true` or `false`.

Example request:

```json
{
  "mode": "noul",
  "objective": "Is the item eligible?",
  "context": {
    "price": 25,
    "maximum_price": 50
  }
}
```

Conceptual response:

```json
{
  "mode": "noul",
  "value": true
}
```

The Boolean value represents the model's decision. It is not automatically a guarantee that the decision is correct.

## 4. Choice — Categorical Decisions

Choice selects one option from a supplied set of candidates.

Example request:

```json
{
  "mode": "choice",
  "objective": "Select a delivery method",
  "context": {
    "priority": "fast"
  },
  "candidates": [
    {
      "id": "standard",
      "description": "Standard delivery"
    },
    {
      "id": "express",
      "description": "Express delivery"
    }
  ]
}
```

Conceptual response:

```json
{
  "mode": "choice",
  "selected_id": "express"
}
```

The selected identifier must refer to one of the candidates supplied in the request. If no valid candidate can be selected, the system should return an explicit error or abstention result rather than inventing a candidate.

## 5. Score — Ordinal Decisions

Score assigns an ordered rating to an item or candidate.

Example request:

```json
{
  "mode": "score",
  "objective": "Rate the suitability of this option",
  "context": {
    "reliability": "high",
    "cost": "medium"
  },
  "constraints": {
    "minimum_score": 1,
    "maximum_score": 5
  }
}
```

Conceptual response:

```json
{
  "mode": "score",
  "value": 4
}
```

The initial score contract uses an integer from 1 to 5 when those bounds are configured. Other valid ranges may be supported later.

An ordinal score expresses ordering. The difference between scores 1 and 2 is not necessarily equivalent in meaning to the difference between scores 4 and 5.

## 6. Box — Bounded Values

Box represents a numeric decision or prediction restricted to a defined range.

Example request:

```json
{
  "mode": "box",
  "objective": "Choose a target temperature",
  "context": {
    "current_temperature": 18
  },
  "constraints": {
    "minimum": 16,
    "maximum": 24
  }
}
```

Conceptual response:

```json
{
  "mode": "box",
  "value": 21.5
}
```

The value must be finite and within the configured bounds. The implementation must reject invalid bounds, including a minimum greater than the maximum.

## 7. Standard Response Fields

As the implementation matures, responses may include common fields such as:

- `request_id`: Identifier associated with the request, when supplied.
- `mode`: Decision mode used.
- `value` or `selected_id`: The result appropriate to the mode.
- `scores`: Optional candidate scores or rankings.
- `confidence`: Optional model confidence estimate.
- `model_version`: Optional identifier for the model version.
- `latency_ms`: Optional inference timing.

Only fields relevant to a particular result should be included.

Confidence must not be interpreted as a calibrated probability unless evaluation demonstrates that calibration is adequate. Latency and model-version fields should be added when reliable measurements or version identifiers are available.

## 8. Validation and Failure Behavior

ODM should validate requests before running inference.

Validation should cover:
- Unknown decision modes.
- Missing required fields.
- Malformed candidate lists.
- Duplicate or missing candidate identifiers where identifiers are required.
- Invalid numeric bounds.
- Non-finite numeric values.
- Invalid constraints.

Errors should be structured and explain what needs correction without exposing internal secrets or sensitive implementation details.

ODM should not silently replace invalid inputs with arbitrary defaults.

If the model cannot produce a valid decision, the interface should return a clear failure or abstention result.

## 9. Candidate Ranking

When ranking is supported, ODM may return a list of candidates with associated scores.

Scores are model outputs and are not necessarily probabilities. Their meaning and scale must be documented for the relevant model version.

The system must preserve candidate identifiers so the calling application can map the result back to its own actions.

The calling application remains responsible for checking permissions, enforcing safety constraints, and executing any selected action.

## 10. Interface Compatibility

All integrations must share the same core request validation and decision logic.

- The Python SDK should expose typed Python interfaces.
- The HTTP API should serialize requests and responses using JSON.
- The MCP adapter should expose decision functionality through MCP-compatible tools.

Transport-specific details may differ, but the meaning of a decision must remain consistent across interfaces.

## 11. Versioning

Contract changes must be evaluated for compatibility.

Changes that break existing request or response behavior should be documented and may require a new API or contract version.

Tests should verify valid requests, invalid requests, response structure, and consistency across integrations.

## 12. Implementation Status

These examples define the intended contract, not a claim that all modes or fields are implemented today.

The first implementation stage will introduce typed Python request and response models, validation, and automated tests before connecting the neural model.
