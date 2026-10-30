# 14 — RESEARCH & VALIDATION NOTES

## Purpose
Outside research is used only to improve generic operations/queue/inventory modeling. It does not override explicit Dispo Game/TFS project decisions.

## 1. Queue abandonment
**OUTSIDE RESEARCH:** Garnett, Mandelbaum & Reiman, “Designing a Call Center with Impatient Customers,” *Manufacturing & Service Operations Management* 4(3), 2002. The Erlang-A family explicitly models customers who abandon while waiting, unlike basic Erlang-C queues.

Source: https://pubsonline.informs.org/doi/10.1287/msom.4.3.208.7753

Use in V2:
- patience/abandonment is a real queue state rather than a cosmetic happiness timer;
- waiting-time performance must be measured together with abandonment.

Not copied literally:
- Dispo Game is time-varying, small-server, phase-driven and deliberately game-tuned, so V2 uses a seeded discrete-event harness rather than assuming steady-state Erlang-A equations are the exact game model.

## 2. Server availability
**OUTSIDE RESEARCH:** service-system literature notes that modeling servers as always available can overestimate queue behavior when workers have breaks/after-work/unavailability. V2 therefore explicitly represents staff availability/task states.

Background: Mandelbaum et al., “Erlang-S: A Data-Based Model of Servers in Queueing Networks,” *Management Science*, 2019.
https://doi.org/10.1287/MNSC.2018.3166

Use in V2:
- staff on break/receiving/busy are not simultaneously counted as service capacity.

## 3. Retail assortment breadth/depth/service level
**OUTSIDE RESEARCH:** assortment planning literature treats variety/breadth, depth and service level as interrelated decisions subject to consumer preferences, space and retailer constraints.

Source: Mantrala et al., “Why is Assortment Planning so Difficult for Retailers? A Framework and Research Agenda,” *Journal of Retailing* 85(1), 2009.
https://doi.org/10.1016/j.jretai.2008.11.006

Use in V2:
- breadth vs depth is a core ordering tradeoff;
- storage/space and customer coverage must be visible constraints.

## 4. Safety stock
**OUTSIDE RESEARCH:** safety stock should respond to demand variability, forecast error and lead-time variability rather than a fixed percentage of cycle stock.

Source: Peter L. King, “Crack the Code: Understanding Safety Stock and Mastering its Equations,” APICS/MIT-hosted reading.
https://web.mit.edu/2.810/www/files/readings/King_SafetyStock.pdf

Use in V2:
`SS = z * sqrt(L_mean*sigma_d^2 + demand_mean^2*sigma_L^2)` as an internal configurable planning approximation.

The game exposes risk bands rather than requiring players to calculate the formula.

## 5. Assortment size is not monotonic good
**OUTSIDE RESEARCH:** a 2022 meta-analysis reports that larger assortments can improve choice/sales perceptions but can also raise cognitive effort, uncertainty and avoidance.

Source: Chernev et al., “The effect of retail assortment size on perceptions, choice, and sales: Review and research directions,” *Journal of Retailing* 98(1), 2022.
https://doi.org/10.1016/j.jretai.2022.01.001

Use in V2:
- no assumption that more SKUs is universally better;
- the game values coverage but also storage, operations and complexity.

## 6. Queue simulation
The validation harness is a **game-design model**, not empirical Phoenix-store calibration.

Assumptions:
- phase-specific Gamma renewal arrivals;
- single-player server for baseline floor tests;
- lognormal service/patience;
- service-time medians derived as explicit tuning proposals, not claimed real-store measurements.

Key result used to revise design:
- first-pass 22–25 Standard arrivals was too aggressive at natural service times;
- V2 Standard ~19 arrivals produces ~4% abandonment for targeted play;
- ask-all materially overloads the queue;
- ask-none has better queue performance, proving progression must account for information quality.

## 7. Economy stress test
The 18-SKU model is deliberately stylized. It is used to detect dominant-strategy risk, not to assert real dispensary financial performance.

Observed qualitative result:
- “order everything” improves fill but increases holding/waste;
- margin-only can preserve contribution while damaging coverage;
- therefore service coverage and economic contribution must coexist as separate objectives.

## 8. What outside research did NOT change
- TFS scoring/Similar/parser behavior;
- store physical facts;
- canonical product/batch truth;
- modeled Arizona transaction behavior supplied by the handoff;
- current Unity/Blender authority;
- progression role ladder.
