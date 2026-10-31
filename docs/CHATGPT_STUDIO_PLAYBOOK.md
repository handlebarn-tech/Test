# ChatGPT Studio Playbook

> **Status: NON-CANONICAL WORKFLOW GUIDANCE**
>
> This document is a usage guide for Nolan. It is **not** project design authority, implementation authority, a studio operating system, a decision record, or a replacement for canonical project documentation. Claude/Fable workers must not treat this file as a source of game truth unless Nolan explicitly promotes a specific conclusion into the project's canonical authority structure.

## Purpose

Use ChatGPT as an independent research, design, verification, and QA layer around the implementation studio rather than merely as a document generator.

Recommended separation of responsibilities:

- **Nolan — Product owner:** sets intent, priorities, taste, constraints, and final decisions.
- **ChatGPT — Independent intelligence layer:** researches, challenges, reconciles, audits, tests assumptions, and prepares integration-ready conclusions.
- **Fable Hub / Claude — Implementation manager:** owns the live repository, implementation planning, worker dispatch, integration, commits, and canonical project state.
- **Workers — Execution:** implement bounded tasks under Hub management.
- **ChatGPT after implementation — Independent QA:** checks whether completed work actually satisfies Nolan's intent and the relevant project authority.

The objective is not to create another management layer. ChatGPT should reduce ambiguity and catch errors before they propagate into canonical project state.

---

## 1. Pre-Implementation Design Challenge

### Use when
A feature, system, packet, mechanic, workflow, or major implementation idea is about to enter the studio.

### Give ChatGPT
- the proposed material;
- relevant canonical design/architecture files;
- known constraints;
- the intended player or studio outcome.

### Ask for
- hidden assumptions;
- contradictions;
- implementation ambiguity;
- unnecessary complexity;
- missing interactions with existing systems;
- requirements that sound good but may create bad gameplay;
- places Claude could reasonably interpret the material in multiple ways;
- what should remain untouched.

### Desired output
A decision-oriented audit, not a rewritten document by default.

### Starter prompt
> Audit this before it enters implementation. Do not improve it merely because more detail is possible. Determine what already works, what is genuinely broken or ambiguous, what conflicts with existing project truth, what Claude could misinterpret, and what would create downstream problems. Separate required corrections from optional ideas. Do not create new project authority.

---

## 2. Independent Parallel Design

### Use when
A problem is important enough that a single design path could create tunnel vision.

Examples:
- customer simulation;
- economy/progression;
- traffic and parking;
- employee behavior;
- transaction flow;
- procedural asset strategy;
- UX systems.

### Method
Use separate chats as genuinely independent designers. Avoid showing one chat another chat's reasoning until both have produced conclusions.

Then use a third pass to reconcile them.

### Desired output
- areas of agreement;
- meaningful disagreements;
- strongest solution from each;
- incompatibilities;
- a merged recommendation only where evidence supports one.

### Starter prompt
> Independently solve this design problem from the supplied project constraints. Do not assume an existing proposed solution is correct. Optimize for the intended game experience, implementation clarity, and integration with existing systems. Mark assumptions as assumptions.

---

## 3. Cross-Document Conflict and Authority Audit

### Use when
Several design packets, handoffs, audits, decisions, or implementation documents touch the same system.

This becomes increasingly important as the project corpus grows.

### Ask ChatGPT to detect
- duplicated ownership;
- conflicting sources of truth;
- stale rules;
- requirements repeated with different wording;
- implementation notes presented as design authority;
- assumptions presented as facts;
- circular references;
- files that tell workers to search the wrong place for authority;
- rules that silently override newer decisions;
- independent packets that accidentally define the same behavior.

### Desired output
An **authority/dependency/conflict map**, not another broad rewrite.

Suggested categories:

| Classification | Meaning |
|---|---|
| Canonical owner | File/system that should own the rule |
| Consumer | May reference the rule but should not redefine it |
| Duplicate | Repeats authority and risks drift |
| Conflict | Gives materially different instructions |
| Stale | Previously valid but superseded |
| Provisional | Useful but not established truth |
| Missing owner | Rule exists but has no clear canonical home |

### Starter prompt
> Build an authority, dependency, and conflict map for these files. Do not redesign the systems. Identify who owns each rule, which files merely consume it, duplicated truth, stale authority, contradictions, dangerous search instructions, assumptions stated as facts, and any rule with no clear owner. Recommend the smallest reconciliation necessary.

---

## 4. Research Sandbox

### Use when
External knowledge could improve a design but should not immediately become project truth.

Examples:
- Unity architecture;
- Blender procedural workflows;
- traffic simulation patterns;
- game economy design;
- environmental storytelling;
- UI/UX conventions;
- real retail or dispensary operations;
- technical tooling and model capabilities.

### Principle
Research aggressively outside the project, but keep three things distinct:

1. **Evidence / observed practice**
2. **Inference**
3. **Recommendation for this game**

Do not let external research overwrite project-specific facts.

### Desired output
Only the conclusions worth considering for integration, with assumptions clearly marked.

### Starter prompt
> Research this topic deeply, but treat the project facts I provide as constraints. Separate external evidence, your inference, and your recommendation. Do not convert research into project authority. End with the smallest set of findings that would materially improve this project.

---

## 5. Integration-Ready Delta

### Use when
Research or a design audit produced useful conclusions and those conclusions need to enter the implementation studio.

### Prefer this over
Sending Claude another long standalone design document that restates existing systems.

### Output should specify
- what remains unchanged;
- what changes;
- why the change is needed;
- canonical authority affected;
- dependencies;
- affected systems/files;
- acceptance criteria;
- explicit non-goals;
- what must **not** be reinterpreted or redesigned;
- unresolved items that remain Nolan decisions.

### Starter prompt
> Convert these approved findings into an integration-ready delta for the Fable Hub. Do not create a parallel specification. State what remains unchanged, the minimum required changes, authority affected, dependencies, acceptance criteria, explicit non-goals, and anything the Hub must not reinterpret. Preserve existing canonical ownership.

---

## 6. Completion Report Interrogation

### Use when
Hub or a worker reports that something is finished.

This is one of the highest-value independent uses of ChatGPT.

### Give ChatGPT
- original task or packet;
- relevant authority;
- completion report;
- diff/test output when available;
- screenshots or build evidence when relevant.

### Ask
- What was actually proven?
- Which claims are unsupported by evidence?
- Did scope expand?
- Were requirements silently dropped?
- Did implementation introduce new authority?
- Were acceptance criteria actually tested?
- Are tests validating behavior or merely implementation details?
- Did the worker interpret ambiguous language instead of escalating it?
- Does the result satisfy Nolan's intent, not merely the worker's own documentation?

### Starter prompt
> Treat this completion report as an unverified claim. Compare it against the original task and relevant authority. Determine what is actually proven, what remains unverified, what was omitted, whether scope drift occurred, whether any new authority was invented, and what evidence would be required before I should accept the work as complete.

---

## 7. Player-Experience QA

### Use when
The implementation is technically valid but needs evaluation as a game.

### Give ChatGPT
- screenshots;
- short recordings or frame sequences;
- UI states;
- gameplay descriptions;
- timings;
- interaction flow;
- build/test observations.

### Evaluate separately from code correctness
- readability;
- pacing;
- responsiveness;
- friction;
- player comprehension;
- visual hierarchy;
- environmental believability;
- interaction burden;
- reward clarity;
- repetition;
- whether systems create the intended feeling;
- whether technically sophisticated behavior is actually fun.

### Starter prompt
> Evaluate this as a player, not as the engineer who built it. Ignore implementation elegance unless it affects the experience. Identify what feels good, what is confusing or tedious, where pacing breaks, what the player can and cannot infer, and where the result fails to create the intended experience. Do not propose additional systems unless a demonstrated problem requires one.

---

## 8. Project History / Decision Reconstruction

### Use when
Something in the current project feels wrong and the question is historical:

- When did this rule appear?
- Was this intentional?
- Which version changed the behavior?
- Was a provisional idea accidentally promoted?
- Why is the Hub doing this?
- Which older packet is still influencing current work?

### Desired output
A chronology with confidence levels and evidence, distinguishing:

- original intent;
- later interpretation;
- formal decision;
- implementation;
- subsequent modification;
- current canonical state.

### Starter prompt
> Reconstruct the history of this rule/system from the supplied chats, files, decisions, and reports. Identify the original intent, when wording changed, when it became canonical if ever, later reinterpretations, and the current authoritative state. Flag gaps rather than filling them with assumptions.

---

## What ChatGPT Should Usually NOT Do

Do not automatically use ChatGPT to:

- rewrite every document;
- make every system more detailed;
- create a new `.md` file for every conversation;
- invent missing project facts;
- create another operating system around the Hub;
- duplicate canonical rules into convenience documents;
- act as a persistent department lead;
- manage workers that are already owned by Hub;
- validate a proposal merely because it is internally consistent;
- optimize implementation at the expense of the intended player experience;
- convert external research directly into project truth.

Sometimes the correct output is:

- **no change needed**;
- **the proposed feature should be rejected**;
- **the existing design is already sufficient**;
- **there is not enough evidence to decide**;
- **this belongs in an existing authority file rather than a new document**.

---

## Recommended Flow for Important Work

```text
Nolan intent
    ↓
Independent ChatGPT research/design challenge
    ↓
Nolan decision
    ↓
Integration-ready delta
    ↓
Fable Hub plans + dispatches
    ↓
Workers implement
    ↓
Hub integrates + verifies
    ↓
Independent ChatGPT completion/experience audit
    ↓
Nolan accepts, rejects, or requests correction
```

Not every task requires every stage. Use the additional layers only when they reduce meaningful project risk.

---

## Core Rule

**ChatGPT should increase the quality of decisions entering and leaving the implementation studio without becoming another source of project authority.**

The value is independence: the implementation studio can become internally consistent while still being wrong. ChatGPT is most useful when it challenges that consistency against Nolan's actual intent, external evidence, player experience, and the project's real canonical authority.