# 08_Mock_Enterprise.md

# Mock Enterprise Data Specification

Version 1.0

---

# 1. Purpose

This document defines the fictional enterprise environment used by the Agentic Decision Intelligence Platform (ADIP).

Rather than using isolated mock files, the project simulates a realistic B2B SaaS company with customers, internal documentation, CRM records, support tickets, meeting transcripts, emails, and organizational knowledge.

This creates a realistic Retrieval-Augmented Generation (RAG) environment for the hackathon.

---

# 2. Fictional Company

Company Name

**NimbusCRM**

Industry

Cloud-based CRM Software

Customers

Medium-sized B2B companies

Primary Users

* Customer Success Managers
* Account Managers
* Support Engineers
* Sales Teams

---

# 3. Enterprise Repository Structure

```text
enterprise/

├── customers/
│
├── crm/
│
├── meetings/
│
├── emails/
│
├── support/
│
├── product_docs/
│
├── playbooks/
│
├── pricing/
│
├── release_notes/
│
├── faq/
│
└── policies/
```

Each folder represents an enterprise knowledge source.

---

# 4. Customers

The platform contains four mock enterprise customers.

## Acme Corp

Scenario

* Low adoption
* Missed check-ins
* Churn risk

---

## TechFlow Inc

Scenario

* Heavy usage
* Rapid growth
* Upsell opportunity

---

## Buildify

Scenario

* Early onboarding
* Feature confusion
* Training required

---

## NovaSoft

Scenario

* Renewal approaching
* Champion resigned
* Executive engagement required

---

# 5. Customer Data

Each customer contains

Customer Profile

Usage Metrics

CRM Notes

Meeting History

Support Tickets

Email Threads

Decision History

These files simulate operational enterprise data.

---

# 6. CRM Records

Each CRM record contains

* Account owner
* Contract value
* Health score
* Renewal date
* Active users
* Product adoption
* Expansion opportunities
* Risk indicators

---

# 7. Meeting Transcripts

Meeting documents simulate Customer Success meetings.

Example scenarios

* Quarterly Business Review

* Onboarding Call

* Renewal Discussion

* Escalation Meeting

* Product Feedback Session

These become primary RAG inputs.

---

# 8. Email Threads

Example conversations

Customer requesting help.

Customer asking pricing questions.

Renewal reminders.

Upsell discussions.

Executive escalation.

Emails provide conversational business context.

---

# 9. Support Tickets

Support tickets include

Issue

Severity

Resolution

Status

Owner

Product Area

Resolution Time

These provide operational evidence for recommendations.

---

# 10. Product Documentation

Contains

Feature Guides

Administration Guide

Integration Guide

Implementation Guide

User Manual

These support onboarding recommendations.

---

# 11. Playbooks

Internal Customer Success playbooks.

Examples

Customer Onboarding

Churn Prevention

Expansion Strategy

Renewal Process

Executive Escalation

Each playbook includes

Objectives

Required Actions

Best Practices

Escalation Rules

Success Metrics

---

# 12. Pricing Guide

Contains

Subscription Plans

Feature Matrix

Upgrade Paths

Discount Policy

Enterprise Licensing

Used by Opportunity Agent.

---

# 13. Release Notes

Product releases.

Examples

Version 2.3

New onboarding wizard.

Version 2.4

AI Insights Dashboard.

These documents help explain feature recommendations.

---

# 14. Frequently Asked Questions

Internal FAQ

Examples

Authentication

Integrations

Permissions

Billing

Product Limits

Provides lightweight retrieval.

---

# 15. Internal Policies

Examples

Escalation Policy

Customer Communication Policy

Renewal Approval Process

Risk Classification

These influence Business Rules.

---

# 16. RAG Retrieval Strategy

The Retrieval Agent searches multiple sources.

Possible retrieval

```text
Meeting

↓

CRM

↓

Playbook

↓

Product Documentation

↓

Support Ticket

↓

FAQ
```

The platform never relies on one document type alone.

---

# 17. Mock Enterprise Scale

Approximate dataset

Customers

4

CRM Records

4

Meeting Transcripts

12

Support Tickets

16

Email Threads

20

Playbooks

5

Product Documents

8

Pricing Documents

2

Release Notes

6

FAQ Documents

10

Policies

4

Approximately

70–80 enterprise documents.

---

# 18. Document Metadata

Every document stores metadata.

Example

* document_id
* document_type
* customer_id (optional)
* version
* author
* created_date
* tags

Metadata improves retrieval quality.

---

# 19. Embedding Strategy

Every document is

Chunked

↓

Embedded

↓

Stored in FAISS

Metadata is preserved for filtering.

---

# 20. Example Retrieval

Input

Customer says

"Our onboarding has been confusing and adoption is low."

Retrieval

* Onboarding Playbook
* Customer CRM Notes
* Previous Meeting Transcript
* Product Onboarding Guide
* Support Ticket #204

The Recommendation Agent uses all retrieved evidence.

---

# 21. Future Expansion

The enterprise environment can later include

* Slack conversations
* Jira tickets
* Salesforce exports
* Zendesk history
* Product analytics
* Customer surveys

without changing platform architecture.

---

# 22. Summary

NimbusCRM provides a realistic enterprise environment that powers the Agentic Decision Intelligence Platform.

Rather than relying on isolated mock files, the platform simulates a complete organizational knowledge ecosystem, enabling multi-source Retrieval-Augmented Generation, explainable recommendations, and realistic decision intelligence workflows.
