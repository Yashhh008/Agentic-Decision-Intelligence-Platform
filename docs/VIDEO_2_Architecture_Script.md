# VIDEO 2 — 5-Minute Architecture Walkthrough Script
## ADIP: Agentic Decision Intelligence Platform

---

> **Judging weight for this video: 70% of total score**
>
> This video must convince judges that ADIP is a real, architecturally
> sophisticated agentic platform — not a wrapper around a single LLM call.
> Show code. Show the diagram. Show the UI. Never just describe in words
> what you can show on screen.

---

## Pre-Recording Checklist

- [ ] Architecture diagram open: `docs/architecture.png` — fullscreen or side-by-side
- [ ] VS Code open at `c:\XLv_Hackathon\backend\` — explorer sidebar visible
- [ ] Browser open at `http://localhost:5174` — have a completed session ready with Planner Panel visible
- [ ] Zoom VS Code font to 16pt — code must be readable in the recording
- [ ] Close file diffs, terminals, and git panels — clean workspace only
- [ ] Screen recorder at 1080p minimum

---

## What Judges Are Scoring in This Video

| Architecture Criterion | What to Show |
|---|---|
| Multi-agent orchestration | Planner Panel — selected vs. skipped agents |
| Dynamic planning | Planner code + Planner Panel in UI |
| RAG implementation | `vectorstore/` + Retrieved Knowledge panel |
| Deterministic components | Confidence % badge + business rule badge in recommendation card |
| Memory / learning loop | Memory timeline in UI + `memory_service.py` |
| Code quality & structure | `backend/core/`, `backend/engine/`, `backend/agents/` |
| Extensibility | Architecture diagram + closing argument |

---

## Section-by-Section Script

---

### SECTION 1 — Design Philosophy (0:00 – 0:40)

**Show:** Architecture diagram fullscreen. Keep it visible throughout this section.

**Say:**

> "Before I walk through the architecture, I want to explain the core design philosophy — because every component in ADIP was built around one principle: separation of concerns.
>
> We never put business logic inside a single LLM prompt. We never let one agent call another directly. All communication in the system flows through a single shared state object called `ADIPState` — which is the single source of truth for the entire pipeline.
>
> This means every agent is independently testable, every execution step is reproducible, and you can add a new agent to the system without modifying any existing code. The architecture is modular by design, not by accident."

---

### SECTION 2 — Context Agent: Narrow, Typed, Reliable (0:40 – 1:10)

**Show:** Point to Context Agent box in diagram. Then switch to VS Code and open `backend/agents/context_agent.py`. Show the class definition and the output schema.

**Say:**

> "The pipeline starts with the Context Agent. And I want to emphasize how deliberately narrow it is.
>
> Its only job is signal extraction from raw text. It takes an unstructured customer transcript and outputs a strongly-typed signal object: `churn_risk`, `low_adoption`, `renewal_risk`, `expansion_interest`, `onboarding_friction`. Nothing else.
>
> It does not analyze. It does not recommend. It does not reason about business outcomes. It classifies.
>
> The LLM call inside this agent is schema-validated — if the response doesn't conform to our Pydantic model, the agent retries up to three times before failing gracefully with a structured error. This is production-grade reliability, not a demo shortcut."

---

### SECTION 3 — Dynamic Planner: The Architectural Centerpiece (1:10 – 2:05)

**Show:** Point to Planner in diagram. Then switch to the browser — open the Planner Panel from the completed Buildify session. Point to selected agents, skipped agents, and the planner reasoning text.

**Say:**

> "This is the component that makes ADIP an *agentic* system — not a sequential pipeline with hard-coded routing.
>
> After signal extraction, the Dynamic Planner receives the typed signals and the customer's organizational memory. It then makes an LLM call to generate an ExecutionPlan — a structured JSON object that specifies exactly which agents to run, in which order, and why.
>
> This is not `if churn_risk then run RiskAgent`. The Planner reasons. For a customer with low adoption and an expansion signal, it decides to run both the Risk Agent and the Opportunity Agent simultaneously — because both are relevant. For a healthy customer with only expansion signals, it skips the Risk Agent entirely. The execution graph adapts to the context of each individual customer.
>
> And — critically — look at this Planner Panel in the UI."

**Point to the Planner Panel on screen.**

> "Every judge can see exactly what the Planner decided: the detected signals, the selected agents, the skipped agents, and the full reasoning text. This transparency was a deliberate design choice. In an enterprise system, every AI decision must be auditable. You can never have a black box making business recommendations."

---

### SECTION 4 — Agent Framework: Registry, BaseAgent, State (2:05 – 2:40)

**Show:** VS Code. Open `backend/core/` — show `agent_registry.py` and `shared_state.py`. Briefly show `backend/agents/base_agent.py`.

**Say:**

> "All six specialized agents — Context, Retrieval, Risk, Opportunity, Renewal, Recommendation — inherit from a common BaseAgent. They're registered in the AgentRegistry at startup.
>
> Each agent follows the same contract: receive `ADIPState`, read from it, perform its specialized reasoning, write outputs back into state, return. Agents never talk to each other directly — ever. All inter-agent communication happens through the shared state object.
>
> The ExecutionEngine reads the Planner's output and runs the selected agents in the specified order, aggregating their insights into the shared state as it goes. This makes execution deterministic — the same inputs always produce the same agent selection and the same execution path. No randomness, no side effects."

---

### SECTION 5 — RAG Architecture: Grounded Intelligence (2:40 – 3:15)

**Show:** VS Code — open `backend/vectorstore/faiss_store.py`. Then switch to browser — show the Retrieved Knowledge panel with document chunks visible.

**Say:**

> "Recommendations in ADIP are not generated from the LLM's training data. They're grounded in retrieved enterprise knowledge.
>
> The Retrieval Agent searches a FAISS vector index — currently 163 chunks from 31 enterprise documents: customer CRM records, meeting transcripts, internal playbooks, support ticket history, email threads, product documentation, pricing guides, and internal policies.
>
> We embed documents using sentence-transformers all-MiniLM-L6-v2 — a fast, offline embedding model with no API dependency. Each chunk in the index carries metadata: document type, customer ID, source file, and creation date. This metadata enables filtering — when analyzing Buildify, we can retrieve Buildify-specific CRM notes alongside general playbooks.
>
> Look at the Retrieved Knowledge panel in the UI — these are the actual chunks that were retrieved for this analysis, with similarity scores. The Recommendation Agent receives all of these as structured evidence in its prompt. Every recommendation that comes out of the system can be traced back to a specific source document."

---

### SECTION 6 — Business Rules + Confidence Engine: Zero Hallucination (3:15 – 3:50)

**Show:** VS Code — open `backend/engine/` — show `business_rules.py` and `confidence_engine.py` briefly. Then switch to browser — zoom in on a recommendation card showing the confidence % and the Rule badge.

**Say:**

> "Two components run after the agents complete, and both are 100% deterministic. No LLM is involved in either of them.
>
> The Business Rules Engine evaluates threshold-based conditions against the customer data and detected signals. If the `LOW_ADOPTION` rule fires — active seats below 60% at Month 3 — it automatically attaches that rule to relevant recommendations. These rules are defined in code. They cannot be hallucinated. They are always auditable.
>
> The Confidence Engine scores each recommendation using a four-factor mathematical formula: signal strength, evidence quality from retrieval, customer health score, and rule alignment weight. The resulting percentage — 80%, 79%, 78% — is a deterministic calculation, not an LLM estimate.
>
> When a CSM sees 80% confidence on a recommendation, they can ask *why* — and the answer is a formula, not a feeling."

---

### SECTION 7 — Organizational Memory: The Learning Loop (3:50 – 4:25)

**Show:** Browser — Organizational Memory panel with existing Buildify records. Point to APPROVED and REJECTED records. Then switch to VS Code — open `backend/services/memory_service.py`.

**Say:**

> "Organizational memory is the architectural feature that separates a decision support tool from a decision intelligence platform.
>
> When a CSM approves or rejects a recommendation, that decision is persisted to SQLite with full context: the action taken, the human's decision, the outcome, the signals that were active at the time. On every subsequent analysis for the same customer, this history is retrieved and injected directly into the Planner's context — before it builds the execution plan.
>
> Look at Buildify's memory: a previous field training session was approved. An executive meeting was rejected. When the Planner processes a new Buildify transcript, it knows these things happened. It doesn't recommend the training again. It doesn't recommend the executive meeting again — the CSM said no.
>
> Instead it escalates. Instead it generates more precise interventions. The system improves with every human decision. That is the organizational learning loop — and it's live in this demo."

---

### SECTION 8 — Extensibility: The Platform Argument (4:25 – 5:00)

**Show:** Architecture diagram fullscreen again. Pan slowly across all layers.

**Say:**

> "Let me make the final architectural argument.
>
> Every layer of ADIP — the Dynamic Planner, the Agent Registry, the Execution Engine, the Business Rules Engine, the Confidence Engine, and the Memory Service — is completely domain-agnostic. None of these components know anything about Customer Success. They know about signals, execution plans, evidence, rules, scores, and decisions.
>
> Customer Success is Module 1 of this platform.
>
> To apply ADIP to a Sales team: register a QuotaRiskAgent and a PipelineAgent, load sales playbooks and pipeline data into the knowledge base, define sales-specific business rules. The Planner, the RAG layer, the Confidence Engine, the memory loop — unchanged.
>
> To apply ADIP to HR: register a RetentionRiskAgent and a PerformanceAgent. Same framework.
>
> The architecture was designed to be a platform from the beginning — not retrofitted. That is the thesis of ADIP: enterprise-grade, reusable, explainable, human-controlled Agentic Decision Intelligence."

---

## Closing Line

> "We didn't build a Customer Success chatbot. We built an architectural foundation for agentic decision intelligence across enterprise domains. Customer Success is how we demonstrate it today. Every other business domain is an agent registry update away."

---

## If Judges Ask Questions

| Question | Answer |
|---|---|
| "Why multiple agents instead of one big prompt?" | "Separation of concerns. Each agent is narrow, testable, and replaceable. One large prompt creates a brittle system that fails silently and is impossible to debug." |
| "Why FAISS instead of a cloud vector DB?" | "Offline, fast, zero latency, zero cost, no API dependency. For a hackathon demo it's also fully reproducible — the index ships with the repo." |
| "Why not let the LLM calculate the confidence score?" | "LLM confidence scores are uncalibrated and unverifiable. A 91% from an LLM means nothing. A 91% from our four-factor formula means: signal strength 0.9, evidence quality 0.85, health alignment 0.95, rule weight 1.0. You can audit it." |
| "How does memory handle conflicting decisions?" | "The Planner sees all prior decisions and reasons about conflicts in context. If a recommendation was rejected, the Planner treats it as a constraint. If the same action was approved and then rejected on a different occasion, it presents both data points and lets the confidence score reflect the ambiguity." |
| "Can this scale to hundreds of customers?" | "The architecture is stateless per request — each analysis creates its own ADIPState instance. Horizontal scaling is straightforward. The FAISS index can be replaced with a managed vector DB like Pinecone with no agent code changes." |
