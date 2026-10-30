# 08 — UX & INTERACTION DESIGN

## 1. UX thesis
The player should be able to move from human conversation to canonical TFS to physical fulfillment without losing context. Menus accelerate decisions; they do not replace the store.

## 2. Top-level interaction state

`WORLD -> CUSTOMER_DIALOGUE -> TFS -> PRODUCT_COMMITMENT -> RETRIEVAL -> WEIGH/SCAN -> POS -> COMPLETE -> WORLD`

Optional branches:
- TFS -> Compare -> TFS
- TFS -> Similar -> TFS
- Customer Dialogue -> Clarify -> Customer Dialogue
- Product Commitment -> Alternate -> TFS
- POS -> Correct Basket -> Retrieval/TFS
- any reversible panel -> Back

## 3. Input baseline
All inputs remappable.

Keyboard/mouse proposal:
- `E`: world interact / confirm context action
- `Q`: clarification menu for active customer
- `R`: open/reopen canonical TFS with active KnownCustomerProfile
- `Tab`: Floor Mode
- `C`: Compare selected results
- `S`: Similar when a valid reference exists
- `F`: contextual quick action
- `1–5`: select visible action/result slot
- `Esc`: back one layer; hold to close to world where safe
- mouse: standard selection/scroll

No core action depends on a chord.

## 4. Controller
- South/A/Cross: interact/confirm
- East/B/Circle: back
- West/X/Square: context quick action
- North/Y/Triangle: active customer/TFS
- LB/RB: cycle relevant panels/results
- D-pad: quick question/result slots
- stick: world movement or UI navigation by focus

Controller path must complete 100% of a normal transaction without virtual mouse precision.

## 5. Focus model
Only one of these owns directional/key focus:
- world;
- dialogue choices;
- TFS result list;
- compare/details;
- POS;
- manager dashboard.

Transition displays a 100–150ms focus cue, not a modal fade.

## 6. Customer HUD
Compact card contains **known** information only:
- customer line/opener transcript;
- parsed/stated intent summary;
- known avoidances;
- known budget;
- known product/quantity preference;
- legitimate repeat-history cue;
- consultation cue only if behavior makes it observable.

Unknown fields are absent, not shown as “???,” because that would reveal that a hidden constraint definitely exists.

## 7. Clarification UI
Press Q for 3–5 context-valid questions.

Rules:
- do not show impossible/irrelevant questions;
- previously answered redundancy group is muted;
- no “recommended question” highlight by default;
- always include `Recommend now` / exit path;
- response writes facts to KnownCustomerProfile before TFS rerun.

Question menu should take <300ms to open and permit number/D-pad selection.

## 8. TFS integration
Modes:
1. Floor Mode
2. Recommendation/Search
3. Compare
4. Similar
5. Details/Explanation

### Persistent context
Top bar shows active customer + known constraints + inventory snapshot timestamp/status.

Results change only when:
- TFS input changes;
- authoritative eligible inventory changes;
- mode/query explicitly changes.

Never silently refresh because difficulty changed.

## 9. Floor Mode
Purpose: high-speed service under pressure.

Show:
- top actionable results;
- price/tier if canonical source supports it;
- concise effect/profile text from preserved TFS behavior;
- stock state/location;
- one-key Compare/Similar/details.

Floor Mode is not a simplified recommendation engine. It is a compact view of the same truth.

## 10. Result commitment
Selecting a product creates a `ProductIntent`, not an immediate sale.

`ProductIntent` contains:
- item/batch ID;
- customer/transaction ID;
- selected TFS snapshot;
- requested quantity;
- intended retrieval location.

The world can highlight the correct location if assist is enabled.

## 11. Physical retrieval
Player must reach and interact with the authoritative item location.

Error prevention:
- label batch/item clearly on interaction;
- if player picks a different same-name batch, show batch mismatch before transaction commit;
- if stock changes after recommendation, mark result stale and offer rerun/alternate.

## 12. Deli weighing
Scale interface:
- target grams;
- current grams;
- difference;
- tolerance state;
- tare/reset where physically applicable.

Inventory handling:
- scooped quantity is temporary handling state;
- authoritative available stock is reserved/temporarily allocated as appropriate;
- permanent SOLD decrement occurs at transaction completion;
- cancel returns handled amount exactly once.

Difficulty/assist changes tolerance, not grams in ledger.

## 13. Packaged retrieval
Flow:
`select -> retrieve physical unit -> scan/select -> basket`

No weighing. If FOH is empty but BOH exists, the physical transfer/retrieval rule applies; the menu cannot teleport it.

## 14. POS
Default normal checkout fits on one primary screen:
- basket lines;
- quantity;
- price/deal/tax calculation from PricingService;
- modeled transaction-limit check;
- confirm payment abstraction.

Only exceptions open additional UI.

## 15. Warning tiers
### Informational
- LOW stock
- deal ending
- repeat-history note

No modal.

### Correctable warning
- wrong batch/item;
- selected quantity unavailable;
- deal ineligible;
- stale TFS inventory snapshot.

Inline blocker with one-click corrective path.

### Hard blocker
- invalid modeled transaction limit;
- no reserved quantity;
- transaction state conflict;
- authoritative stock insufficient.

Cannot complete until resolved.

## 16. Inventory cues
World + Floor Mode use text/icon shape as well as color:
- HEALTHY
- LOW
- CRITICAL
- EMPTY WITH BACKSTOCK
- SOLD OUT

No color-only communication.

## 17. Queue cues
Show:
- count;
- trend arrow;
- oldest-wait severity band;
- optional staff coverage icon at Lead+.

Do not expose exact hidden abandonment seconds.

## 18. Rush shortcuts
Allowed:
- reopen active TFS context;
- select result row by number;
- jump to prior-purchase context for legitimate repeat;
- Compare two selected rows;
- mark world retrieval target;
- fast-add already physically retrieved packaged item.

Not allowed:
- auto-ask best question;
- auto-select “correct” product;
- auto-weigh;
- teleport inventory;
- auto-complete sale.

## 19. Manager UX
Use a single operational dashboard with tabs, not separate full-screen applications:
- Floor
- Staff/Tasks
- Inventory
- Orders
- Forecast/Report

Urgent floor state remains visible as a compact strip while in management views.

## 20. Back/cancel contract
- Back never commits state.
- Closing TFS keeps customer session alive.
- Cancel ProductIntent releases only its reservation/temporary handling.
- Cancel transaction never edits completed ledger.
- Manager draft changes do not apply until explicit submit.

## 21. Accessibility
Must support:
- text scaling;
- subtitles/transcript persistence;
- high contrast;
- non-color state icons;
- remapping;
- hold/toggle options;
- reduced camera motion;
- simplified weighing;
- patience assist;
- interaction highlighting;
- persistent known-intent summary;
- recommendation explanation expansion;
- optional UI clock slowdown as an explicit assist.

## 22. Performance targets
- Floor Mode open: perceived immediate, target <150ms local UI response.
- question menu: <150ms.
- TFS response: preserve current implementation performance budget; show non-blocking spinner only if >250ms.
- world-to-POS no unnecessary fade/scene load.

## 23. UX acceptance scenarios
- explicit regular: opener -> TFS -> product -> retrieval -> POS with no extra modal;
- ambiguous novice: question -> new known fact -> rerun TFS without losing context;
- repeat: prior history visible but current request can override it;
- wrong batch: warning before commit;
- sold-out after recommendation: stale-state warning + alternate path;
- controller completes all above.
