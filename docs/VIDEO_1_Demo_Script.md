# VIDEO 1 — 5-Minute Product Demo Script
## ADIP: Agentic Decision Intelligence Platform
### Customer: Buildify | Scenario: Onboarding Friction + Expansion Opportunity

---

> **Judging weights: 70% Agentic AI Architecture · 30% Business Use Case**
>
> Every second of this script is engineered for those weights.
> Buildify is chosen because it demonstrates **dual-signal intelligence** —
> the platform catches both an onboarding problem AND a hidden CEO expansion
> opportunity from a single conversation. A human CSM would miss one of them.

---

## Pre-Recording Checklist

- [ ] Backend running: `uvicorn backend.main:app --reload --port 8000`
- [ ] Frontend running: `npm run dev`
- [ ] Browser open at `http://localhost:5174` — Dashboard tab visible
- [ ] Memory pre-seeded (Buildify already has 3 records — verify in sidebar)
- [ ] Zoom browser to **110%** — text must be readable in recording
- [ ] Close all other browser tabs, notifications, and Slack/email
- [ ] Screen recorder set to **1080p minimum** (OBS, Loom, or Screencastify)
- [ ] Interaction 1 transcript copied and ready to paste
- [ ] Interaction 2 CRM update copied and ready to paste

---

## Interaction Transcripts (Copy These Before Recording)

### Interaction 1 — Paste first

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

### Interaction 2 — Paste for the memory loop moment

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

## Scene-by-Scene Script

---

### SCENE 1 — The Problem (0:00 – 0:35)

**Show:** Dashboard overview. Keep the mouse still. Let the UI breathe. Do NOT click yet.

**Say:**

> "Every enterprise Customer Success team manages hundreds of accounts simultaneously. Each customer generates meeting notes, CRM updates, emails, support tickets — all unstructured text scattered across systems.
>
> The CSM has to read all of it, remember every prior decision, cross-reference internal playbooks, and then decide: *what is the next best action for this specific customer, right now?*
>
> That process is slow. It's inconsistent. It depends entirely on individual experience. And when someone leaves the team, that institutional knowledge walks out the door with them.
>
> ADIP — Agentic Decision Intelligence Platform — solves this. A network of specialized AI agents extracts signals, retrieves enterprise knowledge, and generates ranked, evidence-backed recommendations — with a human always making the final call."

**Why this opens strong:** Judges hear the problem before they see a single feature. By the time you click anything, they already care.

---

### SCENE 2 — The Portfolio (0:35 – 1:00)

**Show:** Dashboard. Slowly pan from KPI cards down to the customer table. Pause on Buildify's row.

**Say:**

> "The platform gives a Customer Success team real-time visibility across their entire portfolio — health scores, adoption rates, renewal timelines, contract value.
>
> Notice Buildify here — health score 55, adoption at 40%, Month 3 of onboarding. The platform has already flagged this account as needing attention. 12 of 30 licensed seats are active — that's well below the 60% benchmark for Month 3."

**Click Buildify's "Analyze" button.**

---

### SCENE 3 — The Decision Workspace (1:00 – 1:20)

**Show:** Decision Workspace loads. Point to the health ring, then slowly move to the agent pipeline row at the top — all nodes grey/idle.

**Say:**

> "We're inside the Decision Workspace for Buildify. On the left, the customer's health ring — a live health visualization. The stats bar shows the adoption rate, contract value, and renewal date at a glance.
>
> And at the top — the Agent Execution Pipeline. Six specialized agents: Context, Retrieval, Risk, Opportunity, Renewal, and Recommendation. Notice that none of them have run. That's intentional. A Dynamic Planner will decide which agents this specific customer situation actually needs — the system never runs every agent on every customer."

---

### SCENE 4 — Input & Trigger (1:20 – 1:50)

**Show:** Paste Interaction 1 into the transcript input box. Interaction type: `meeting_transcript`. Mouse hovers over "Run AI Analysis" button.

**Say:**

> "A Customer Success Manager pastes in the transcript from this morning's Month 3 check-in call with Tom Reeves, Buildify's Operations Manager. This is raw, unstructured voice-of-customer — no formatting, no preprocessing.
>
> Tom is describing a real problem: his field workers can't adopt a digital tool that's harder than a sticky note. He's also feeling CEO pressure to justify $36,000 a year at the next leadership meeting.
>
> I'm going to click Run AI Analysis — and I want you to watch exactly what happens."

**Click "Run AI Analysis".**

---

### SCENE 5 — The Live Pipeline (1:50 – 2:40) ← MOST IMPORTANT SCENE

**Show:** Agent pipeline nodes animate one by one. Point to each node as it lights up and narrate in real time.

**Say — narrate as each node glows:**

> "Watch the pipeline execute live — this is the architecture running in front of you.
>
> **Context Agent** — first to run. Its only job is structured signal extraction. It reads Tom's transcript and classifies it into typed business signals: `onboarding_friction` from the field team resistance, `low_adoption` from the seat count data, and — notice — it also detected an `expansion_interest` signal buried in the CEO's ROI question. A CSM skimming this transcript would focus on the complaint. The platform catches both signals simultaneously.
>
> **Organizational Memory** — next. The system queries what we already know about Buildify. It finds three prior decisions: a hands-on field training was approved and completed. Procore escalation was approved. An executive alignment meeting with the CEO was explicitly *rejected* by the CSM. All of this gets injected into the Planner's context before it makes a single decision.
>
> **Dynamic Planner** — this is where LangGraph orchestration comes in."

**PAUSE here as the Planner node glows. Let 2 seconds pass silently. Then:**

> "The Planner analyzed the signals and the memory. It built an execution plan. Watch which agents it selected."

**When Planner Panel appears on screen — point to it deliberately:**

> "Here — the Planner Panel. You can see *exactly* what it decided and why. It activated the Opportunity Agent — because of the CEO expansion signal. It activated the Risk Agent — because of the adoption gap. Retrieval ran to pull relevant knowledge. The Renewal Agent was skipped — renewal isn't until December. This isn't hard-coded routing. This is dynamic, context-aware orchestration."

---

### SCENE 6 — Retrieved Evidence (2:40 – 3:05)

**Show:** Retrieved Knowledge panel. Read the top retrieved chunk name aloud. Scroll through 2–3 chunks slowly.

**Say:**

> "While agents executed, the Retrieval Agent searched our FAISS vector index — 163 chunks from 31 enterprise documents: onboarding playbooks, CRM history, expansion strategy guides, product documentation, internal policies.
>
> Look at what was retrieved: the Customer Onboarding Playbook — specifically the section on field worker adoption. The Expansion Strategy guide. The Buildify CRM history showing the adoption trend. The Procore integration notes.
>
> Every recommendation the platform generates will be grounded in this evidence. Nothing is fabricated from model training. It's sourced."

---

### SCENE 7 — Recommendations & Human Approval (3:05 – 4:05)

**Show:** Three recommendation cards. Read the title of each. Then click "Show reasoning & evidence" on Recommendation 2.

**Say:**

> "Three ranked recommendations. Each card shows the action, the priority level — CRITICAL, HIGH, or MEDIUM — a confidence score calculated mathematically by our Confidence Engine, and the business rule that triggered it.
>
> **Recommendation 1, 80% confidence, CRITICAL priority — Rule: HIGH_CHURN_SIGNALS:** 'Escalate Procore integration status to the NimbusCRM Engineering Lead to expedite deployment.'
>
> This came from the Business Rules Engine — not the LLM. Our internal policy states: if an integration blocker is causing high churn signals, it escalates directly to engineering leadership. 
>
> **Recommendation 2, 78% confidence, HIGH priority — Rule: LOW_ADOPTION:** 'Pivot from video-based training to a hands-on, in-person or live-remote workshop for the 18 field workers.'
>
> Let me expand the evidence on this one."

**Click 'Show reasoning & evidence' on Recommendation 2.**

> "The reasoning is specific: 'The current onboarding video series has failed to drive adoption among field workers; evidence suggests a hands-on, non-technical training approach is required to overcome the 60% adoption gap.' The Retrieval Agent pulled this directly from the Buildify CRM history file. The Confidence Engine scored it at 78% based on the rule trigger and the evidence match. This is a justified, auditable decision."

**Recommendation 3:**

> "**Recommendation 3, 76% confidence — Rule: HIGH_CHURN_SIGNALS:** 'Schedule a formal Value Realization review with Tom Reeves to address dissatisfaction and align on a recovery plan.' — concrete, measurable, and grounded in the customer's exact pain points."

**Click Approve on Recommendations 1 and 2.**

> "The CSM approves these top two recommendations. Both decisions are now logged to organizational memory. Remember that — it matters in 30 seconds."

---

### SCENE 8 — The Memory Loop (4:05 – 4:45) ← THE WOW MOMENT

**Show:** Organizational Memory panel. Let it update visually. Then clear the interaction box and paste Interaction 2.

**Say:**

> "Two weeks have passed. The training happened — adoption jumped from 40% to 60%, the benchmark was hit. The CEO summary was delivered. But look at what arrived in a routine CRM update today: Linda Walsh, the CEO, is keynoting at the Western Construction Technology Summit next month and wants to feature this NimbusCRM rollout publicly. And Tom mentioned that Linda is planning three new regional offices in 2027 — potential expansion ARR of $108,000.
>
> I'm going to run the analysis again on the same customer. Watch what happens."

**Click Run AI Analysis.**

> "The Planner is querying memory first. It sees: hands-on field training was approved, and the Procore issue was escalated to the Engineering Lead. It will not recommend either of those exact actions again.
>
> Watch the execution plan change based on the memory and the new signals."

**When Run 2 recommendations appear:**

> "The platform remembered. It did not repeat the exact actions approved in the first run. Instead, it escalated and adapted based on the new context:
>
> 1. **83% Confidence, CRITICAL — Rule: expansion_interest:** 'Schedule a strategic expansion planning session with CEO Linda Walsh regarding the three new office locations.' The Opportunity Agent recognized the $108k signal and prioritized it above all else.
> 2. **81% Confidence, HIGH — Rule: LOW_ADOPTION:** 'Escalate the Procore integration delay to the VP of Engineering to ensure the end-of-June deadline is met.' The system escalated from the Engineering Lead (which was already approved) up to the VP level because the CEO is going public.
> 3. **78% Confidence, MEDIUM:** 'Coordinate with the Customer Success Enablement team to design a Train-the-Trainer program for Buildify's internal leads.' Instead of repeating the field workshop, it's now building a sustainable internal program.
>
> The system adapted. It escalated because the context changed, and it avoided repeating what was already done because memory persisted. That is organizational decision intelligence."

---

### SCENE 9 — Platform Close (4:45 – 5:00)

**Show:** Switch to Platform Insights tab. Let it display for 5 seconds.

**Say:**

> "ADIP is not a Customer Success tool. Customer Success is Module 1. The same Planner, the same Agent Registry, the same Confidence Engine and Memory Layer can be applied to Sales, Finance, HR, or any decision-heavy enterprise domain — by extending the knowledge base and registering new agents. The core architecture doesn't change.
>
> This is ADIP: a reusable, explainable, human-controlled Agentic Decision Intelligence Platform."

---

## Closing Line for Maximum Impact

> "Between these two analyses, the platform caught a hidden $108,000 expansion opportunity in a complaint call, remembered prior human decisions, refused to repeat completed actions, escalated a technical blocker to VP level because a CEO was going public, and pivoted to a scalable Train-the-Trainer program — all from unstructured text a CSM would read in 60 seconds and file away.
>
> That is the difference between a tool that processes text and a platform that exercises decision intelligence."

---

## Key Phrases to Use

| Avoid | Say Instead |
|---|---|
| "We call Gemini" | "The Context Agent makes a schema-validated LLM call with retry logic" |
| "The AI recommends" | "The Intelligence Fusion Engine consolidates multi-agent insights; the Confidence Engine scores deterministically" |
| "It remembers decisions" | "Organizational memory persists approved decisions and injects them into the Planner's context" |
| "You can approve or reject" | "The Human-in-the-Loop workflow requires explicit human authorization before any action is taken" |
| "We use LangGraph" | "LangGraph orchestrates the execution graph; the Planner generates the execution plan dynamically at runtime" |
