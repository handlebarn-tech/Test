# 04 — DIFFICULTY SYSTEM

## 1. Invariant
Difficulty changes **decision complexity and concurrency**, never canonical TFS recommendation truth.

## 2. Difficulty axes
Internally tune 11 independent axes:
1. ambiguity;
2. number of simultaneous customer constraints;
3. constraint conflict/no-perfect-fit frequency;
4. inventory scarcity;
5. arrival pressure;
6. patience;
7. operational-task concurrency;
8. repeat-customer complexity;
9. staff coverage pressure;
10. product/category breadth;
11. physical precision.

## 3. Player-facing custom controls
Expose five understandable controls:
- Customer Complexity
- Traffic Pressure
- Inventory Pressure
- Operational Load
- Physical Precision

Patience is derived mainly from Traffic Pressure and accessibility assists; TFS is never a slider.

## 4. Presets

| Lever | Beginner | Standard | Expert |
|---|---|---|---|
| Ambiguity 0/1/2/3 | 45/40/13/2 | 25/40/25/10 | 10/30/40/20 |
| Multi-constraint | 15–25% | 35–50% | 55–70% |
| Tradeoff/no-viable | 3–6% | 10–20% combined | 18–33% combined |
| Single-player arrivals | ~13/26m | ~19/32m | ~22/35m |
| Patience multiplier | 1.35 | 1.00 | 0.88 |
| Meaningful restocks | 1–3 | 2–4 | 3–5 |
| Major concurrent tasks | 0–1 | 1 | 1–2, if delegable |
| Repeat complexity | exact/simple | mixed | changed-use/new-batch/dissatisfied |
| Category breadth | narrow | normal | broad |
| Weigh tolerance | generous | normal | tight but readable |

## 5. Difficulty budget
Do not max every axis simultaneously.

Each generated shift receives a `PressureBudget` of points.

Standard example budget = 10:
- high-ambiguity customer slot: 1
- no-perfect-fit slot: 1
- rush intensity +1 tier: 2
- critical stock state at opening: 2
- delivery collision: 3
- staff shortage: 3
- register/station outage: 3

Ordinary Standard generation should spend 6–10. Expert 10–15. Beginner 2–5.

This keeps difficulty legible and prevents accidental impossible stacks.

## 6. Complexity progression order
When increasing challenge, prefer:
1. ambiguity;
2. constraint combinations;
3. inventory tradeoffs;
4. concurrency;
5. traffic;
6. patience reduction.

Patience is the last lever because pure timer pressure is the least interesting form of difficulty.

## 7. Inventory difficulty
Difficulty may alter:
- proportion of LOW/CRITICAL stock;
- breadth of backstock;
- probability best-fit item is inconveniently located;
- supplier availability in management scenarios.

It may not hide stock state that the player should reasonably know merely to manufacture failure.

## 8. Repeat-customer difficulty
Beginner repeat:
- exact prior purchase still in stock.

Standard:
- prior item unavailable;
- Similar request;
- one changed preference.

Expert:
- same strain/new batch;
- prior dissatisfaction plus changed use;
- conflicting memory and current statement requiring clarification.

## 9. Staff/manager difficulty
Harder management means:
- tighter but feasible coverage;
- more overlapping responsibilities;
- less redundant capability;
- higher opportunity cost for intervention.

It does not make employees irrational or randomly disobedient.

## 10. Physical precision
Tunable:
- interaction target size;
- scale tolerance;
- scan/selection assistance;
- movement/camera assists.

Physical difficulty cannot cause hidden inventory math differences.

## 11. Accessibility assists
Orthogonal to difficulty:
- +25% / +50% patience;
- simplified weighing;
- reduced rush density;
- persistent known-intent summary;
- recommendation explanation expansion;
- interaction highlighting;
- high contrast;
- text scaling;
- controller aim assistance;
- optional slower clock while a detail panel is open.

Progression targets are assist-aware. The game does not shame or block promotion for accessibility use; target baselines adjust to the selected configuration.

## 12. No hidden dynamic difficulty by default
Do not secretly lower TFS complexity or change future outcomes because the player performed badly.

Optional `Adaptive Assistance` may suggest visible assists after repeated failures, but applying them is explicit.

## 13. Scenario difficulty metadata
Every authored scenario records:
- intended preset;
- pressure-budget spend;
- expected benchmark abandonment;
- expected service-time band;
- expected peak queue;
- required competencies;
- whether management delegation is expected.

## 14. QA invariants
- Same TFS fixture passes on all presets.
- Difficulty only changes allowed generator/store/traffic values.
- Expert is demonstrably harder for benchmark policy without changing canonical result for identical customer/store input.
- Beginner still requires information and inventory decisions.
