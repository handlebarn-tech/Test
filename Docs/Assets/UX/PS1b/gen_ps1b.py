# Generates UX-005 (PS1b counter intelligence) wireframes (static SVG). Usage: python -I gen_ps1b.py <outdir>
# Reuses the PS1 drawing kit (everything in ../PS1/gen_ps1.py above its screen list) so tokens stay identical.
import sys, os
_kit = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "PS1", "gen_ps1.py")
exec(open(_kit, encoding="utf-8").read().split("\nscreens = []")[0])

INFO = "#c3c9d2"  # CUSTOMER INFO tag: neutral text colour, never --ok/--warn/--bad (those belong to TFS fit labels)

def known(s, x, y, facts, info, w=1520):
    """KNOWN-facts row: fact chips (value + source glyph) left, square-cornered CUSTOMER INFO tag right."""
    s.r(x, y, w, 56, fill="#11141a", stroke="none", rx=8)
    s.t(x + 16, y + 36, "KNOWN", 16, T3, 700)
    cx = x + 96
    for txt in facts:
        cx = s.chip(cx, y + 11, txt, T2, 16)
    tw = int(len(info) * 16 * 0.6) + 40
    s.r(x + w - tw - 12, y + 9, tw, 38, fill="none", stroke=INFO, rx=2)
    s.t(x + w - tw + 6, y + 35, info, 16, INFO, 700)

def strip(s, line, facts, info, y=170):
    s.r(200, y, 1520, 56, fill="#11141a", stroke="none", rx=8)
    s.t(224, y + 37, line, 22, T2)
    known(s, 200, y + 64, facts, info)

screens = []
FACTS = ["Effect: relaxing 💬", "Stay functional: yes ❓", "Budget: ≈ $20 ❓"]

# 01 dialogue + question menu
s = S("cx_01_questions", "CX-01 Dialogue: question menu + KNOWN strip")
world(s, "customer at the counter (world, not dimmed)")
s.r(96, 70, 1290, 120, fill="#0f1215cc", stroke="none")
known(s, 112, 86, ["Effect: relaxing 💬", "Stay functional: yes ❓"], "◐ CUSTOMER INFO PARTIAL", w=1258)
s.t(112, 172, "glyphs: 💬 said it  ❓ you asked  ↩ follow-up  ✋ after a rejection  ↺ remembered  🧾 history", 16, T3)
s.r(360, 820, 1200, 150, fill="#0f1215e6", stroke="none")
s.t(390, 856, "Customer · Normal", 18, T3, 600)
s.t(390, 900, "“Yeah, I've got stuff to do after.”", 28, T1)
s.r(1500, 250, 380, 540, fill=PANEL, stroke=LINE, rx=12)
s.t(1524, 290, "Ask… (Backspace: back)", 18, T3, 600)
qs = ["1  What are you looking for?", "2  Anything you don't want?", "3  Need to stay functional?", "4  Trying to stay under anything?",
      "5  Had anything you liked?", "6  Anything you didn't like?", "7  When will you use it?"]
for i, q in enumerate(qs):
    s.r(1516, 310 + i * 66, 348, 56, fill=CARD, stroke=ACC if i == 0 else LINE, rx=8, sw=4 if i == 0 else 2)
    s.t(1532, 346 + i * 66, q, 18, T1)
s.f(1, 1506, 310)
s.note("Dialogue options: 1 Look it up · 2 Ask… (opens this list) · 3 Nothing fits right now (after a search). The list replaces the options column; 1–7 ask; Backspace/Ⓑ returns.")
s.note("Every question stays askable and looks the same before and after it is answered: no grey-out, no tick, no 'already known' hint (DP §10). Q5 (product type) waits for PS3.")
s.note("The answer plays as a subtitle; a new fact drops into KNOWN with its source glyph. A known field asked again: customer restates it, KNOWN unchanged. Too many: DP §12 deflection lines.")
screens.append(s)

# 02 query preview
s = S("cx_02_query_preview", "CX-02 Query: preview of the wording sent to the TFS tool")
dim(s)
s.r(160, 90, 1600, 900, fill=PANEL, stroke=LINE, rx=16)
s.t(200, 145, "What are they looking for?", 28, T1, 700); s.t(1720, 145, "Esc / Ⓑ  Back", 18, T3, 400, "end")
strip(s, "“I want something relaxing.”", FACTS, "◐ CUSTOMER INFO PARTIAL")
for i, n in enumerate(["Sleep", "Pain", "Anxiety / calm", "Energy", "Focus", "Social"]):
    x = 200 + i * 252
    s.r(x, 330, 236, 90, fill=CARD, stroke=LINE, rx=10)
    s.t(x + 118, 384, n, 24, T1, 600, "middle")
s.t(200, 470, "You'll search for", 22, T2, 600)
s.r(200, 486, 1520, 130, fill="#11141a", stroke=ACC, rx=10)
s.t(228, 536, "“something relaxing but I need to stay functional, under $20”", 30, T1, 600)
x = 228
for tok in ["relaxing ✕", "stay functional ✕", "under $20 ✕"]:
    x = s.chip(x, 562, tok, T2, 16)
s.f(1, 190, 486)
s.btn(200, 660, 420, "Similar to Strain Q  · takes a moment", "S / Ⓨ")
s.f(3, 190, 660)
s.btn(1420, 660, 300, "Search", "Enter / Ⓐ", primary=True)
s.f(2, 1410, 660)
s.note("Preview = the exact text the composer (GAME-017) passes to QueryParser; never edited free-hand. Known facts arrive as tokens (on by default); ✕/Del drops one. Liked/disliked strains are not wording.")
s.note("Chips stay the quick path: a tile sets the effect token and the preview shows its canonical wording (chip-only = DEC-017 golden parse). Hidden facts can never appear here (QA-002 gate).")
s.note("Similar shows only when a liked strain is KNOWN (Q6, later repeat memory). Cost tag in words, no seconds or bars. The CUSTOMER INFO tag lives in the strip, never on a card.")
screens.append(s)

# 03 results with workflow entry points + no-sale
s = S("cx_03_results_workflows", "CX-03 Results: Details, Compare marks, Similar, Nothing fits")
dim(s)
s.r(160, 90, 1600, 900, fill=PANEL, stroke=LINE, rx=16)
s.t(200, 145, "Search: “something relaxing but I need to stay functional, under $20”", 24, T1, 700)
strip(s, "“I want something relaxing.”", FACTS, "● CUSTOMER INFO COMPLETE")
for i, (n, x) in enumerate([("Strain A", 200), ("Strain B", 710), ("Strain C", 1220)]):
    w, y = (490 if i < 2 else 500), 320
    s.r(x, y, w, 500, fill=CARD, stroke=ACC if i == 0 else LINE, sw=4 if i == 0 else 2)
    if i == 0: s.r(x, y, 8, 500, fill=ACC, stroke="none", rx=4)
    s.t(x + 28, y + 50, f"{i+1}  {n}", 28, T1, 700)
    s.t(x + 28, y + 82, "‹Brand› · House Fresh · ‹n›% terps", 18, T3)
    s.chip(x + 28, y + 104, "✓ Good fit", OK)
    s.t(x + 28, y + 186, "$xx.xx · an eighth", 34, T1, 700)
    s.t(x + 28, y + 226, "‹g› in jar · ‹why line›", 18, T3)
    s.r(x + 28, y + 300, 30, 30, fill=ACC if i < 2 else "none", stroke=ACC, rx=4)
    s.t(x + 70, y + 324, "Compare mark (C)", 18, T2)
    s.btn(x + 28, y + 400, 150, "Details", "I / Ⓨ")
    s.btn(x + 196, y + 400, w - 224, "Choose", "Enter / Ⓐ", primary=True)
    if i == 0: s.f(1, x + 196, y + 395)
s.btn(200, 880, 380, "Nothing fits right now", "N / click")
s.f(4, 190, 880)
s.btn(840, 880, 420, "Similar to Strain Q · takes a moment", "S")
s.btn(1280, 880, 440, "Compare 2 · takes a moment", "Shift+C / Ⓧ hold")
s.f(2, 1270, 880); s.f(3, 830, 880)
s.note("Cards keep their TFS meaning only (rank order, fit label, price, grams). No completeness, risk, DQ or 'best' marker is ever drawn inside a card (DP §17, DEC-052).")
s.note("Details (was Inspect, I) opens ux_05; Compare: mark 2–3 cards with C, then Compare n (Shift+C) opens ux_06 with the engine's compare. Each is a timed action; tag in words.")
s.note("'Nothing fits right now' sits bottom-left, far from Choose, neutral style (it can be the right call); it opens a confirm card (CX-04). Shown after the first search for this customer.")
screens.append(s)

# 04 no-sale confirm
s = S("cx_04_nofit_confirm", "CX-04 Informed no-sale confirm")
dim(s)
s.r(560, 340, 800, 340, fill=PANEL, stroke=LINE, rx=16)
s.t(600, 400, "Tell them nothing fits right now?", 28, T1, 700)
s.t(600, 450, "“I don't really have anything that fits what", 22, T2)
s.t(600, 482, "you're asking for right now.”", 22, T2)
s.t(600, 530, "They'll leave without buying.", 20, T3)
s.btn(600, 580, 340, "Keep helping", "Esc / Ⓑ", primary=True)
s.btn(980, 580, 340, "Tell them", "Enter on focus / Ⓐ")
s.f(1, 590, 575); s.f(2, 970, 575)
s.note("Default focus = Keep helping, so a stray Enter or a double press of N never ends the service. 'Tell them' needs focus first (Tab / → / click), then Enter.")
s.note("No hint whether the no-sale is informed or avoidable: GAME-019 grades it afterwards (DP §30–31); the result shows only in the report and the debug panel.")
s.note("After 'Tell them' the customer answers with a no-sale line and leaves; toast '↩ No sale · {reason they gave}' in neutral style (4 s).")
screens.append(s)

# 05 debug panel
s = S("cx_05_debug_panel", "CX-05 Dev debug panel (F3, debug builds only)")
world(s)
s.r(120, 70, 1680, 940, fill="#0b0d10ee", stroke=NOTE, rx=8, dash="8 6")
s.t(144, 108, "DEBUG · dev build only · customer #07 · seed 4411", 20, NOTE, 700)
for x, head, col, rows in [
    (144, "TFS VALUES · engine output (what the tool was given and returned)", OK,
     ["Query sent: “something relaxing”", "Parsed: crit relax ≥ ‹n› · neg — · primary relax", "Outcome: Ok", "Candidates (TFS order):",
      "  1 Strain A  ✓ Good fit", "  2 Strain B  ✓ Good fit", "  3 Strain C  ✓ Good fit", "Workflows used: Details ×1, Compare ×0, Similar ×0", "Player selected: Strain A (TFS #1)"]),
    (980, "GAMEPLAY VALUES · simulation + evaluation", WARN,
     ["TRUE: relax · avoid sedation · budget $20 · tier 2", "KNOWN: effect relaxing 💬", "InformationCompleteness 0.30 · InformationRisk high",
      "QuestionTolerance 0.60 · Depth desired 0.50 / actual 0.10", "QueueCost ‹n› · Satisfaction ‹n›", "EVALUATION (uses true intent, DEC-052):",
      "  BestAvailableResolution: ask Q3, then sell", "  Utility best ‹n› / chosen ‹n› · Regret ‹n›", "  DecisionQuality 0.41 (gameplay, not a fit)"])]:
    s.t(x, 160, head, 18, col, 700)
    s.r(x, 172, 776, 4, fill=col, stroke="none", rx=2)
    for i, r in enumerate(rows):
        s.t(x, 214 + i * 40, r, 18, T1 if not r.startswith("EVAL") else NOTE)
s.r(956, 150, 2, 560, fill=LINE, stroke="none", rx=1)
s.t(144, 760, "REJECTION EXPLANATION (DP §114)", 18, NOTE, 700)
for i, r in enumerate(["[TFS]  query used: “something relaxing” · card chosen: Strain A (TFS #1)",
                       "[GAME] not yet learned: stay functional (avoid sedation)",
                       "[GAME] outcome: ASK_LESS_SEDATING · cause: functional need had not been discovered"]):
    s.t(144, 800 + i * 40, r, 18, T1)
s.note("Two fixed columns with their own header colour and rule: TFS left, GAMEPLAY right; a value never moves between them. Evaluation oracle values are a labelled sub-block of GAMEPLAY.")
s.note("Rejection explanation: each line tagged [TFS] or [GAME]. Never 'the game knew the card was wrong'. Panel is non-modal, never takes focus, fixed 100 % text, F3 toggles (exists today).")
s.note("Shows the serving customer, else the last served. Hidden in release builds (Debug.isDebugBuild || editor, as today); none of these values exist in player UI.")
screens.append(s)

# 06 report v2 summary
s = S("cx_06_report_v2", "CX-06 Shift report v2: star gate, categories, revenue apart")
dim(s)
s.r(260, 70, 1400, 940, fill=PANEL, stroke=LINE, rx=16)
s.t(300, 130, "Shift report", 32, T1, 700)
s.t(300, 186, "★★☆  2 stars", 34, T1, 700)
s.t(620, 186, "Overall acceptable · one category weak: FLOW", 22, T2)
for i, (cat, band, ic) in enumerate([("SERVICE", "Strong", "▲"), ("FLOW", "Weak", "▼"), ("OPERATIONS", "Acceptable", "●")]):
    x = 300 + i * 300
    s.r(x, 220, 280, 130, fill=CARD, stroke=LINE)
    s.t(x + 20, 262, cat, 20, T3, 700)
    s.t(x + 20, 316, f"{ic} {band}", 30, T1, 700)
s.r(1240, 220, 380, 130, fill="none", stroke=LINE, rx=10, dash="6 6")
s.t(1260, 262, "Revenue (not part of the stars)", 18, T3, 600)
s.t(1260, 316, "$x,xxx.xx", 34, T1, 700)
rows = [("Customers served", "14"), ("Average wait", "‹m:ss›"), ("Average service time", "‹m:ss›"), ("Average decision quality", "Good"),
        ("Customer satisfaction", "Mostly happy"), ("Walkouts", "2"), ("Stockouts", "1"), ("Waste", "—")]
for i, (k, v) in enumerate(rows):
    y = 410 + i * 46
    s.t(300, y, k, 22, T2); s.t(1000, y, v, 22, T1, 600, "end")
    s.el.append(f'<line x1="300" y1="{y+14}" x2="1000" y2="{y+14}" stroke="{LINE}" stroke-width="1"/>')
for i, tab in enumerate(["Service", "Consultation", "Inventory", "Flow", "Compliance"]):
    s.btn(1080, 400 + i * 84, 540, f"{tab} detail  ›", None, h=64)
s.f(1, 1070, 400)
s.btn(1360, 900, 260, "Close", "Esc / Enter")
s.note("Stars come from the gate (DP §106), never from an average; a severe flag caps them and the reason line says so ('capped: {flag}'). Bands are words + shape icons, never colour only.")
s.note("Revenue sits in its own dashed box outside the category row. Decision quality and satisfaction show as words (§23 bands / satisfaction band), never as numbers or per card.")
s.note("Detail buttons open CX-07. Waste shows '—' until a waste mechanic exists. Rows for systems that are not built yet hide instead of showing 0 (restock rows wait for GAME-012).")
screens.append(s)

# 07 report detail
s = S("cx_07_report_detail", "CX-07 Report detail sections (Service · Consultation · Inventory · Flow)")
dim(s)
s.r(260, 70, 1400, 940, fill=PANEL, stroke=LINE, rx=16)
x = 300
for i, tab in enumerate(["Service", "Consultation", "Inventory", "Flow", "Compliance"]):
    w = len(tab) * 13 + 48
    s.r(x, 100, w, 52, fill=CARD, stroke=ACC if i == 1 else LINE, rx=8, sw=4 if i == 1 else 2)
    s.t(x + w / 2, 134, tab, 20, T1, 600, "middle")
    x += w + 12
s.f(1, 290, 100)
sections = [("SERVICE DETAIL (§109)", ["Ideal sales", "Good compromises", "Acceptable compromises", "Informed no-sales", "Avoidable mismatches", "Avoidable no-sales"]),
            ("CONSULTATION DETAIL (§110)", ["Questions per customer", "Relevant question rate", "Average customer info", "Over-consulted customers", "Under-consulted customers"])]
y = 210
for head, rs in sections:
    s.t(300, y, head, 18, T3, 700); y += 40
    for r in rs:
        s.t(320, y, r, 22, T2); s.t(1000, y, "‹n›", 22, T1, 600, "end"); y += 40
    y += 20
s.t(1080, 210, "INVENTORY DETAIL (§111)", 18, T3, 700)
for i, r in enumerate(["Stockouts", "Lost sales from stock", "(Proactive / reactive / emergency", " restocks: after GAME-012)"]):
    s.t(1100, 250 + i * 40, r, 22 if i < 2 else 18, T2 if i < 2 else T3)
s.t(1080, 450, "FLOW DETAIL (§112)", 18, T3, 700)
for i, r in enumerate(["Peak queue", "Walkouts", "Average queue", "Rush throughput", "Recovery"]):
    s.t(1100, 490 + i * 40, r, 22, T2); s.t(1620, 490 + i * 40, "‹n›", 22, T1, 600, "end")
s.btn(1360, 900, 260, "Back", "Esc / Ⓑ")
s.note("Tabs ← → (LB/RB); Esc returns to the summary. Each tab is one section; this frame stacks four for review only. Compliance = UX_PS1 §6 block unchanged.")
s.note("'Average customer info' = band word (Complete / Partial / Need more), the same words as the counter tag. Relevant question rate as a %, a plain count ratio, not an evaluation value.")
s.note("No row shows utilities, regret or TFS-oracle ranks (DEC-052). Rows sorted as DP §109–112; zero rows show 0.")
screens.append(s)

# 08 M1 text scale 150 %
s = S("cx_08_text150", "CX-08 Text 150 % (REVIEW-W4L M1): register two-column, ID readout")
dim(s)
s.r(96, 70, 1728, 940, fill=PANEL, stroke=LINE, rx=16)
s.t(130, 136, "Register", 40, T1, 700)
for i in range(3):
    y = 170 + i * 128
    s.r(130, y, 1000, 112, fill=CARD, stroke=ACC if i == 0 else LINE, sw=4 if i == 0 else 2)
    s.t(156, y + 46, "Strain With A Very Long Na…", 33, T1, 700)
    s.t(156, y + 90, "‹batch› · House F…", 24, T3)
    s.btn(700, y + 24, 70, "−", None, h=64); s.t(820, y + 66, "14 g", 33, T1, 700, "middle"); s.btn(870, y + 24, 70, "+", None, h=64)
    s.t(1040, y + 66, "$xx.xx", 30, T1, 600, "end"); s.btn(1056, y + 24, 64, "✕", None, h=64)
s.btn(130, 570, 360, "+ Add item", "A", h=72)
s.r(1170, 160, 620, 820, fill="#11141a", stroke="none", rx=10)
s.t(1196, 210, "Flower      21.0 g / 28 g", 30, T2, 600)
s.r(1196, 230, 568, 26, fill=CARD, stroke="none", rx=12); s.r(1196, 230, 426, 26, fill=WARN, stroke="none", rx=12)
s.t(1196, 300, "⚠ Near the 1 oz limit", 28, WARN, 700)
s.t(1196, 400, "Subtotal  $xx.xx", 30, T2); s.t(1196, 450, "Tax 25.1%  $x.xx", 30, T2); s.t(1196, 520, "Total  $xx.xx", 44, T1, 700)
s.btn(1196, 580, 270, "● Cash", None, h=64); s.btn(1490, 580, 270, "○ Card", None, h=64)
s.btn(1196, 860, 568, "Hold to confirm", "Hold Enter / Ⓐ", primary=True, h=72)
s.btn(130, 900, 360, "Cancel", "Esc / Ⓑ", h=72)
s.t(130, 700, "ID panel at ≥125 %: DOB / EXP / TYPE / FORMAT also listed in a readout", 22, T3)
s.t(130, 734, "column beside the card at full scale; they never ellipsize. NAME may.", 22, T3)
s.note("At 125/150 % the register (1000 px wide) switches to two columns inside the full safe area: lines + Add item left; meter, totals, payment, Confirm right. It never scrolls; Confirm is always on screen.")
s.note("Cart rows grow 80 → 96 → 112 px; name and batch line ellipsize (full name on focus tooltip and in Details); stepper, grams, price and ✕ keep fixed columns and never truncate.")
s.note("Meter value and state text never truncate (state wraps to 2 lines). ID card scales up to fit the panel; any decision field that cannot reach the chosen scale on the card goes in the readout.")
screens.append(s)

os.makedirs(OUT, exist_ok=True)
for s in screens:
    p = os.path.join(OUT, s.name + ".svg")
    open(p, "w", encoding="utf-8").write(s.svg())
    assert os.path.getsize(p) < 20_000, p
print(len(screens), "written")
