# MASTER_PROMPT.md

# ADIP – Agentic Decision Intelligence Platform

## Master Development Prompt

---

# Overview

You are acting as a **Senior Staff AI Engineer and Enterprise Solutions Architect**.

Your task is to implement an enterprise-grade **Agentic Decision Intelligence Platform (ADIP)** for a hackathon.

This project is **NOT** a simple AI chatbot.

It is a reusable enterprise platform that uses multiple AI agents, Retrieval-Augmented Generation (RAG), planning, orchestration, memory, explainability, and human-in-the-loop decision making.

The implementation must strictly follow the architecture provided in the `docs/` folder.

The documentation is the **single source of truth**.

If implementation conflicts with documentation, **always follow the documentation**.

---

# Before Writing Any Code

Read and fully understand every document inside the `docs/` directory.

Read them in order:

1. 00_Project_Overview.md
2. 01_System_Architecture.md
3. 02_Backend_Architecture.md
4. 03_Agent_Framework.md
5. 04_AI_Design.md
6. 05_Frontend_Architecture.md
7. 06_API_Specification.md
8. 07_Database_Design.md
9. 08_Mock_Enterprise.md
10. 09_Implementation_Roadmap.md
11. 10_Demo_Guide.md

Do not skip any document.

---

# Phase 1 — Architecture Validation (MANDATORY)

Before generating code, provide an Architecture Validation Report.

The report must contain:

## 1. Architecture Summary

Explain in your own words:

* System Architecture
* Backend Architecture
* AI Architecture
* Frontend Architecture
* Database Architecture

---

## 2. Folder Structure

Show the complete folder structure that will be generated.

---

## 3. Technology Stack

List every technology and explain why it is being used.

---

## 4. Potential Issues

Identify:

* Missing requirements
* Architecture inconsistencies
* Dependency conflicts
* Possible implementation risks

If you find issues, explain them before writing code.

---

## 5. Development Plan

Break implementation into logical phases.

Explain:

* what will be built first
* why
* dependencies between components

Wait for my confirmation before starting implementation.

---

# General Development Rules

Always behave like a senior software engineer working on a production codebase.

Do NOT generate the entire project in one response.

Implement the project in small logical phases.

At the end of every phase:

* Verify imports.
* Verify dependencies.
* Ensure the project builds.
* Summarize completed work.
* Stop and wait for my approval.

Never continue automatically.

---

# Coding Principles

Follow:

* SOLID Principles
* Clean Architecture
* Separation of Concerns
* Reusable Components
* Modular Design
* Type Safety
* Consistent Naming

Avoid unnecessary complexity.

Write readable code.

Do not duplicate logic.

---

# Backend Requirements

Use:

* Python 3.11+
* FastAPI
* Pydantic
* SQLAlchemy
* LangGraph
* Google Gemini API
* SentenceTransformers
* FAISS
* SQLite

The backend must be modular.

Business logic must never exist inside API routes.

---

# Frontend Requirements

Use:

* React
* Vite
* TypeScript
* Tailwind CSS
* React Query
* Axios

Design the frontend like an enterprise SaaS platform.

Do NOT build a chatbot interface.

The primary interface is an enterprise dashboard.

---

# AI Requirements

Implement a multi-agent architecture.

Use:

* Planner
* Execution Engine
* Shared State
* Agent Registry
* Context Agent
* Retrieval Agent
* Risk Agent
* Recommendation Agent
* Intelligence Fusion Engine
* Memory Service

The Planner decides which capabilities are required.

Agents never directly call each other.

Agents communicate only through Shared State.

---

# RAG Requirements

Use Retrieval-Augmented Generation.

Knowledge sources include:

* Customer Profiles
* CRM Records
* Meeting Transcripts
* Emails
* Support Tickets
* Product Documentation
* Playbooks
* FAQs
* Policies
* Release Notes

Chunk documents.

Generate embeddings.

Store vectors in FAISS.

Ground every recommendation using retrieved evidence.

Never rely solely on LLM knowledge.

---

# Recommendation Requirements

Every recommendation must include:

* Action
* Priority
* Confidence Score
* Supporting Evidence
* Reasoning
* Referenced Knowledge Source

Recommendations without evidence are not acceptable.

---

# Human-in-the-Loop

Every recommendation must support:

* Approve
* Reject
* Override

Approved decisions must be stored in Memory.

Future recommendations should consider previous decisions where appropriate.

---

# Memory Requirements

Memory stores:

* Previous recommendations
* Human decisions
* Outcomes
* Customer history

Memory is organizational knowledge, not conversation history.

---

# Database Requirements

Separate storage into:

1. SQLite for structured operational data.

2. FAISS for vector embeddings.

3. File system for enterprise documents.

Do not store embeddings inside SQLite.

---

# UI Requirements

The UI should include:

* Customer Dashboard
* Decision Workspace
* Planner Panel
* Retrieved Knowledge Panel
* Recommendation Cards
* Human Approval Panel
* Memory Timeline

Every AI decision should be explainable.

---

# Code Quality Requirements

All code must:

Compile successfully.

Use meaningful naming.

Include docstrings where appropriate.

Use type hints.

Avoid placeholder implementations.

Avoid commented-out code.

Avoid dead code.

---

# Testing

After every major implementation phase:

Verify:

* backend starts
* frontend starts
* APIs respond correctly
* database initializes
* imports resolve
* no runtime errors exist

Fix issues before continuing.

---

# Documentation

Keep README updated.

If implementation changes architecture, explain why.

Do not silently change documented behavior.

---

# What NOT to Do

Do NOT:

* Rewrite unrelated files.
* Ignore documentation.
* Simplify architecture without explanation.
* Hardcode values that should be configurable.
* Mix business logic with API or UI code.
* Generate fake implementations just to satisfy interfaces.

---

# Communication Style

Whenever you finish a phase, always provide:

## Summary

What was completed.

## Files Created

List every created or modified file.

## Design Decisions

Explain important architectural choices.

## Remaining Work

Explain what should be implemented next.

Then stop and wait for my approval.

---

# Success Criteria

The final project should demonstrate:

* Enterprise-grade architecture
* Multi-agent orchestration
* Retrieval-Augmented Generation
* Explainable AI
* Human-in-the-loop decision making
* Persistent memory
* Modular and extensible design
* Clean frontend
* Production-quality backend

The judges should perceive ADIP as a reusable **Agentic Decision Intelligence Platform**, not a simple AI application.

Build the project incrementally, maintain architectural integrity, and prioritize correctness, maintainability, and explainability over speed.

Your first task is ONLY to complete Phase 1 (Architecture Validation).

Do not generate any code yet.

Read every document.

Analyze the architecture.

Produce the Architecture Validation Report.

Wait for my approval before implementing anything.
