# 02_Backend_Architecture.md

# Backend Architecture Specification

Version 1.0

---

# 1. Objective

The backend provides the orchestration layer of the Agentic Decision Intelligence Platform (ADIP).

Its responsibilities are:

* Receive customer interactions
* Maintain platform state
* Orchestrate AI agents
* Retrieve enterprise knowledge
* Apply business rules
* Generate recommendations
* Persist organizational memory
* Expose REST APIs

The backend is intentionally modular and extensible.

---

# 2. Technology Stack

Language

* Python 3.11+

Framework

* FastAPI

AI Orchestration

* LangGraph

LLM

* Google Gemini (latest stable model)

Embeddings

* SentenceTransformers

Vector Database

* FAISS

Persistence

* SQLite

Validation

* Pydantic

Environment

* python-dotenv

---

# 3. Backend Folder Structure

```text
backend/

├── api/
│
├── agents/
│
├── core/
│
├── engine/
│
├── graph/
│
├── knowledge/
│
├── memory/
│
├── models/
│
├── prompts/
│
├── services/
│
├── utils/
│
├── vectorstore/
│
├── data/
│
├── config/
│
└── main.py
```

Every folder has a single responsibility.

---

# 4. Component Responsibilities

## api/

FastAPI routes.

Only request handling.

Never contains business logic.

---

## agents/

All AI agents.

Every agent inherits BaseAgent.

---

## engine/

Contains

* Planner
* Execution Engine
* Result Aggregator
* Confidence Engine
* Business Rules Engine

---

## graph/

Contains LangGraph implementation.

Responsible only for graph orchestration.

---

## services/

Contains reusable services.

Example

* Gemini Service
* Embedding Service
* Retrieval Service
* Memory Service

---

## knowledge/

Enterprise documents.

Playbooks

FAQs

Product docs

Policies

---

## vectorstore/

FAISS implementation.

---

## memory/

SQLite persistence.

---

## models/

Pydantic models.

Shared data objects.

---

## prompts/

Every LLM prompt.

No prompt should exist inside Python files.

---

## utils/

Logging

Parsing

Helpers

Formatting

---

# 5. Backend Layers

```text
REST API

↓

Controllers

↓

Orchestrator

↓

Execution Engine

↓

Agents

↓

Services

↓

Storage
```

Every layer communicates only with adjacent layers.

---

# 6. Request Lifecycle

```text
User Request

↓

FastAPI

↓

Validation

↓

State Initialization

↓

Memory Retrieval

↓

Planner

↓

Execution Plan

↓

Execution Engine

↓

Agent Execution

↓

Aggregation

↓

Recommendation

↓

Confidence

↓

Response
```

---

# 7. Shared State

The platform maintains a shared state.

Every component reads and writes to the same object.

Example fields

* customer

* interaction

* signals

* retrieved_context

* analyses

* recommendations

* confidence

* memory

The state acts as the communication medium between agents.

Agents never directly call each other.

---

# 8. Planner

Responsibilities

* Inspect state
* Inspect available agents
* Generate execution plan

The planner never performs business analysis.

Output

```text
Execution Plan

Agents

Execution Mode

Priority

Reason
```

Example

```text
Agents

Retrieval

Risk

Renewal

Parallel

True

Reason

Renewal within 30 days and health score below threshold.
```

---

# 9. Execution Plan

ExecutionPlan is a dedicated object.

Fields

```text
Goal

Selected Agents

Execution Order

Parallel Groups

Skipped Agents

Planner Reasoning
```

The Execution Engine executes this object.

---

# 10. Execution Engine

Responsibilities

* Read ExecutionPlan
* Execute selected agents
* Manage dependencies
* Handle failures
* Update shared state

The Execution Engine contains no AI logic.

It only coordinates execution.

---

# 11. Agent Registry

The registry manages all available agents.

Responsibilities

* Register agents
* Discover agents
* Lookup capabilities
* Instantiate agents

The planner queries the registry.

It never imports agents directly.

---

# 12. Result Aggregator

After execution

Every agent returns

```text
AnalysisResult
```

The Aggregator

* merges outputs
* removes duplicates
* resolves conflicts
* normalizes formats

Produces

UnifiedAnalysis

---

# 13. Business Rules Engine

Pure deterministic logic.

Examples

Health Score

<30

↓

Escalation Required

Support Tickets

> 5

↓

Urgent Review

Renewal

<30 days

↓

Priority High

No LLM is involved.

---

# 14. Recommendation Engine

Consumes

UnifiedAnalysis

Business Rules

Memory

Produces

Recommendations

Every recommendation contains

* Action

* Evidence

* Reasoning

* Priority

---

# 15. Confidence Engine

Confidence is calculated.

Never hallucinated.

Inputs

* Retrieval similarity

* Number of matching signals

* Business rule confidence

* Historical consistency

Output

```text
Confidence

88

Breakdown

Similarity

40

Rules

25

History

15

Signals

8
```

---

# 16. Memory Service

Responsibilities

Retrieve

Store

Update

Historical decisions.

Memory includes

* Recommendations

* Human decisions

* Outcomes

* Customer history

The planner loads memory before planning.

---

# 17. Retrieval Service

Responsibilities

Embed query.

Search FAISS.

Return ranked context.

Supports

* semantic search

* metadata filtering

* hybrid retrieval (future)

---

# 18. Error Handling

Every layer handles only its own errors.

Examples

API

↓

HTTP Exceptions

Planner

↓

Planning Errors

LLM

↓

Retry

Timeout

Fallback

Retrieval

↓

No Results

Memory

↓

Database Errors

---

# 19. Logging

Every major event should be logged.

Examples

Request received

Planner decision

Agents executed

Execution time

Memory updated

Human approval

Recommendation generated

---

# 20. Dependency Rules

Allowed

API

↓

Engine

↓

Agents

↓

Services

↓

Storage

Forbidden

Agent

↓

API

Planner

↓

Gemini

Agent

↓

Another Agent

This keeps coupling low.

---

# 21. Backend Design Principles

Single Responsibility

Loose Coupling

Shared State

Interface Driven

Reusable Components

Deterministic Business Rules

Observable Execution

---

# 22. Future Scalability

The backend should support

* Additional business domains

* New agents

* Multiple vector stores

* Different LLM providers

* PostgreSQL

* Redis

* Authentication

* Multi-tenancy

without major architectural changes.

---

# 23. Summary

The backend is designed around orchestration rather than sequential workflows.

The Planner generates execution plans.

The Execution Engine coordinates agents.

Specialized agents perform isolated responsibilities.

The Result Aggregator merges intelligence.

The Recommendation Engine produces explainable actions.

The Memory Service enables continuous learning.

This architecture emphasizes modularity, extensibility, and maintainability while remaining achievable within the hackathon timeline.
