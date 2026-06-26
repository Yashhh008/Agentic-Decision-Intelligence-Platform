# 01_System_Architecture.md

# ADIP – Agentic Decision Intelligence Platform

## System Architecture Specification

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the high-level architecture of the Agentic Decision Intelligence Platform (ADIP).

The architecture is designed around the following principles:

* Modular
* Reusable
* Extensible
* Explainable
* Enterprise-ready

Customer Success is the first implemented business module. The platform architecture is intentionally domain-agnostic so that additional domains (Sales, HR, Finance, Operations) can be supported by adding new agents and business rules without redesigning the system.

---

# 2. Architectural Goals

The architecture must satisfy the following objectives.

## Functional Goals

* Ingest enterprise interactions.
* Retrieve organizational knowledge.
* Dynamically orchestrate AI agents.
* Generate explainable recommendations.
* Support human approval.
* Learn from historical decisions.

## Non-Functional Goals

* Modular design
* Extensible architecture
* Maintainable codebase
* High observability
* Clear separation of responsibilities

---

# 3. High-Level Architecture

```
                    User
                     │
                     ▼
        React Enterprise Dashboard
                     │
                     ▼
      Customer Interaction Input Layer
      (Transcript / CRM / Email / Ticket)
                     │
                     ▼
       Ingestion & Preprocessing Service
                     │
                     ▼
          Context Extraction Agent
                     │
                     ▼
             Memory Retrieval Layer
                     │
                     ▼
====================================================

               Planner Agent

      Generates Dynamic Execution Plan

====================================================
                     │
                     ▼
             Execution Engine
                     │
      ┌────────┬────────┬────────┬─────────┐
      │        │        │        │         │
      ▼        ▼        ▼        ▼         ▼

 Retrieval   Risk   Opportunity Renewal Business
   Agent     Agent     Agent      Agent    Rules

      └────────┴────────┴────────┴─────────┘
                     │
                     ▼
             Result Aggregator
                     │
                     ▼
         Recommendation Engine
                     │
                     ▼
           Confidence Engine
                     │
                     ▼
         Human-in-the-Loop Review
                     │
                     ▼
            Persistent Memory Store
                     │
                     ▼
            Analytics & Dashboard
```

---

# 4. Architectural Layers

The platform is divided into logical layers.

## Layer 1 – Presentation Layer

Responsibilities

* Customer selection
* Interaction submission
* Recommendation display
* Human approval
* Memory timeline
* Analytics dashboard

Technology

* React
* Tailwind CSS

---

## Layer 2 – API Layer

Responsibilities

* REST endpoints
* Request validation
* Session management
* Authentication (future)

Technology

* FastAPI

---

## Layer 3 – Orchestration Layer

Responsibilities

* Planner
* Execution Engine
* Agent Registry
* State Management

Technology

* LangGraph

This is the heart of the platform.

---

## Layer 4 – Intelligence Layer

Contains specialized AI agents.

Each agent performs one responsibility only.

Examples

* Context Agent
* Retrieval Agent
* Risk Agent
* Opportunity Agent
* Renewal Agent
* Recommendation Agent

---

## Layer 5 – Knowledge Layer

Provides organizational knowledge.

Sources include

* Playbooks
* Product Documentation
* FAQs
* Customer History
* CRM Notes
* Previous Decisions

Technology

* FAISS
* Sentence Transformers

---

## Layer 6 – Persistence Layer

Stores

* Customer profiles
* Decision history
* Memory
* Metadata

Technology

* SQLite

---

# 5. Core Components

## 5.1 Context Extraction Agent

Purpose

Converts raw interaction text into structured business signals.

Input

* Meeting transcript
* CRM update
* Email
* Support ticket

Output

```
Detected Signals

Customer Intent

Priority

Entities
```

Example

```
Input

"Our onboarding has been confusing."

↓

Output

onboarding_friction
```

---

## 5.2 Planner Agent

The Planner is responsible for orchestration.

Responsibilities

* Read platform state.
* Inspect available agents.
* Build an execution plan.
* Decide which agents execute.
* Decide execution order.
* Skip unnecessary agents.

The Planner never performs business analysis.

Its responsibility is orchestration only.

---

## 5.3 Execution Engine

Executes the Planner's execution plan.

Supports

* Sequential execution
* Parallel execution
* Conditional execution

Future versions may support distributed execution.

---

## 5.4 Agent Registry

The registry maintains all available agents.

Responsibilities

* Register agents
* Discover agents
* Expose capabilities
* Enable extensibility

The Planner never imports agents directly.

It queries the registry.

---

## 5.5 Specialized Agents

Each specialized agent owns exactly one responsibility.

Example

Retrieval Agent

* Search enterprise knowledge

Risk Agent

* Assess churn risk

Opportunity Agent

* Identify expansion opportunities

Renewal Agent

* Analyze renewal readiness

Recommendation Agent

* Merge intelligence into actions

---

## 5.6 Business Rules Engine

Contains deterministic business rules.

Examples

```
Health Score < 30

↓

Executive Escalation
```

```
Renewal < 30 Days

↓

High Priority
```

Unlike LLMs, business rules are fully deterministic.

---

## 5.7 Result Aggregator

Combines outputs from multiple agents.

Responsibilities

* Merge results
* Remove duplicates
* Resolve conflicts
* Normalize outputs

The Recommendation Agent consumes the aggregated result instead of communicating directly with every agent.

---

## 5.8 Recommendation Engine

Produces the final Next Best Actions.

Each recommendation includes

* Action
* Priority
* Evidence
* Reasoning
* Confidence

---

## 5.9 Confidence Engine

Calculates confidence scores.

Confidence is not generated by the LLM.

Inputs include

* Retrieval similarity
* Business rule matches
* Historical consistency
* Signal strength

The final score is deterministic and explainable.

---

## 5.10 Memory Service

Stores organizational learning.

Each record includes

* Customer
* Signals
* Recommendation
* Human decision
* Outcome
* Timestamp

The Planner retrieves relevant memory before planning.

---

# 6. Data Flow

```
User Input

↓

Context Extraction

↓

Memory Retrieval

↓

Planner

↓

Execution Plan

↓

Execution Engine

↓

Specialized Agents

↓

Result Aggregator

↓

Recommendation Engine

↓

Confidence Engine

↓

Human Approval

↓

Memory Update

↓

Dashboard
```

---

# 7. Architectural Principles

## Single Responsibility

Each component performs one responsibility only.

---

## Loose Coupling

Components communicate through shared state and interfaces.

---

## High Cohesion

Related logic remains inside its own module.

---

## Explainability

Every recommendation must include evidence.

---

## Human Oversight

No recommendation is automatically executed.

---

## Extensibility

New agents should be added without changing existing architecture.

---

# 8. Extending the Platform

The architecture supports additional domains.

Example

```
Customer Success

↓

Sales

↓

Finance

↓

HR

↓

Operations
```

Only the following need to change

* Knowledge Base
* Business Rules
* Specialized Agents

The Planner, Execution Engine, Registry, Memory Service, and UI remain unchanged.

---

# 9. Technology Stack

Frontend

* React
* Tailwind CSS

Backend

* FastAPI
* Python

AI

* LangGraph
* Google Gemini
* Sentence Transformers

Knowledge

* FAISS

Database

* SQLite

Deployment

* Vercel
* Render

---

# 10. Architecture Decisions

| Decision                    | Reason                                           |
| --------------------------- | ------------------------------------------------ |
| Planner-based orchestration | Dynamic execution instead of hardcoded workflows |
| Agent Registry              | Easy extensibility                               |
| Execution Engine            | Separation of planning and execution             |
| Result Aggregator           | Simplifies downstream reasoning                  |
| Business Rules Engine       | Deterministic enterprise logic                   |
| Confidence Engine           | Explainable scoring                              |
| Memory Service              | Continuous improvement across interactions       |

---

# 11. Future Enhancements

* Multi-tenant deployment
* Authentication and RBAC
* Multiple LLM providers
* Additional business domains
* Plugin-based agent loading
* Distributed execution
* Agent health monitoring
* Observability dashboard
* Workflow analytics
* Feedback-driven learning

---

# 12. Summary

The Agentic Decision Intelligence Platform is designed as a reusable enterprise platform rather than a single-purpose application.

Its architecture emphasizes modularity, explainability, human oversight, and extensibility while remaining lightweight enough to implement within the hackathon timeline.
