# UX_PS1 — PS1 "Counter Decisions" UI: cart, limit meter, ID stand, medical POS, strikes (UX-002)

**Owner:** UX-002 · **Consumers:** GAME-006 (cart), GAME-007 (meter, strikes), GAME-008 (ID stand), GAME-009 (medical) · **Status:** draft for review · 2026-10-30
**Inputs:** `Design/SPEC_COMP002.md` (cited **CP§n**), `Design/ROADMAP_POST_SLICE.md` §2, `Specs/UX_SLICE.md` (cited **US§n**), `Specs/SLICE_DESIGN.md` §3–4, `Handoffs/GAME-002.md`, DEC-048 store facts.
**Wireframes:** `Docs/Assets/UX/PS1/ps1_01…ps1_08.svg` (1920×1080 + note strip). Regenerate: `python -I Docs/Assets/UX/PS1/gen_ps1.py Docs/Assets/UX/PS1`. Prices in frames are placeholders (`$xx.xx`); GAME-006 computes them.

Everything not restated here is unchanged from UX_SLICE: tokens and colour (US§6), type scale and safe area (US§5), toast rules (US§3.8), accessibility settings (US§7), focus ring and Back behaviour (US§4). Built as today: UI Toolkit in code + `UI/Slice/Slice.uss` (GAME-002). Values marked [GDD] are UX tuning, not law. Copy rule H1: no effect claims in any string.

## 1. Flow changes

| Step | Slice (US§2) | PS1 |
|---|---|---|
| Results → Choose | present → ACCEPT → POS | Same for the first item. Once the cart has ≥ 1 line, **Choose** reads **Add to cart** (same key); it presents the item and, on ACCEPT, adds the line and opens the register (ps1_01). |
| Register | one item | cart of 1–3 lines, meter, `+ Add item` → Query (ps1_02/03) |
| Rush start | — | optional "cover the ID stand?" prompt → walk to the stand → ID panel × 3 (ps1_04/05) |
| MED customer | — | register in medical mode (ps1_06/07) |
| Strike | — | strike toast (ps1_08), row in the report |

Each item is presented and answered on its own (REJECT reasons stay per item, SLICE_DESIGN §3.5); GAME-006 averages item fit.

## 2. Cart (ps1_01, ps1_02) — GAME-006
- **Request strip** (US§3) ticks each clause already in the cart: "A half of something for sleep ✓ and an eighth of something for energy."
- **Cart chip** top-right of the terminal while the cart has lines: `🛒 Cart {n} / 3 · {g} g`; click or **R** → register without adding.
- **Register panel** 1000×900 (was 1000×840). Top: title + verification badge (`✓ 21+ ID verified`, or the MED badges of §5). Then 1–3 **cart lines**, each 80 px: name, batch · tier, `−` weight `+`, line price (pre-tax), `✕` remove. Weight steps through `STD_WEIGHTS` 3.5/7/14/28; a step is skipped when jar grams < weight (existing "Not enough in the jar" rule). Removing the last line returns to Results.
- `+ Add item` under the lines → Query with the request strip; disabled at 3 lines as "Cart full (3)".
- Totals: Subtotal = Σ line pre-tax; Tax; Total rounded once on the cart (DEC-035). Payment Cash / Card, Hold-to-confirm, Cancel unchanged (US§3.7). Cancel releases nothing (no reservation, SLICE_DESIGN §4) and the customer leaves with no sale if the cart was refused.
- The single-item POS weight tiles are replaced by the line stepper (one control for 1–3 lines).

## 3. Purchase-limit meter (ps1_02, ps1_03) — GAME-007
- Placement: on the register, left column under the lines, above Payment; 440 px bar, label left, `{cart g} / {cap}` right, 75 % tick mark on the bar.
- **States** (icon + word, never colour only):

| State | Rule | Colour | Text under the bar | Confirm |
|---|---|---|---|---|
| Neutral | < 75 % (`meterAmberFraction`) | `--ok` | none | enabled |
| Amber | 75–100 % | `--warn` | `⚠ Near the 1 oz limit` | enabled |
| Red | > 100 % | `--bad` | `✗ Over the 1 oz limit` + boxed hint `Remove a line or step a weight down` | disabled |

- **Per transaction only** (DEC-049): no daily limit. The adult-use meter starts at 0 g for every new cart, including a customer who already bought the max and got back in line; a returning customer is allowed, never a strike, and gets no special UI.
- Entering Red fires the existing `overLimit` toast once ("Over the 1 oz limit", GAME-002 M1). The hint never says which line to drop: that is the decision (CP§2).
- **Packaged goods are out of PS1 scope** (deli only). DEC-050: they are never self-serve; the budtender fetches them from FOH (vapes, edibles, infused prerolls), the fridge (drinks) or the cooler (concentrates, perishable edibles) while the customer waits on the floor. When packaged lines arrive (GAME-004 / PS3), "Add to cart" for a packaged item should start a fetch step (walk or timer, patience keeps draining) before the line appears; the cart line then shows its source (`FOH` / `Fridge` / `Cooler`). Not wireframed here.
- **Concentrate row** (`Concentrate {g} / 5 g`) is built but hidden until PS3 (GAME-014). DEC-048: packaged goods count toward the caps (an edible ≈ 0.1 g). For PS3 the line shows its counted grams under the name (`counts as 0.1 g`) so the meter always adds up; the per-category numbers come from DES/COMP (GAP-COMP-02).

## 4. ID stand (ps1_04, ps1_05) — GAME-008
DEC-048: a guard scans IDs at a stand directly **left inside the entrance**. CP§3's "check-in" is this stand; the UI calls it **ID stand** (see Q1).
- **Prompt** (ps1_04): centred 800×300 card on rush start at `coverCheckInChance`: "⚠ The ID stand is backed up" / "Cover it for the next 3 arrivals?" / "Your counter line keeps waiting while you're away." Buttons **Cover the stand** (Y) and **Stay at counter** (N). The sim does not pause; it auto-declines after 8 s [GDD]. If it fires while a screen is open it waits until that screen closes.
- **Getting there:** accept → world marker on the stand anchor + HUD line `◆ ID stand · {done}/3`. Interact (E) at the stand opens the panel. GAME-008 uses an entry anchor by name or `TEMP_CheckInDesk` (GAP-COMP-08).
- **ID panel** (ps1_05): 1200×900 at left; world dimmed only behind it. Header `ID stand · arrival {i} of 3` and the **in-game date** top-right (`Today: Tue 10/27/2026`). The card is drawn at ID-1 ratio: horizontal 770×486, **vertical** rotated to portrait in the same slot. Fields: state + type in the header band (e.g. ARIZONA · DRIVER LICENSE; passport / military use their own band text), photo, NAME (generated, no real people), DOB, EXP, TYPE, FORMAT. No verdict is shown.
- Buttons **Admit** (A) and **Refuse** (R). Esc closes the panel; arrivals not yet checked wait at the stand.
- **Counter queue while away:** the HUD cluster becomes a **Counter line** strip at top-right (440×420): one patience word + icon per queued customer (`● Relaxed / ◐ Waiting / ▲ Impatient`, forced on while covering, independent of the Patience-hints assist), `◆ Stand: {n} waiting`, clock and sales. It stays until the 3rd ID is done or the player is back at the counter.
- **Result toast** (4 s, under the strip): see §8 strings. Admitting an invalid ID raises the strike toast instead (§6).
- **Assist** `ID age helper` (off by default, US§7 table): adds "Age {n} · expires in {t}" under the card.

## 5. Medical register mode (ps1_06, ps1_07) — GAME-009
Medical customers are rare (under 5 %, DEC-048); same pre-tax prices, lower tax, higher allotment.
- Badge `✓ MED card verified` replaces `✓ 21+ ID verified`.
- Meter becomes `14-day remaining`: cart g / (`medicalLimitGrams14d` − 14-day history), small caption `Allotment 70.87 g · {h} g bought in the last 14 days`, amber/red rules as §3; red text `✗ Over the 14-day allotment`. The 28 g cap is not shown in medical mode.
- Tax line reads `Tax 9.1% (medical)`.
- **Sale type** switch `● Medical / ○ Adult-use` next to Payment (T toggles). Adult-use swaps the tax line to 25.1 % and the meter to Flower / 28 g. Shown only for MED customers.
- **Out-of-state card** (ps1_07): badge `⚠ Card: out-of-state` is the only cue up front. Confirm while Medical: first time blocked + hint toast; later times blocked + strike (CP§4, GAP-COMP-04).

## 6. Strikes and report (ps1_08) — GAME-007 ledger, GAME-008/009 sources
- **Strike toast:** top-left, `--bad` border, `✗ Strike · {reason}` + one flavour line, **6 s** (sale toasts 4 s), never takes focus. Strikes never end the shift (DEC-032).
- **Report:** new **Compliance** block under the slice rows. `Strikes {n}` (+ `⚠ Manager review` at `strikeReviewThreshold`), one indented row per strike `{hh:mm} · {reason}`, then `IDs checked`, `Bad IDs caught`, `Valid IDs refused`, `Over-limit trims`, `Medical sales`, `Medical tax collected`, `Adult-use tax collected` (CP§7). Zero rows still show 0; the three medical rows hide when the shift had no MED customer.

## 7. Input mapping (new controls)
Today's build: mouse + E / Esc / M / F3 (GAME-002). New keys avoid I, C, M, F3 and the 1–5 dialogue keys.

| Control | Keyboard / mouse | Controller |
|---|---|---|
| Add to cart (card) | Enter / click (same as Choose) | Ⓐ |
| Go to register (cart chip) | R / click | Ⓨ hold |
| Cart line focus | ↑ ↓ / hover | D-pad ↑↓ |
| Step weight down / up | ← → or − / + / click | D-pad ←→ |
| Remove line | Del / click ✕ | Ⓧ |
| + Add item | A / click | RB |
| Cover-stand prompt | Y accept · N decline / click | Ⓐ · Ⓑ |
| Open ID panel at stand | E | Ⓐ |
| Admit · Refuse | A · R / click (Enter activates the focused button only) | Ⓐ · Ⓧ |
| Close ID panel | Esc | Ⓑ |
| Sale type toggle (MED) | T / click | LB |
| Close report | Esc / Enter | Ⓑ |

Focus order is the pink numbers in each frame. Default focus: register → line 1; prompt → Cover; ID panel → the card (no button) so a stray Enter cannot admit; Tab → Admit → Refuse. Keyboard focus nav is still unbuilt (GAME-002 open item); these keys work by direct binding meanwhile.

## 8. New strings (for `SliceLines.json`)

| Key | Text | Used by |
|---|---|---|
| `addToCart` | Add to cart | GAME-006 |
| `cartChip` | 🛒 Cart {0} / 3 · {1} g | GAME-006 |
| `goToRegister` | Go to register | GAME-006 |
| `addItem` | + Add item | GAME-006 |
| `cartFull` | Cart full (3) | GAME-006 |
| `removeLine` | Remove | GAME-006 (tooltip / screen reader) |
| `meterFlower` | Flower | GAME-007 |
| `meterConcentrate` | Concentrate | GAME-014 (PS3) |
| `meterValue` | {0} g / {1} g | GAME-007/009 |
| `nearLimit` | ⚠ Near the 1 oz limit | GAME-007 |
| `overLimit` | Over the 1 oz limit (exists; red row adds ✗) | GAME-007 |
| `trimHint` | Remove a line or step a weight down | GAME-007 |
| `countsAs` | counts as {0} g | GAME-014 (PS3) |
| `strikeToast` | ✗ Strike · {0} | GAME-007 |
| `coverPromptTitle` | ⚠ The ID stand is backed up | GAME-008 |
| `coverPromptBody` | Cover it for the next {0} arrivals? | GAME-008 |
| `coverPromptCost` | Your counter line keeps waiting while you're away. | GAME-008 |
| `coverAccept` / `coverDecline` | Cover the stand / Stay at counter | GAME-008 |
| `standHud` | ◆ ID stand · {0}/{1} | GAME-008 |
| `idPanelTitle` | ID stand · arrival {0} of {1} | GAME-008 |
| `idToday` | Today: {0} | GAME-008 |
| `idFields` | NAME / DOB / EXP / TYPE / FORMAT | GAME-008 |
| `idFormatH` / `idFormatV` | Horizontal / Vertical | GAME-008 |
| `idTypes` | Driver license / ID card / Passport / Military ID | GAME-008 |
| `idAdmit` / `idRefuse` | Admit / Refuse | GAME-008 |
| `counterLine` | Counter line ({0}) | GAME-008 |
| `standWaiting` | ◆ Stand: {0} waiting | GAME-008 |
| `idAdmitted` | ✓ Admitted | GAME-008 |
| `idRefusedBad` | ✓ Refused: {0} (reasons: under 21 / expired / vertical ID past 30 days) | GAME-008 |
| `idRefusedValid` | ⚠ Refused a valid ID · they left | GAME-008 |
| `strikeBadId` | An invalid ID got through | GAME-008 |
| `fineFlavor` | Stores can be fined up to $2,000 per violation. | GAME-008 (CP§3, B4) |
| `idAgeHelper` | Age {0} · expires in {1} | GAME-008 (assist) |
| `medVerified` | ✓ MED card verified | GAME-009 |
| `medOutOfState` | ⚠ Card: out-of-state | GAME-009 |
| `med14d` | 14-day remaining | GAME-009 |
| `medAllotmentCaption` | Allotment {0} g · {1} g bought in the last 14 days | GAME-009 |
| `overMedLimit` | ✗ Over the 14-day allotment | GAME-009 |
| `taxMedical` | Tax {0}% (medical) | GAME-009 |
| `saleType` / `saleMedical` / `saleAdultUse` | Sale type / Medical / Adult-use | GAME-009 |
| `oosHintTitle` | ⚠ Can't ring an out-of-state card as medical | GAME-009 |
| `oosHintBody` | Switch the sale to Adult-use (21+, 1 oz limit). | GAME-009 |
| `strikeOosMed` | Rang an out-of-state card as medical | GAME-009 |
| `reportCompliance` | Compliance | GAME-007 |
| `reportRows` | Strikes / Manager review / IDs checked / Bad IDs caught / Valid IDs refused / Over-limit trims / Medical sales / Medical tax collected / Adult-use tax collected | GAME-007/008/009 |

All strings are procedural or legal-fact text; none claims an effect (H1).

## 9. Validation
- CP§2 controls (meter, red block, trim by remove/step, no-sale on Cancel): ps1_02, ps1_03. CP§3 (prompt, Admit/Refuse, card fields, date, toast, queue cost visible): ps1_04, ps1_05. CP§4 (MED badge, 14-day meter, 9.1 % tax, out-of-state badge, adult-use switch): ps1_06, ps1_07. CP§7 rows + strike toast: ps1_08. Cart entry point and lines: ps1_01, ps1_02. ✔
- Every new string is in §8. ✔ Each SVG < 10 KB. ✔
- Example ID in ps1_05: DOB 11/14/2005 on Tue 10/27/2026 → age 20 → Refuse is correct. Meter examples: 14 + 3.5 + 3.5 = 21 g = 75 % (amber); 28 + 3.5 = 31.5 g (red); MED 70.87 − 21.5 = 49.37 g, cart 42 g → 85 % (amber).
