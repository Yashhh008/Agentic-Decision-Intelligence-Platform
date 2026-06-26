# 06_API_Specification.md

# REST API Specification

Version 1.0

---

# 1. Purpose

This document defines the REST API contract for the Agentic Decision Intelligence Platform (ADIP).

The API exposes platform functionality to the frontend while keeping orchestration, AI reasoning, and persistence encapsulated within the backend.

The API follows RESTful principles where practical while remaining lightweight enough for the hackathon implementation.

---

# 2. API Design Principles

The API should be:

* Stateless
* Predictable
* Resource-oriented
* JSON-based
* Versionable
* Easy to extend

---

# 3. Base URL

```text
/api/v1
```

---

# 4. Core Resources

The platform exposes the following primary resources:

```text
Customers

Analysis Sessions

Planner

Knowledge

Recommendations

Approvals

Memory
```

---

# 5. Customer Endpoints

## Get Customers

```http
GET /customers
```

Returns all available mock customers.

Response

```json
[
  {
    "customer_id": "acme_corp",
    "company_name": "Acme Corp",
    "health_score": 32
  }
]
```

---

## Get Customer

```http
GET /customers/{customer_id}
```

Returns full customer profile.

---

## Customer History

```http
GET /customers/{customer_id}/history
```

Returns historical recommendations and outcomes.

---

# 6. Analysis Sessions

Analysis Sessions represent a single AI analysis workflow.

---

## Create Session

```http
POST /sessions
```

Body

```json
{
  "customer_id": "acme_corp",
  "interaction_type": "meeting_transcript",
  "interaction_text": "..."
}
```

Response

```json
{
  "session_id": "abc123",
  "status": "created"
}
```

---

## Get Session

```http
GET /sessions/{session_id}
```

Returns current session state.

---

## Execute Analysis

```http
POST /sessions/{session_id}/analyze
```

Triggers

* Context extraction
* Planner
* Retrieval
* Agents
* Recommendation generation

Response

```json
{
  "status": "completed"
}
```

---

# 7. Planner Endpoints

## Get Planner Decision

```http
GET /sessions/{session_id}/planner
```

Returns

* Detected signals
* Selected capabilities
* Selected agents
* Skipped agents
* Execution order
* Planner reasoning

Example

```json
{
  "signals": [
    "renewal_risk",
    "churn_risk"
  ],
  "execution_plan": {
    "parallel": true,
    "agents": [
      "retrieval",
      "risk",
      "renewal"
    ]
  }
}
```

---

# 8. Knowledge Endpoints

## Retrieved Knowledge

```http
GET /sessions/{session_id}/knowledge
```

Returns

Retrieved chunks

Similarity score

Source document

Evidence snippet

---

# 9. Recommendation Endpoints

## Get Recommendations

```http
GET /sessions/{session_id}/recommendations
```

Returns ranked recommendations.

Each recommendation contains

* action
* priority
* confidence
* reasoning
* evidence
* business_rule

---

## Recommendation Detail

```http
GET /recommendations/{recommendation_id}
```

Returns complete recommendation details.

---

# 10. Approval Endpoints

## Update Recommendation

```http
PATCH /recommendations/{recommendation_id}
```

Body

```json
{
  "decision": "approved"
}
```

Possible values

* approved
* rejected
* overridden

Override example

```json
{
  "decision": "overridden",
  "custom_action": "Schedule executive meeting."
}
```

---

# 11. Memory Endpoints

## Customer Memory

```http
GET /customers/{customer_id}/memory
```

Returns

Historical decisions

Planner history

Health progression

Previous recommendations

---

# 12. Analytics Endpoints

## Dashboard Metrics

```http
GET /analytics/dashboard
```

Returns

Average confidence

Approval rate

Average health score

Recommendation count

Executed agents

---

# 13. Error Format

Every error uses the same structure.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Customer not found."
  }
}
```

---

# 14. Response Format

Every successful response follows the same envelope.

```json
{
  "success": true,
  "data": {},
  "timestamp": "2026-06-29T12:00:00Z"
}
```

---

# 15. API Flow

Typical workflow

```text
GET /customers

↓

POST /sessions

↓

POST /sessions/{id}/analyze

↓

GET /sessions/{id}/planner

↓

GET /sessions/{id}/knowledge

↓

GET /sessions/{id}/recommendations

↓

PATCH /recommendations/{id}

↓

GET /customers/{id}/memory
```

---

# 16. Future Endpoints

Potential future APIs

* Authentication
* Agent registry
* Workflow templates
* Multiple business domains
* Streaming recommendations
* Batch analysis

---

# 17. Summary

The REST API provides a clean separation between the frontend and the AI orchestration backend.

It exposes customer management, analysis sessions, planner transparency, knowledge retrieval, recommendation workflows, approvals, memory, and analytics through consistent and extensible endpoints.
