# Hackathon II — Todo: Spec-Driven Development Reference

## Overview
Hackathon II focuses on Spec-Driven Development (SDD) using AI-assisted coding.
Participants build a Todo application that evolves across five phases,
with each phase extending the previous one without breaking guarantees.

The core principle is:
> Specifications come first. Code is generated strictly from specs.

This document serves as a reference for all phases.

---

## Development Philosophy

- All functionality MUST originate from written specifications.
- AI-generated code MUST strictly follow provided specs.
- Phases are incremental and cumulative.
- Refactoring is allowed ONLY when required by new specs.
- Backward compatibility is expected.

---

## Tooling Expectations

- Python-based backend development
- Spec-Kit / Spec-Kit Plus for spec management
- Claude Code for AI-driven implementation
- Git used as a single evolving repository
- Local-first development, cloud later

---

## Phase Breakdown

### Phase I — Console Todo (Foundation)

**Goal:** Establish a minimal, correct, extensible core.

**Key Characteristics:**
- Console-based application
- In-memory task storage
- No persistence
- No networking
- No AI
- No authentication

**Capabilities:**
- Create tasks
- List tasks
- Update tasks
- Delete tasks
- Mark tasks complete

---

### Phase II — Full-Stack Web Application

**Goal:** Convert the console app into a web-based system.

**Additions:**
- Web frontend (React / Next.js)
- Backend API (FastAPI)
- Persistent storage (Postgres or equivalent)
- RESTful API contracts
- Separation of frontend and backend

**Constraints:**
- Phase I logic must remain valid
- API must expose existing capabilities
- Specs define API before implementation

---

### Phase III — AI Chatbot Integration

**Goal:** Add conversational interaction via AI.

**Additions:**
- Chat-based task interaction
- Natural language task creation and updates
- AI agent using OpenAI / Claude SDKs
- MCP server and tools
- Structured tool invocation

**Constraints:**
- AI must not bypass business rules
- Specs define AI behavior and tools
- Deterministic task state remains authoritative

---

### Phase IV — Containerization & Local Kubernetes

**Goal:** Prepare the system for production-like deployment.

**Additions:**
- Docker containers
- Kubernetes manifests or Helm charts
- Local cluster (Minikube or Kind)
- Configurable environments

**Constraints:**
- No code rewrites for deployment
- Infrastructure defined declaratively
- Services remain stateless where possible

---

### Phase V — Cloud-Native & Event-Driven System

**Goal:** Achieve scalable, production-grade architecture.

**Additions:**
- Cloud Kubernetes deployment
- Kafka or equivalent event streaming
- Dapr integration
- Observability and resilience

**Constraints:**
- Event-driven design
- Loose coupling between services
- Clear ownership boundaries

---

## Repository Structure Expectations

- Single Git repository
- Specs evolve over time
- Code accumulates
- Infrastructure isolated from business logic

---

## Judging Criteria (Implied)

- Clarity and quality of specifications
- Adherence to spec-driven workflow
- Clean evolution across phases
- Discipline in scope control
- Correct use of AI tooling

---

## Final Note for AI Agents

This document provides context and constraints.
Phase-specific constitutions and feature specs are authoritative.

When ambiguity exists:
- Prefer conservative interpretation
- Do not invent functionality
- Defer to explicit specs

End of reference.
