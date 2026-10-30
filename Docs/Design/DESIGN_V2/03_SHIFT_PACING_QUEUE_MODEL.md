# 03 — FULL SHIFT PACING & QUEUE MODEL

## 1. Baseline decision
**NEW PROPOSAL, numerically validated:** Standard full shift target is **32 real minutes**, with approximately **18–20 customer arrivals** under the single-player floor baseline.

The previous V1 target of 22–25 is rejected because it created excessive abandonment when combined with natural consultation/service times.

## 2. Why a queue model exists
Queue pressure is gameplay only if:
- waiting customers can accumulate;
- patience is heterogeneous;
- service choices alter service time;
- recovery is possible after a rush;
- a fast-but-poor and slow-but-thorough strategy each have costs.

## 3. Arrival process
Use a **bounded-renewal** process rather than unconstrained Poisson arrivals for ordinary game shifts.

Per phase, inter-arrival time is sampled from a Gamma distribution:

`InterArrival ~ Gamma(shape=k, scale=(60/lambda)/k)`

where `lambda` is arrivals/minute.

This preserves variability but reduces absurd clustering that is neither fun nor necessary for realism. Special/event arrivals use dedicated seeded slots.

### Standard phase table

| Phase | Time | Base arrival rate/min |
|---|---:|---:|
| Opening | 2 min | 0.12 |
| Steady A | 5 min | 0.54 |
| Rush 1 | 6 min | 0.96 |
| Recovery | 4 min | 0.30 |
| Rush 2 | 6 min | 1.08 |
| Late | 5 min | 0.54 |
| Closing/report | 4 min | 0.00 |

Gamma shape `k=2.5`.

Add 2 seeded special/repeat/event customer slots between minute 5 and 27.

Simulation mean: ~19.3 arrivals.

## 4. Beginner shift
Length: 26 min.

| Phase | Time | rate/min |
|---|---:|---:|
| Opening | 2 | 0.09 |
| Steady | 5 | 0.54 |
| Rush 1 | 4 | 0.86 |
| Recovery | 4 | 0.32 |
| Rush 2 | 4 | 0.99 |
| Late | 4 | 0.54 |
| Report | 3 | 0 |

`k=3.0`, plus 1 special slot.

Validated replay mean: ~13.0 arrivals, ~0.1% abandonment under targeted play in the stress harness.

## 5. Expert shift
Length: 35 min.

| Phase | Time | rate/min |
|---|---:|---:|
| Opening | 2 | 0.13 |
| Steady | 5 | 0.55 |
| Rush 1 | 7 | 0.94 |
| Recovery | 4 | 0.32 |
| Rush 2 | 7 | 1.02 |
| Late | 6 | 0.55 |
| Report | 4 | 0 |

`k=2.2`, plus 2 special slots.

Validated replay mean: ~21.8 arrivals and ~6.6% abandonment under targeted single-player play. Expert management/staff scenarios may support greater arrival volume because effective server capacity is higher; do not reuse this single-server table unchanged for a staffed floor.

## 6. Service-time model
Service time includes customer interpretation, TFS use, retrieval/weighing/scan and POS for the single-player baseline.

Base median seconds before ambiguity adjustment:

| Archetype | Median |
|---|---:|
| Decisive repeat | 32 |
| Price shopper | 40 |
| Regular | 46 |
| Novice | 58 |
| Enthusiast | 72 |
| Indecisive | 76 |

Lognormal sigma: 0.20 initial tuning.

### Targeted-question time adders
- ambiguity 0: +0 sec
- ambiguity 1: +8 sec
- ambiguity 2: +14 sec
- ambiguity 3: +22 sec
- Enthusiast typical compare overhead: +6 sec

This produces approximately 60 sec median service in the Standard validation model.

### Strategy stress cases
- `ASK_ALL`: +42 sec average question overhead.
- `ASK_NONE`: -6 sec against targeted baseline, but creates information-quality risk.

These are validation strategies, not literal player action durations.

## 7. Patience
Patience is waiting tolerance before service, not customer health.

Base median seconds:
- Low: 140
- Normal: 230
- High: 330

Distribution: Lognormal sigma 0.35.

Class mix initial Standard: 20% / 60% / 20%.

Difficulty multiplier:
- Beginner 1.35x
- Standard 1.00x
- Expert 0.88x

A customer’s exact abandonment threshold is seeded and hidden.

## 8. Active-service patience
Once service begins, use `EngagementState`:
- useful clarification/explanation: active patience decay 0.25–0.50x;
- ordinary productive service: 0.75x;
- idle/no-progress: 1.0x;
- repeated redundant loop: 1.25x.

Cap any engagement-derived patience relief to 60 sec per interaction. This prevents infinite Compare abuse.

## 9. Queue states
For single-player Standard:
- `CLEAR`: 0 waiting
- `NORMAL`: 1–2
- `PRESSURE`: 3–4
- `CRITICAL`: 5–6
- `OVERLOAD`: 7+

These are presentation states, not hard mechanics. Expert/staffed scenarios can use capacity-relative thresholds.

## 10. Queue telemetry
Track:
- peak waiting count;
- mean/p90 wait;
- abandonment;
- arrival-to-service latency;
- time-to-clear after peak;
- player-attributable vs structural abandonment;
- queue pressure at every player decision.

## 11. Attribution
Do not blame the player for impossible traffic.

Attribution baseline is scenario expected capacity. An abandonment is `player_attributable` only when one or more of these are true:
- redundant consultation above configured allowance;
- avoidable idle time;
- avoidable incorrect retrieval/rework;
- preventable stock workflow interruption;
- poor staffing assignment at management rank.

If seeded demand exceeds intended capacity despite competent benchmark play, classify as `structural_pressure` and do not heavily penalize progression.

## 12. Recovery windows
After a sustained rush >=5 min, Standard should provide 3–4 minutes of reduced arrival pressure unless scenario-authored otherwise.

Recovery decisions:
- proactive restock;
- receive/prepare delivery;
- inspect critical stock;
- clean/organize lightweight state;
- staff/break correction;
- wait for next customer.

Recovery is not free. Choosing a 45-sec restock means accepting the risk of a customer arriving during it.

## 13. Restock pacing
Standard full shift target:
- 2–4 meaningful restock decisions;
- 1–2 proactive opportunities;
- 0–2 reactive interruptions depending on player preparation;
- >2 emergency restocks means the inventory/decision model is creating chore spam or the player has materially mismanaged stock.

## 14. Operational events
Standard:
- 1 major event maximum by default;
- 1–2 minor events;
- flavor events do not consume major task budget.

Expert may have 2 major concurrent demands only if at least one can be delegated or deferred.

## 15. Quiet-time compression
Allow time acceleration/advance only when:
- no current customer;
- no customer within configured short horizon;
- no low/critical decision requiring attention;
- no active delivery/escalation;
- no staff decision due;
- no meaningful task currently available.

Time acceleration stops before the next meaningful event. It cannot skip a decision.

## 16. Simulation results
Stress harness uses 700 deterministic seeds per strategy/profile.

### Standard, same traffic
| Strategy | arrivals | abandonment | mean wait | mean max queue | median service |
|---|---:|---:|---:|---:|---:|
| Targeted | 19.3 | 4.1% | 45 sec | 3.1 | 60 sec |
| Ask everything | 19.3 | 19.0% | 97 sec | 4.4 | 93 sec |
| Ask nothing | 19.3 | 0.9% | 22 sec | 2.3 | 44 sec |

The queue model alone makes `ASK_NONE` look efficient; progression/DecisionQuality must therefore penalize avoidably uninformed decisions. This is intentional cross-system design, not a queue bug.

### Expert targeted
~21.8 arrivals, ~6.6% abandonment, ~50 sec mean wait, mean max queue ~3.4.

### Beginner targeted
~13.0 arrivals, ~0.1% abandonment, ~21 sec mean wait, p90 max queue ~3.

## 17. Acceptance gates
Standard benchmark bot/policy should satisfy:
- 18–20 mean arrivals;
- 2–6% abandonment;
- mean peak queue 2.5–3.5;
- p90 peak queue <=5;
- mean service 55–70 sec;
- Rush 1/2 queue can recover during recovery/late windows.

If later physical interaction telemetry increases median service above 70 sec, lower traffic before lowering patience.
