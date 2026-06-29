# ADIP — Hackathon Demo & Presentation Guide

> **Judging weights: 70% Agentic AI Architecture · 30% Business Use Case**
>
> This guide is engineered for those weights. Every second of both videos is intentional.

---

## The Judge's Mindset

Judges are evaluating hundreds of submissions. They will remember you for **one thing**.

Make that one thing:

> *"This team built a real platform — not a chatbot with an API key."*

The way you earn that impression is by **showing architecture live**, not describing it in slides.

---

# VIDEO 1 — 5-Minute Product Demo

## Objective

Prove that ADIP solves a real enterprise problem with an AI system that is:
- Multi-agent (not one LLM call)
- Evidence-grounded (not hallucinating)
- Explainable (not a black box)
- Human-controlled (not autonomous)

## Pre-Recording Checklist

- [ ] Backend running: `uvicorn backend.main:app --reload --port 8000`
- [ ] Frontend running: `npm run dev`
- [ ] Browser open at `http://localhost:5174` — Dashboard tab visible
- [ ] Memory pre-seeded: `python -m backend.scripts.seed_demo_memory`
- [ ] Zoom browser to 110% — text must be readable in recording
- [ ] Close all other browser tabs and notifications
- [ ] Use a screen recorder at 1080p minimum (OBS, Loom, or Screencastify)

---

## Scene-by-Scene Script (5 min 00 sec)

---

### SCENE 1 — The Problem (0:00 – 0:35)

**Show:** Dashboard overview. Do not click anything yet.

**Say:**

> "Every enterprise Customer Success team manages hundreds of accounts simultaneously. Each customer generates emails, meeting notes, CRM updates, support tickets — all unstructured text. The CSM has to read all of it, recall prior decisions, cross-reference internal playbooks, and decide: what's the next best action for this account?
>
> That process is slow, inconsistent, and depends entirely on individual experience. When a team member leaves, that knowledge walks out the door.
>
> ADIP solves this with a multi-agent AI platform that transforms fragmented customer signals into ranked, evidence-backed recommendations — with humans always in control."

**Why this works:** You've told judges *why this exists* before showing a single feature. They now care.

---

### SCENE 2 — The Portfolio View (0:35 – 1:00)

**Show:** Dashboard. Point to the 4 KPI cards, then slowly scan the customer table.

**Say:**

> "The dashboard gives a Customer Success team real-time visibility across their entire portfolio. Health scores, adoption rates, renewal dates, ARR — all in one place. The system has already identified Acme Corp as Critical — health score 32, renewal in 18 days, only 8 of 25 licensed seats active."

**Click Acme Corp's "Analyze" button.**

---

### SCENE 3 — Customer Context (1:00 – 1:20)

**Show:** Decision Workspace — Customer Header with health ring, stats bar, agent pipeline (idle state).

**Say:**

> "The Decision Workspace loads the full customer context. Notice the agent pipeline at the top — six specialized agents are standing by. None of them have run yet. That's by design: the system doesn't execute every agent on every customer. A Dynamic Planner will decide which agents are relevant to *this* customer's situation."

---

### SCENE 4 — Input & Analysis Trigger (1:20 – 1:50)

**Show:** Interaction input panel with the pre-filled Acme Corp transcript.

**Say:**

> "A CSM pastes a meeting transcript into the workspace. This is direct voice-of-customer: Acme's operations manager is explicitly saying adoption is failing, support tickets are unresolved, and they're unsure about renewal."

**Click "Run AI Analysis". Start narrating while the pipeline animates.**

---

### SCENE 5 — Live Pipeline (1:50 – 2:30) ← MOST IMPORTANT SCENE

**Show:** Agent pipeline nodes lighting up one by one. Point to each as it activates.

**Say — narrate as each node glows:**

> "Watch the pipeline execute live.
>
> First — the **Context Agent** extracts structured business signals from the raw text. It's detecting churn risk, low adoption, renewal risk, and dissatisfaction — not keywords, semantic signals.
>
> Next — **Organizational Memory** is queried. The system already knows this customer had onboarding training two weeks ago, and a Business Value Review last week. This prevents the AI from recommending actions already taken.
>
> Now — the **Dynamic Planner**. This is where LangGraph orchestration comes in. The Planner analyzes the signals and *decides* which agents need to run. It's not executing all six agents — it's building a targeted execution plan."

**When Planner Panel appears — PAUSE. Point to it explicitly.**

> "Here — the Planner Panel shows you exactly what it decided: Risk Agent and Renewal Agent activated because of the churn and renewal signals. The Opportunity Agent was skipped because there's no upsell signal in this account. This transparency is a core design principle — you can always explain *why* the system did what it did."

---

### SCENE 6 — Retrieved Evidence (2:30 – 3:00)

**Show:** Retrieved Knowledge panel on the right.

**Say:**

> "While agents ran, the **Retrieval Agent** searched our FAISS vector index — 163 chunks from 31 enterprise documents: playbooks, CRM notes, email threads, support tickets, product documentation, internal policies.
>
> Every recommendation will be grounded in this evidence — not generated from the LLM's imagination."

**Point to the highest-match chunk.**

> "Here's the Churn Prevention Playbook retrieved at 87% similarity. The recommendation engine will use this as primary evidence."

---

### SCENE 7 — Recommendations & HITL (3:00 – 4:00)

**Show:** Recommendation cards. Read the top one. Expand evidence.

**Say:**

> "The platform has generated three ranked recommendations. Each one shows: the action, priority level, a confidence score — calculated mathematically, not by the LLM — and the business rule that was triggered.
>
> This recommendation to escalate to executive engagement — confidence 91% — was triggered by our internal policy: 'Renewal within 30 days, health score below 40, two unresolved critical tickets — executive outreach required.'
>
> Let me expand the evidence."

**Click "Show reasoning & evidence".**

> "The recommendation cites the Churn Prevention Playbook, the Acme Corp email thread where the customer explicitly mentioned competitors, and the escalation policy. This is not a guess — it's a justified decision."

**Click Approve on the top recommendation.**

> "The CSM approves. This decision is now logged to organizational memory."

---

### SCENE 8 — Memory Loop (4:00 – 4:40) ← THE WOW MOMENT

**Show:** Organizational Memory panel updating in real-time.

**Say:**

> "Watch the memory timeline. The approval just created a new record. Now — here's what makes this a *platform* and not just a tool."

**Clear the transcript. Type a shorter, second version:**
> *"Follow-up call with Acme Corp. Team says they appreciated the executive outreach but onboarding training hasn't resolved the adoption problem. Still at risk."*

**Click Run AI Analysis again.**

> "I'm running analysis a second time on the same customer. The system retrieves the memory — it knows we already did onboarding training, already did the BVR, already initiated executive contact. Watch what it recommends now."

**When recommendations appear:**

> "The platform adapted. It's no longer recommending what we already did. It's escalating: bring in the Churn Prevention Specialist, trigger the 48-hour SLA policy, propose a retention offer. The system *learned* from the human decision. That's organizational memory in action."

---

### SCENE 9 — Closing (4:40 – 5:00)

**Show:** Switch to Platform Insights tab.

**Say:**

> "ADIP is more than a recommendation tool. It's a reusable enterprise platform. The same agent framework, planner, and memory layer can be applied to Sales, HR, Finance, or any decision-heavy domain — by adding new agents and knowledge sources without changing the core architecture.
>
> This is ADIP: Agentic Decision Intelligence Platform."

---

# VIDEO 2 — 5-Minute Architecture Walkthrough

## Objective

Convince judges — who are weighting architecture at **70%** — that you understand:
1. Why multi-agent over a single LLM
2. How the planner works
3. What makes RAG grounded
4. Why confidence is deterministic
5. What the memory loop achieves architecturally

**Show the architecture diagram throughout this video. Keep it on screen.**

---

## Architecture Script (5 min)

---

### SECTION 1 — Design Philosophy (0:00 – 0:40)

**Show:** Architecture diagram (`docs/architecture.png`). Keep it visible.

**Say:**

> "The core design principle of ADIP is separation of concerns across agents. We never put business logic in a single LLM prompt. We never let one agent call another directly. All communication flows through a shared state object — ADIPState — which is the single source of truth throughout the pipeline.
>
> This makes the system modular, testable, and extensible. You can add a new agent to the registry without touching any existing code."

---

### SECTION 2 — Context Agent + Signal Extraction (0:40 – 1:10)

**Show:** Point to Context Agent in diagram. Open `backend/agents/context_agent.py`.

**Say:**

> "The pipeline starts with the Context Agent. Its only job is structured signal extraction from raw text. It outputs typed signals — churn_risk, low_adoption, renewal_risk — using a schema-validated LLM call. If the LLM returns malformed output, we retry up to three times before failing gracefully.
>
> We deliberately keep this agent narrow. It doesn't analyze, recommend, or reason about business outcomes — it only classifies."

---

### SECTION 3 — Dynamic Planner (1:10 – 2:00) ← MOST IMPORTANT FOR JUDGES

**Show:** Point to Planner in diagram. Show Planner Panel in the UI.

**Say:**

> "The Dynamic Planner is the architectural centerpiece. After signal extraction, it uses an LLM call to build an ExecutionPlan — a structured JSON object that specifies exactly which agents to run, in what order, and why.
>
> This is not hard-coded routing. The Planner reasons about the detected signals and selects capabilities dynamically. For a customer with churn risk and renewal pressure, it activates the Risk Agent and Renewal Agent. For a healthy customer with expansion signals, it activates the Opportunity Agent instead.
>
> This is what makes ADIP an *agentic* system, not a pipeline. The execution graph adapts to context."

**Show the Planner Panel in the running UI:**

> "In the Planner Decision Panel, you can see exactly what the Planner decided — detected signals, activated agents, skipped agents, and its full reasoning. This transparency was a deliberate architectural choice. Every decision in the system must be auditable."

---

### SECTION 4 — Agent Framework (2:00 – 2:35)

**Show:** `backend/core/` directory structure.

**Say:**

> "All agents inherit from BaseAgent and are registered in the AgentRegistry. Each agent receives the shared ADIPState, reads from it, writes its output back to it, and returns. Agents never communicate with each other — only through state.
>
> The ExecutionEngine reads the Planner's output and runs selected agents in order, aggregating their insights into the shared state. This keeps execution deterministic and reproducible."

---

### SECTION 5 — RAG Architecture (2:35 – 3:10)

**Show:** `backend/vectorstore/` and the Retrieved Knowledge panel.

**Say:**

> "The Retrieval Agent uses FAISS for similarity search across 163 chunks from 31 enterprise documents — playbooks, CRM notes, email threads, support tickets, release notes, and internal policies. Each chunk carries metadata: document type, customer ID, source file, creation date.
>
> We use sentence-transformers all-MiniLM-L6-v2 for embeddings — fast, offline, no API dependency. The retrieval result is injected into the RecommendationAgent's prompt as structured evidence, so recommendations are grounded in real organizational knowledge, not model weights."

---

### SECTION 6 — Business Rules + Confidence Engine (3:10 – 3:45)

**Show:** `backend/engine/` directory. Show a recommendation card's confidence % and business rule badge.

**Say:**

> "Two components run after agents complete, and both are 100% deterministic — no LLM involved.
>
> The Business Rules Engine evaluates threshold conditions against the customer's data and the detected signals. If health score is below 40 and renewal is within 30 days — a critical escalation rule fires. These rules cannot be hallucinated.
>
> The Confidence Engine scores each recommendation using a four-factor formula: signal strength, evidence quality, customer health, and rule alignment. The score is mathematical. A CSM can always verify why a recommendation has 91% confidence — it's not an LLM's gut feeling."

---

### SECTION 7 — Memory Layer (3:45 – 4:20) ← SHOWS ARCHITECTURAL SOPHISTICATION

**Show:** Memory timeline in the UI. Point to `backend/services/memory_service.py`.

**Say:**

> "Organizational memory is the feature that separates a decision tool from a decision intelligence platform.
>
> When a CSM approves or rejects a recommendation, that decision is persisted to SQLite with full context: the action, the decision, the outcome, the detected signals. On every subsequent analysis for the same customer, this history is retrieved and injected into the Planner's context.
>
> The Planner can then avoid repeating actions already taken, escalate when prior interventions failed, and adapt its execution plan based on institutional knowledge. This is the learning loop — it improves with every human decision."

---

### SECTION 8 — Extensibility & Reusability (4:20 – 5:00)

**Show:** Full architecture diagram again.

**Say:**

> "Every design decision in ADIP optimized for reusability. The Planner, Agent Registry, Execution Engine, Business Rules Engine, Confidence Engine, and Memory Layer are domain-agnostic. They don't know anything about Customer Success.
>
> To apply this platform to Sales: add a QuotaRiskAgent and PipelineAgent, load sales playbooks into the knowledge base, define new business rules. The rest of the architecture is unchanged.
>
> To apply it to HR: add a RetentionRiskAgent and PerformanceAgent. Same framework.
>
> That's the architectural thesis: ADIP is not a Customer Success tool. It's an enterprise-grade Agentic Decision Intelligence Platform that happens to be running Customer Success as its first domain."

---

# GitHub Repository Guide

## What Judges Look For in the Repo

1. **README is the landing page** — it must hook them in 30 seconds
2. **Clean structure** — they shouldn't have to hunt for files
3. **Working setup** — if they can't run it, it hurts your score
4. **Architecture evidence** — they want to see the sophistication is real

## Pre-Submission Repository Checklist

- [ ] README displays architecture diagram correctly on GitHub
- [ ] All API keys removed from committed files (check `.env` is in `.gitignore`)
- [ ] `docs/` folder contains `architecture.png` and all 12 documentation files
- [ ] `backend/requirements.txt` is accurate and complete
- [ ] `backend/knowledge/enterprise/` contains all 31 documents
- [ ] `backend/vectorstore/index/` — commit the pre-built FAISS index (saves setup time for judges)
- [ ] `render.yaml` and `frontend/vercel.json` deployment configs present
- [ ] README quick-start works with exactly those commands

## Optional: Add These to GitHub README Top

Add GitHub topic tags to your repo:
```
langgraph  multi-agent  rag  fastapi  react  enterprise-ai  decision-intelligence
```

---

# Judging Criteria Response Map

## 70% — Agentic AI Platform Architecture

| What They Assess | Where You Show It |
|---|---|
| Multi-agent orchestration | Planner Panel — selected vs. skipped agents |
| Dynamic planning | Architecture walkthrough Section 3 |
| RAG implementation | Retrieved Knowledge panel + Section 5 |
| Deterministic components | Confidence % badge + business rule badge |
| Memory / learning loop | Demo Scene 8 — second run changes recommendations |
| Code quality | `backend/core/`, `backend/engine/`, `backend/agents/` |
| Extensibility | Architecture walkthrough Section 8 |

## 30% — Business Understanding & Use Case

| What They Assess | Where You Show It |
|---|---|
| Real problem statement | Demo Scene 1 (opening 35 seconds) |
| Enterprise relevance | 4 customer personas, real signals, real scenarios |
| Human-in-the-loop rationale | "Business decisions have financial consequences" |
| Evidence-based decisions | RAG evidence sourcing in recommendation cards |
| Platform reusability claim | "Customer Success is module 1 of N" |

---

# Phrases That Win

Use these during the demo and architecture walkthrough:

| Instead of... | Say... |
|---|---|
| "We use LangGraph" | "LangGraph orchestrates the execution graph; the Planner generates the plan dynamically at runtime" |
| "We call Gemini" | "The Context Agent makes a schema-validated LLM call with retry logic and graceful fallback" |
| "The AI recommends actions" | "The Intelligence Fusion Engine consolidates multi-agent insights; the Confidence Engine scores them deterministically" |
| "It remembers past decisions" | "Organizational memory persists approved decisions and injects them into the Planner's context on future analyses" |
| "You can approve or reject" | "The Human-in-the-Loop workflow ensures every AI recommendation requires explicit human authorization before any action is taken" |

---

# The Single Most Impressive Moment

Run the analysis once. Approve a recommendation. Run it again with a follow-up transcript.

When the recommendations change because memory influenced the Planner — **pause**. Let the judges absorb it.

Then say:

> "The platform just demonstrated adaptive organizational decision intelligence. It didn't repeat what was already tried. It escalated because the prior intervention was insufficient. This is what separates ADIP from a recommendation chatbot — it learns from the humans who use it."

That sentence, delivered confidently at the right moment, wins the demo round.

---

---

# ALTERNATE DEMO — Buildify Customer (Onboarding Friction + Expansion Opportunity)

> Use this version if you want to demo a **different customer arc** — showing
> onboarding friction and feature confusion rather than churn. Buildify is a
> construction company in Month 3 of onboarding: office staff fully adopted,
> but 18 field workers completely bypassing the platform. Champion Tom Reeves
> is engaged and motivated, but under CEO pressure to show ROI.
> This scenario resonates with any B2B SaaS evaluator.

---

## Why Buildify Is a Strong Demo Choice

| Signal | Why It Matters to Judges |
|---|---|
| `onboarding_friction` | Shows signal variety — Planner activates different agents than churn scenario |
| `low_adoption` | Adoption intelligence is a different problem from retention |
| `feature_confusion` | Platform understands nuanced, non-obvious customer problems |
| Dual signals in one conversation | Complaint contains hidden expansion opportunity — AI catches it; human might miss it |
| Clean memory loop | Run 2 visibly avoids repeating training/CEO summary already approved in Run 1 |

---

## Pre-Demo Setup for Buildify

1. Select **Buildify** from the sidebar
2. Clear any previous session text
3. Have **Interaction 1** text ready to paste (copy from below)
4. After approving recommendations, have **Interaction 2** ready for the memory loop

---

## INTERACTION 1 — Month 3 Check-in Call

### Paste into "Customer Interaction Input" (Type: `meeting_transcript`)

```
Month 3 onboarding check-in with Tom Reeves, Operations Manager at Buildify.

Tom: "Aisha, the office team is fully using the platform — our project managers 
love it, pipeline reporting is great. But my field crew, the guys actually 
on-site doing the work — they haven't touched it. They're still logging jobs 
on paper and sending me photos of handwritten notes at end of day.

The problem is they're on phones all day, not laptops, and they find the app 
confusing. My foreman said it takes him 10 minutes to log a job update — he 
used to do it in 30 seconds on a sticky note. If it's harder than paper, 
they won't use it. Simple as that.

We're also still waiting on the Procore integration. My field team lives in 
Procore for project tracking. Until NimbusCRM talks to Procore, I'm asking 
them to switch between two systems — that's never going to work.

I believe in this platform — the office side proves the value. But Linda, 
our CEO, asked me last week in an all-hands what we're getting for $36k a year. 
I didn't have a strong answer. I need to show her something real before my 
next leadership meeting."
```

---

### What to say while analysis runs — narrate the pipeline:

> "Buildify is in Month 3 of onboarding — 12 of 30 licensed seats active, 40% adoption against a 60% benchmark. Tom Reeves is an engaged champion, but 18 field workers have completely bypassed the platform because the workflow doesn't fit how they work.
>
> Watch the Context Agent classify this conversation. It's not pattern-matching keywords — it's understanding that the field team friction is an `onboarding_friction` signal, the workflow complexity is `feature_confusion`, and the CEO ROI question buried at the end is actually an `expansion_interest` signal. A CSM reading this quickly would focus on the complaint and miss the CEO angle entirely.
>
> Now the Planner: it's detected two signal types — an adoption problem AND an executive opportunity. Watch which agents it selects."

**When Planner Panel appears — point to it:**

> "The Planner activated the Risk Agent for adoption risk and — notice — the Opportunity Agent for the CEO expansion signal. It also activated the Retrieval Agent to search our knowledge base for relevant onboarding playbooks, mobile app guides, and expansion strategy documents. The Renewal Agent was skipped — renewal is December, not urgent."

---

### Expected recommendations — what to say about each:

**Recommendation 1 — HIGH priority (80% confidence)**
> Initiate a formal expansion discovery call with CEO Linda Walsh regarding the three new office locations.

**Say:**
> "The Opportunity Agent identified the CEO expansion potential. The Confidence Engine scored this at 80% because it aligned with our expansion strategy playbook and the direct CEO interest signal. The platform caught this strategic opportunity early during onboarding."

**Recommendation 2 — MEDIUM priority (79% confidence) | Rule: LOW_ADOPTION**
> Develop and deliver a simplified, non-technical 'Quick Start' guide specifically for field workers to supplement the existing video series.

**Say:**
> "This was triggered by the Business Rules Engine under the `LOW_ADOPTION` rule. Because our active seat count is below the 60% threshold, the system automatically generated this targeted remediation to resolve onboarding friction."

**Recommendation 3 — MEDIUM priority (78% confidence) | Rule: LOW_ADOPTION**
> Conduct a value-realization review with Tom Reeves to map the Procore integration progress to specific field workforce KPIs.

**Say:**
> "Also triggered by the `LOW_ADOPTION` rule. Instead of a generic status meeting, it specifies mapping the integration progress to concrete field workforce KPIs, ensuring the business value is clear before the CEO's next leadership review."

**Approve Recommendations 1 and 2.** Say: *"The CSM approves. Both decisions are now logged to organizational memory."*

---

## INTERACTION 2 — CRM Update (2 Weeks Later)

> This is the memory loop moment. Run this immediately after approving Run 1 recommendations.
> The platform will visibly change its behaviour because it remembers what was already done.

### Paste into "Customer Interaction Input" (Type: `crm_update`)

```
CRM Update — Buildify — June 19, 2026

On-site training completed this morning at Buildify Sacramento yard. Tom Reeves 
hosted 14 field workers. NimbusCRM trainer demonstrated mobile app offline mode 
and the simplified job logging workflow — reduced from 10 minutes to under 2 minutes.

Post-session: 9 of 14 field workers committed to trying the platform this week. 
5 senior foremen still resistant — prefer paper-based tracking, skeptical of 
any digital tool.

Seat count updated: 18 of 30 active (up from 12). Adoption now at 60% — 
hit the Month 3 benchmark.

Procore integration: still blocked. Buildify IT access provisioning unresolved.

New development: Linda Walsh (CEO) mentioned to Tom that she is keynoting at 
the Western Construction Technology Summit next month and wants to feature 
Buildify's NimbusCRM rollout as a digital transformation success story. She 
asked Tom if NimbusCRM could provide materials or a case study.

Tom also mentioned Linda is planning to open 3 new regional offices in 2027 — 
each would need its own NimbusCRM license. Potential expansion ARR: $108k.
```

---

### What to say before clicking Run AI Analysis:

> "Two weeks have passed. The on-site training happened — adoption jumped from 40% to 60%, hitting the benchmark. CEO summary was delivered. But a completely new, high-value signal has appeared in a routine CRM update: the CEO is about to speak at a public industry conference and wants to showcase this rollout. And there's a $108k expansion opportunity sitting inside three lines of a status update.
>
> Let me run the analysis again and show you what the platform does differently."

---

### After clicking — narrate:

> "The Planner is querying memory before deciding which agents to run. It sees: on-site training was approved and completed. CEO executive summary was approved. It will NOT recommend those again.
>
> Watch the execution plan shift. The Planner is now treating this as a high-priority expansion scenario — the Opportunity Agent becomes the lead agent. The Risk Agent is secondary — 5 foremen still resistant. The Renewal Agent is still skipped — December is far out. Completely different plan from Run 1, for the same customer."

---

### Expected new recommendations — very different from Run 1:

**Recommendation 1 — CRITICAL priority (~93% confidence)**
> Immediately escalate Procore integration to VP of Engineering. CEO Linda Walsh is presenting the NimbusCRM rollout at a public conference in under 30 days. An unresolved integration failure during a public endorsement is a reputational risk for NimbusCRM.

**Say:**
> "The Business Rules Engine fired a new rule that didn't exist in Run 1: 'CEO public commitment + unresolved critical integration = VP-level escalation.' The context changed, the rule fired. This is not the LLM being creative — this is a deterministic threshold being crossed."

**Recommendation 2 — HIGH priority (~89% confidence)**
> Engage CEO Linda Walsh directly with a co-marketing proposal: offer an official NimbusCRM case study, conference speaking support, and reference customer program membership in exchange for a formal reference agreement.

**Say:**
> "The Opportunity Agent identified this as an expansion_interest signal of the highest order. The expansion ARR — $108k from three new offices — combined with the CEO's public visibility at an industry summit creates a strategic account moment. A reactive CSM sends a congratulations email. An intelligent platform converts this into a reference customer agreement."

**Recommendation 3 — MEDIUM priority (~71% confidence)**
> Design a targeted 1-on-1 micro-training for the 5 resistant senior foremen — focus exclusively on the 2-minute mobile logging workflow, delivered individually rather than in a group.

**Say:**
> "The platform remembered 5 foremen are still resistant. Instead of recommending a general training session — which already happened — it generated a targeted intervention for the specific cohort still not adopted. Same problem, more precise action."

---

## The Closing Line for This Scenario

After showing Run 2:

> "Between these two analyses, the platform remembered two human decisions, refused to repeat what was already done, detected a $108k expansion opportunity buried inside a routine CRM status update, escalated a technical blocker to VP level because a CEO was about to speak publicly, and generated a co-marketing strategy — all from a 200-word update that a CSM would read in 60 seconds and file away.
>
> That is the difference between a tool that processes text and a platform that exercises decision intelligence."

---

## Judging Score Map for This Scenario

| Architecture Criterion (70%) | Evidence in This Demo |
|---|---|
| Dynamic Planner adapts between runs | Opportunity Agent becomes lead in Run 2; Risk Agent secondary |
| Memory prevents repetition | Training and CEO summary not recommended again |
| Multi-signal detection from one input | `onboarding_friction` AND `expansion_interest` in same transcript |
| Deterministic Business Rules | VP escalation triggered by CEO conference rule |
| RAG evidence grounding | Onboarding Playbook + Expansion Strategy doc both cited |
| Agent specialization | Opportunity Agent does different work than Risk Agent |

| Business Criterion (30%) | Evidence in This Demo |
|---|---|
| Real enterprise problem | Field worker resistance to digital tools is universal in construction |
| Revenue impact surfaced | $36k → $108k expansion identified from a status CRM update |
| Decision quality vs. individual CSM | Platform caught dual signal (complaint + opportunity) simultaneously |
| Human-in-the-loop rationale | Co-marketing has legal/partnership implications — must be human-approved |
| Platform reusability | Completely different industry and signal set from the Acme Corp scenario |
