# 07_Database_Design.md

# Database Design Specification

Version 1.0

---

# 1. Purpose

This document defines the persistence architecture for the Agentic Decision Intelligence Platform (ADIP).

The persistence layer stores:

* Customer profiles
* Analysis sessions
* Recommendations
* Human decisions
* Organizational memory
* Planner execution history
* Analytics metadata

The platform separates structured operational data from vector knowledge retrieval.

---

# 2. Storage Architecture

The platform uses three storage mechanisms.

```text
                 Storage Layer

        ┌────────────┬────────────┬────────────┐
        │            │            │
     SQLite        FAISS       File System
        │            │            │
 Operational     Embeddings    Documents
```

### SQLite

Stores structured business data.

### FAISS

Stores vector embeddings for semantic retrieval.

### File System

Stores source documents such as playbooks, FAQs, CRM exports, and product documentation.

---

# 3. Database Design Principles

* Normalize operational data.
* Keep vector data separate.
* Never store embeddings inside SQLite.
* Store references rather than duplicate content.
* Maintain complete audit history.

---

# 4. Entity Relationship Overview

```text
Customer
   │
   ├──────────────┐
   │              │
Sessions      Memory
   │              │
Recommendations   │
   │              │
Approvals─────────┘

Knowledge Documents

↓

Embeddings (FAISS)
```

---

# 5. Customers Table

Purpose

Stores customer master data.

Fields

* customer_id (PK)
* company_name
* industry
* contract_value
* renewal_date
* months_active
* health_score
* active_users
* licensed_users
* champion_status
* created_at

---

# 6. Sessions Table

Purpose

Represents a single AI analysis workflow.

Fields

* session_id (PK)
* customer_id (FK)
* interaction_type
* interaction_text
* planner_summary
* status
* created_at

One customer may have many sessions.

---

# 7. Recommendations Table

Purpose

Stores recommendations generated during a session.

Fields

* recommendation_id (PK)
* session_id (FK)
* action
* priority
* reasoning
* confidence
* evidence_source
* business_rule
* created_at

One session produces multiple recommendations.

---

# 8. Approvals Table

Purpose

Stores human decisions.

Fields

* approval_id (PK)
* recommendation_id (FK)
* decision
* override_text
* reviewer
* timestamp

Possible decisions

* approved
* rejected
* overridden

---

# 9. Memory Table

Purpose

Represents organizational learning.

Each record stores a previous decision that may influence future recommendations.

Fields

* memory_id (PK)
* customer_id (FK)
* recommendation
* decision
* outcome
* health_score_before
* health_score_after
* signals
* timestamp

The Planner retrieves recent memory before creating a new execution plan.

---

# 10. Planner Log Table

Purpose

Stores planner reasoning for transparency.

Fields

* planner_log_id
* session_id
* detected_signals
* selected_capabilities
* selected_agents
* skipped_agents
* planner_reasoning
* execution_mode
* execution_time

This powers the Planner Decision Panel.

---

# 11. Analytics Table

Stores lightweight operational metrics.

Examples

* recommendation_count
* average_confidence
* execution_time
* approval_rate

These values support the analytics dashboard.

---

# 12. Knowledge Documents

Enterprise knowledge is stored as files.

Examples

```text
knowledge/

playbooks/

faq/

product_docs/

pricing/

crm_notes/
```

SQLite stores only metadata.

Example

* document_name
* document_type
* path
* last_updated

---

# 13. Vector Store

FAISS contains

* embedding vector
* document_id
* chunk_id
* metadata

Metadata includes

* source document
* document type
* chunk number

SQLite never stores vectors.

---

# 14. Memory Retrieval Strategy

Before every analysis

Planner loads

* last 5 recommendations
* previous approvals
* previous overrides
* previous outcomes

Memory influences planning and recommendation generation.

---

# 15. Relationships

Customer

1 → N Sessions

Session

1 → N Recommendations

Recommendation

1 → 1 Approval

Customer

1 → N Memory Records

Knowledge Documents

1 → N Vector Chunks

---

# 16. Auditability

Every important action should be traceable.

Audit trail includes

* session creation
* planner decisions
* recommendation generation
* approval
* override
* memory update

No historical data is overwritten.

---

# 17. Future Scalability

The schema should support

* PostgreSQL migration
* Multi-tenant architecture
* User authentication
* Team collaboration
* Multiple business domains
* Workflow templates

without significant redesign.

---

# 18. Summary

The persistence layer separates operational data, organizational memory, and semantic knowledge retrieval into dedicated storage mechanisms.

SQLite manages structured business entities, FAISS enables semantic retrieval, and the file system stores enterprise documents. This separation keeps the architecture modular, scalable, and aligned with enterprise AI platform design.
