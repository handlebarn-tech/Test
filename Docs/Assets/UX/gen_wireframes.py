# Generates UX-001 wireframes (static SVG). Usage: python -I gen_wireframes.py <outdir>
import sys, os
from xml.sax.saxutils import escape

OUT = sys.argv[1]
W, H, STRIP = 1920, 1080, 150
# tokens (mirror UX_SLICE.md §6)
BG, WORLD, PANEL, CARD, LINE = "#15181c", "#2b3038", "#1d2127", "#262b33", "#3a414c"
T1, T2, T3 = "#f2f4f7", "#c3c9d2", "#8f98a5"
OK, WARN, BAD, ACC, NOTE = "#56B4E9", "#E69F00", "#D55E00", "#009E73", "#CC79A7"

class S:
    def __init__(s, name, title):
        s.name, s.title, s.el, s.notes = name, title, [], []
    def r(s, x, y, w, h, fill=CARD, stroke=LINE, rx=10, dash=None, sw=2):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def t(s, x, y, txt, size=22, fill=T1, weight=400, anchor="start"):
        s.el.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(txt)}</text>')
    def chip(s, x, y, txt, col, size=18):
        w = int(len(txt) * size * 0.58) + 28
        s.r(x, y, w, size + 16, fill="none", stroke=col, rx=(size + 16) // 2)
        s.t(x + 14, y + size + 3, txt, size, col, 600)
        return x + w + 10
    def btn(s, x, y, w, txt, key, primary=False, h=56):
        s.r(x, y, w, h, fill=ACC if primary else CARD, stroke=ACC if primary else LINE, rx=8)
        s.t(x + w / 2, y + 36, txt, 22, "#0b0d10" if primary else T1, 700, "middle")
        if key: s.t(x + w / 2, y + h + 24, key, 16, T3, 400, "middle")
    def f(s, n, x, y):  # focus-order marker (annotation layer)
        s.el.append(f'<g class="note"><circle cx="{x}" cy="{y}" r="17" fill="{NOTE}"/><text x="{x}" y="{y+7}" font-size="18" font-weight="700" fill="#000" text-anchor="middle">{n}</text></g>')
    def bar(s, x, y, w, lbl, v):
        s.t(x, y + 18, lbl, 18, T2)
        s.r(x + 170, y + 4, w - 170, 16, fill="#11141a", stroke="none", rx=8)
        s.r(x + 170, y + 4, int((w - 170) * v / 100), 16, fill=OK, stroke="none", rx=8)
    def note(s, txt): s.notes.append(txt)
    def svg(s):
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H+STRIP}" viewBox="0 0 {W} {H+STRIP}" font-family="Segoe UI, Arial, sans-serif">',
             f'<title>{escape(s.title)}</title>', f'<rect width="{W}" height="{H}" fill="{BG}"/>']
        o += s.el
        # safe area (title-safe 90%) and frame
        o.append(f'<rect x="96" y="54" width="{W-192}" height="{H-108}" fill="none" stroke="{NOTE}" stroke-width="1.5" stroke-dasharray="10 8" class="note"/>')
        o.append(f'<rect x="0" y="{H}" width="{W}" height="{STRIP}" fill="#ffffff"/>')
        o.append(f'<text x="24" y="{H+36}" font-size="24" font-weight="700" fill="#111">{escape(s.title)}  ·  1920×1080 @100% text  ·  pink = annotation layer (focus order, safe area 96/54 px)</text>')
        for i, n in enumerate(s.notes):
            o.append(f'<text x="24" y="{H+70+i*26}" font-size="19" fill="#222">{escape(n)}</text>')
        o.append('</svg>')
        return "\n".join(o)

def world(s, hint="first-person store view (graybox)"):
    s.r(0, 0, W, H, fill=WORLD, stroke="none", rx=0)
    s.t(W / 2, 470, hint, 28, "#4a525e", 400, "middle")

def dim(s):
    s.el.append(f'<rect width="{W}" height="{H}" fill="#000" opacity="0.55"/>')

def hud(s, prompt=None):
    # top-right cluster: clock, sales, queue
    s.r(1484, 70, 324, 128, fill="#0f1215cc", stroke="none")
    s.t(1508, 112, "◷ 2:47 PM", 26, T1, 600)
    s.t(1508, 150, "$ 412.35 shift sales", 22, T2)
    s.t(1508, 184, "👥 Queue 3", 22, T2)
    s.el.append(f'<circle cx="960" cy="540" r="4" fill="{T1}" opacity="0.8"/>')
    if prompt:
        s.r(810, 880, 300, 56, fill="#0f1215cc", stroke="none")
        s.t(960, 917, prompt, 22, T1, 600, "middle")

def term_frame(s, title):
    dim(s)
    s.r(160, 90, 1600, 900, fill=PANEL, stroke=LINE, rx=16)
    s.t(200, 145, title, 28, T1, 700)
    s.t(1720, 145, "Esc / Ⓑ  Close", 18, T3, 400, "end")
    # persistent request strip (assist: persistent intent summary)
    s.r(200, 170, 1520, 64, fill="#11141a", stroke="none", rx=8)
    s.t(224, 211, "Customer said: “Something to help me sleep, but nothing too pricey.”", 22, T2)
    s.t(1696, 211, "Regular · 2nd visit", 18, T3, 400, "end")

def card(s, x, y, rank, name, role, fit, fitcol, price, stock, why, anx, anxcol, sel=False, w=490, tier="House Fresh"):
    s.r(x, y, w, 470, fill=CARD, stroke=ACC if sel else LINE, sw=4 if sel else 2)
    if rank == 1: s.r(x, y, 8, 470, fill=ACC, stroke="none", rx=4)
    s.t(x + 28, y + 50, str(rank), 28, T3, 700)
    s.t(x + 64, y + 50, name, 28, T1, 700)
    s.t(x + 64, y + 82, f"‹Brand› · {tier} · ‹n›% terps", 18, T3)
    nx = s.chip(x + 28, y + 104, role, T2)
    s.chip(nx, y + 104, fit, fitcol)
    s.t(x + 28, y + 186, price, 36, T1, 700)
    s.t(x + 28, y + 216, "3.5 g, tax incl.", 18, T3)
    s.t(x + w - 28, y + 186, stock, 22, OK, 600, "end")
    s.t(x + w - 28, y + 216, "in jar", 18, T3, 400, "end")
    s.t(x + 28, y + 266, why, 22, T2)
    s.chip(x + 28, y + 290, anx, anxcol)
    s.btn(x + 28, y + 370, 130, "Inspect", "I / Ⓨ")
    s.btn(x + 172, y + 370, 130, "Compare", "C / Ⓧ")
    s.btn(x + 316, y + 370, w - 344, "Choose", "Enter / Ⓐ", primary=True)

screens = []

# 00 flow
s = S("ux_00_flow", "UX-00 Slice flow")
s.r(0, 0, W, H, fill="#ffffff", stroke="none", rx=0)
R1, R2, R3 = 230, 520, 810
nodes = [("HUD / explore", 230, R1), ("Dialogue: request", 600, R1), ("Clarify (≤3 Qs)", 600, R2),
         ("Terminal: query", 980, R1), ("Results (rush view)", 1360, R1), ("Compare", 1700, R1),
         ("Detail", 1700, R2), ("Present → response", 1360, R3), ("POS confirm", 980, R3),
         ("Feedback", 600, R3), ("Customer leaves", 230, R3)]
pos = {n: (x, y) for n, x, y in nodes}
HW, HH = 130, 46
def clip(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    t = min(HW / abs(dx) if dx else 9e9, HH / abs(dy) if dy else 9e9)
    return x1 + dx * t, y1 + dy * t
def arrow(a, b, lbl="", off=(0, 0), lo=(0, -12)):
    (x1, y1), (x2, y2) = pos[a], pos[b]
    x1, y1, x2, y2 = x1 + off[0], y1 + off[1], x2 + off[0], y2 + off[1]
    sx, sy = clip(x1, y1, x2, y2); ex, ey = clip(x2, y2, x1, y1)
    s.el.append(f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="#556" stroke-width="3" marker-end="url(#ah)"/>')
    if lbl: s.t((sx + ex) / 2 + lo[0], (sy + ey) / 2 + lo[1], lbl, 18, "#a03", 600, "middle")
s.el.insert(0, '<defs><marker id="ah" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#556"/></marker></defs>')
arrow("HUD / explore", "Dialogue: request", "Interact NPC")
arrow("Dialogue: request", "Clarify (≤3 Qs)", "Ask", off=(-20, 0), lo=(-40, 0))
arrow("Clarify (≤3 Qs)", "Dialogue: request", "Reply", off=(20, 0), lo=(48, 0))
arrow("Dialogue: request", "Terminal: query", "Look it up")
arrow("Terminal: query", "Results (rush view)", "Search")
arrow("Results (rush view)", "Compare", "Compare")
arrow("Results (rush view)", "Detail", "Inspect", lo=(-40, 10))
arrow("Results (rush view)", "Present → response", "Choose", lo=(-50, 0))
arrow("Present → response", "POS confirm", "ACCEPT", off=(0, -14), lo=(0, -12))
arrow("POS confirm", "Present → response", "Cancel (release)", off=(0, 14), lo=(0, 30))
arrow("POS confirm", "Feedback", "Confirm")
arrow("Feedback", "Customer leaves")
arrow("Present → response", "Terminal: query", "ASK_* (refine)", lo=(-90, 0))
x1, y1 = pos["Present → response"]; x2, y2 = pos["Customer leaves"]
s.el.append(f'<path d="M{x1},{y1+HH} Q{(x1+x2)/2},{y1+220} {x2},{y2+HH+4}" fill="none" stroke="#556" stroke-width="3" marker-end="url(#ah)"/>')
s.t((x1 + x2) / 2, y1 + 150, "REJECT / LEAVE (also on patience out, from any step)", 18, "#a03", 600, "middle")
for n, x, y in nodes:
    s.r(x - HW, y - HH, 2 * HW, 2 * HH, fill="#eef2f6", stroke="#334", rx=14)
    s.t(x, y + 8, n, 22, "#111", 700, "middle")
s.t(960, 120, "Back (Esc / B) always returns one step. Closing the terminal returns to the dialogue; the customer keeps waiting.", 20, "#333", 400, "middle")
s.t(1700, 640, "Choose from Detail/Compare → Present", 18, "#a03", 600, "middle")
s.note("Every node maps to one wireframe ux_01..ux_09. Patience keeps draining in every node except Feedback (spec §27).")
screens.append(s)

# 01 HUD
s = S("ux_01_hud", "UX-01 HUD (explore / idle)")
world(s); hud(s, "E / Ⓐ  Talk")
s.f(1, 1470, 90)
s.note("Top-right cluster only: shift clock (game time), shift sales $, queue count. No patience bars (spec §27): patience is shown by NPC body language.")
s.note("Interaction prompt appears only when a target is in reach (spec §62). Crosshair dot 8 px. HUD has no focusable elements; it hides while the terminal or POS is open.")
s.note("Assist 'Patience hints' (off by default) adds a word under each queued NPC: Relaxed / Waiting / Impatient, with icon. Font: clock 26, other 22.")
screens.append(s)

# 02 dialogue
s = S("ux_02_dialogue", "UX-02 Dialogue: request + clarifying questions")
world(s, "customer at counter"); hud(s)
s.r(360, 760, 1200, 110, fill="#0f1215e6", stroke="none")
s.t(392, 800, "CUSTOMER", 18, WARN, 700)
s.t(392, 842, "“Something to help me sleep, but nothing too pricey.”", 28, T1)
opts = ["Look it up on the terminal", "“What kind of experience are you looking for?”",
        "“Any budget you want to stay under?”", "“Anything you want to avoid?”", "“Did you like anything last time?”"]
for i, o in enumerate(opts):
    y = 330 + i * 76
    s.r(1180, y, 600, 62, fill=ACC if i == 0 else "#0f1215e6", stroke=ACC if i == 0 else LINE, rx=8)
    s.t(1204, y + 40, f"{i+1}  {o}", 22, "#0b0d10" if i == 0 else T1, 600 if i == 0 else 400)
    s.f(i + 1, 1160, y + 31)
s.t(1780, 315, "Questions left: 2 of 3", 18, T3, 400, "end")
s.note("Subtitles: 28 px, max 2 lines, 1200 px box, speaker label 18 px. Options: number keys 1-5, D-pad ↑↓ + Ⓐ, or mouse.")
s.note("Asked questions grey out. Each costs game time (DES-001 sets cost). Option 1 opens the terminal; the request line stays pinned there.")
s.note("Customer reply to a question appears in the subtitle box and is appended to the request strip in the terminal.")
screens.append(s)

# 03 query
s = S("ux_03_terminal_query", "UX-03 Terminal: query")
world(s); term_frame(s, "Recommend")
s.t(200, 290, "What are they after?", 22, T2, 600)
intents = [("Sleep", True), ("Pain", False), ("Anxiety / calm", False), ("Energy", False), ("Focus", False), ("Social", False)]
for i, (n, on) in enumerate(intents):
    x = 200 + i * 252
    s.r(x, 310, 236, 80, fill=ACC if on else CARD, stroke=ACC if on else LINE, rx=10)
    s.t(x + 118, 360, ("✓ " if on else "") + n, 24, "#0b0d10" if on else T1, 700, "middle")
s.f(1, 190, 300)
s.t(200, 450, "Constraints", 22, T2, 600)
s.r(200, 470, 470, 80); s.t(224, 518, "Budget  ≤ $ 20 per 3.5 g", 22, T1); s.f(2, 190, 465)
s.r(690, 470, 470, 80); s.t(714, 518, "Stay functional (cap sedation)", 22, T3); s.f(3, 680, 465)
s.r(1180, 470, 540, 80, dash="8 6"); s.t(1204, 518, "Avoid terpene · First-time  (next wave)", 22, T3)
s.r(200, 600, 1520, 70, fill="#11141a", stroke="none", rx=8)
s.t(224, 645, "Free text search: reserved for the full parser (next wave). Hidden in slice.", 20, T3)
s.btn(1440, 880, 280, "Search", "Enter / Ⓐ", primary=True); s.f(4, 1430, 875)
s.note("Intent tiles = the 6 slice intent families; each maps to one INTENTS key (DES-001 owns the mapping). Multi-select merges per contract §2.9 (crit=max, neg=min).")
s.note("Player picks intents from what they heard: interpretation is the skill (spec §14). Assist 'Auto-fill intent' pre-selects the NPC's emitted key.")
s.note("Focus: tiles (←→) → Budget (−/+ steppers, $5 steps) → Stay functional toggle → Search. Tiles 236×80, text 24.")
screens.append(s)

# 04 results
s = S("ux_04_terminal_results", "UX-04 Terminal: results (rush view, default)")
world(s); term_frame(s, "Recommend · Sleep · ≤ $20")
card(s, 200, 280, 1, "Strain A", "Best match", "✓ Good fit", OK, "$13.10", "214 g", "Myrcene-forward, heavy body", "✓ Low anxiety", OK, sel=True)
card(s, 715, 280, 2, "Strain B", "Most functional", "✓ Good fit", OK, "$17.50", "88 g", "Lighter, linalool calm", "⚠ Moderate anxiety", WARN, tier="TFS Premium")
card(s, 1230, 280, 3, "Strain C", "Lowest anxiety", "✓ Good fit", OK, "$8.75", "31 g", "BCP + humulene, body", "✓ Low anxiety", OK, tier="House Smalls")
for i, x in enumerate((200, 715, 1230)): s.f(i + 1, x - 4, 276)
s.r(200, 790, 1520, 64, fill="#11141a", stroke=WARN, rx=8, dash="8 6")
s.t(224, 831, "⚠ Variant: “No exact match. Closest available.” banner + all cards ‘◐ Possible fit’ (relaxed fallback). None: “Nothing matched.” + Back.", 20, WARN)
s.btn(200, 880, 300, "More options", "M / RS"); s.f(4, 190, 875)
s.btn(520, 880, 300, "Edit search", "Backspace / LS"); s.f(5, 510, 875)
s.note("3 cards max (resultCount 3). Card face = Floor Mode: name, sub-line, role tag, fit label, price, jar grams, one 'why' line, anxiety chip. No bars, no %, no scores.")
s.note("←→ / LB-RB moves card focus; I inspect, C toggles compare (2-3), Enter chooses. Card 490×470; name 28, price 36, body 22, chips 18.")
s.note("Prices shown are Tue day-deal post-tax 3.5 g from TIER_DEFAULTS/DEFAULT_DAY_DEALS (house 13.10, premium 17.50, smalls 8.75). Names/grams/text are placeholders.")
screens.append(s)

# 05 detail
s = S("ux_05_terminal_detail", "UX-05 Terminal: detail (inspect)")
world(s); term_frame(s, "Strain A · detail")
s.r(200, 260, 740, 600)
s.t(228, 304, "Effect fit", 24, T1, 700); s.chip(400, 278, "INFERRED", T3, 16)
for i, (l, v) in enumerate([("Sedation", 82), ("Uplift", 20), ("Anxiety relief", 99), ("Pain", 99), ("Focus", 12)]):
    s.bar(228, 330 + i * 44, 680, l, v)
s.t(228, 590, "Type: Myrcene-heavy (cluster 1)", 22, T2); s.chip(620, 566, "HEURISTIC", T3, 16)
s.t(228, 636, "Anxiety risk: low", 22, OK); s.chip(460, 612, "HEURISTIC", T3, 16)
s.t(228, 690, "‹Card script line from buildScript›", 22, T2)
s.t(228, 760, "Terpene–effect links are early research. THC, dose,", 18, T3)
s.t(228, 786, "tolerance and the person matter more. Start the", 18, T3)
s.t(228, 812, "conversation; don't promise an effect.", 18, T3)
s.r(960, 260, 760, 600)
s.t(988, 304, "Batch (in stock)", 24, T1, 700); s.chip(1210, 278, "OBSERVED", OK, 16)
rows = [("Batch", "‹batch code›"), ("Tested", "‹COA date› · 3 wk old"), ("Tier / brand", "House Fresh · ‹Brand›"), ("Total terpenes", "2.1 %"), ("In jar", "214 g")]
for i, (k, v) in enumerate(rows):
    s.t(988, 352 + i * 40, k, 20, T3); s.t(1220, 352 + i * 40, v, 20, T1)
s.t(988, 580, "Top terpenes (avg of in-stock batches)", 20, T2, 600)
for i, (k, v) in enumerate([("β-Myrcene", "0.92 %"), ("β-Caryophyllene", "0.41 %"), ("Linalool", "0.18 %")]):
    s.t(988, 620 + i * 36, k, 20, T1); s.t(1400, 620 + i * 36, v, 20, T2, 400, "end")
s.t(988, 760, "Prices (tax incl.)  3.5 g $13.10 · 7 g $26.25 · 14 g $52.50 · 28 g $71.25", 18, T2)
s.btn(200, 900, 260, "Back", "Esc / Ⓑ"); s.f(2, 190, 895)
s.btn(1440, 900, 280, "Choose", "Enter / Ⓐ", primary=True); s.f(1, 1430, 895)
s.note("Detail = the tool's expand panel, opt-in only (spec §13 detailed view). Every block carries its evidence tag (MASTER_PLAN §4.3): OBSERVED / INFERRED / HEURISTIC.")
s.note("Bars show display_d (2-99) for 5 domains; antimicrobial is never shown. Saturation at 99 kept for parity (GAP-208). Values here are illustrative.")
s.note("Focus starts on Choose; Back returns to results with the same card focused. Tue prices from contract §12 (house tier).")
screens.append(s)

# 06 compare
s = S("ux_06_terminal_compare", "UX-06 Terminal: compare (2-3)")
world(s); term_frame(s, "Compare")
s.r(200, 260, 1520, 80, fill="#11141a", stroke=ACC, rx=8)
s.t(228, 310, "Key difference: Strain A is notably heavier (Sedation 82 vs 55).", 26, T1, 600)
cols = [("Strain A", "$13.10", "Myrcene-heavy", "✓ Low", OK, "3 wk"), ("Strain B", "$17.50", "Linalool calm", "⚠ Moderate", WARN, "6 wk")]
s.t(228, 400, "", 20)
labels = ["Price 3.5 g", "Type", "Anxiety risk", "Sedation", "Batch age"]
for i, l in enumerate(labels): s.t(228, 440 + i * 70, l, 22, T3)
for c, (n, p, ty, ax, col, age) in enumerate(cols):
    x = 640 + c * 520
    s.r(x - 20, 360, 480, 420)
    s.t(x, 405, n, 28, T1, 700)
    for i, v in enumerate([p, ty, ax, ("82" if c == 0 else "55"), age]):
        s.t(x, 440 + i * 70, v, 24, col if i == 2 else T1, 600 if i == 0 else 400)
    s.btn(x, 800, 200, "Choose", "Enter / Ⓐ", primary=(c == 0)); s.f(c + 1, x - 10, 795)
s.btn(200, 900, 260, "Back", "Esc / Ⓑ"); s.f(3, 190, 895)
s.note("Only decision-relevant rows (spec §19): price, type (cluster), anxiety, the key-difference domain, batch age. No raw chemistry; Inspect from a column opens Detail.")
s.note("Key difference = largest display gap among the 5 shown domains; 'notably' when gap ≥10 (contract §11). Third column appears when 3 are selected.")
screens.append(s)

# 07 present
s = S("ux_07_present", "UX-07 Present choice → customer response")
world(s, "customer at counter, jar of Strain A on counter"); hud(s)
s.r(360, 760, 1200, 110, fill="#0f1215e6", stroke="none")
s.t(392, 800, "CUSTOMER", 18, WARN, 700)
s.t(392, 842, "“Hmm, is there anything a bit cheaper?”", 28, T1)
s.r(96, 70, 520, 90, fill="#0f1215e6", stroke="none")
s.t(120, 108, "Presented: Strain A · 3.5 g · $13.10", 22, T1, 600)
s.t(120, 142, "Response: ASK_CHEAPER", 18, T3)
opts = ["Ring it up anyway", "Show a cheaper option (terminal)", "“This one's the best fit for sleep.”", "Let them go"]
for i, o in enumerate(opts):
    y = 400 + i * 76
    s.r(1180, y, 600, 62, fill="#0f1215e6", stroke=LINE, rx=8)
    s.t(1204, y + 40, f"{i+1}  {o}", 22, T1)
    s.f(i + 1, 1160, y + 31)
s.note("Choosing on the terminal closes it and presents the batch (spec §17 states). ACCEPT skips this menu and opens POS.")
s.note("Each response state has its own option set; 'terminal' options reopen Results with a refine applied (DES-001 maps ASK_* to crit/neg/maxPrice edits).")
s.note("Pinned 'Presented' card top-left so the player keeps context. Same dialogue layout as UX-02.")
screens.append(s)

# 08 POS
s = S("ux_08_pos_confirm", "UX-08 POS confirm")
world(s); dim(s)
s.r(460, 120, 1000, 840, fill=PANEL, stroke=LINE, rx=16)
s.t(500, 180, "Register", 28, T1, 700)
s.t(500, 240, "Strain A", 28, T1, 700); s.t(500, 274, "‹batch code› · House Fresh", 18, T3)
s.t(500, 340, "Weight", 22, T2, 600)
for i, g in enumerate(["3.5 g", "7 g", "14 g", "28 g"]):
    x = 500 + i * 230
    s.r(x, 360, 210, 70, fill=ACC if i == 0 else CARD, stroke=ACC if i == 0 else LINE)
    s.t(x + 105, 405, g, 24, "#0b0d10" if i == 0 else T1, 700, "middle")
s.f(1, 490, 355)
lines = [("Price (House Fresh MSRP)", "$14.00"), ("Day deal: Tuesday House", "− $3.50"), ("Subtotal", "$10.50"), ("Tax 25.1%", "$2.60")]
for i, (k, v) in enumerate(lines):
    s.t(500, 500 + i * 44, k, 22, T2); s.t(1420, 500 + i * 44, v, 22, T1, 400, "end")
s.el.append(f'<line x1="500" y1="680" x2="1420" y2="680" stroke="{LINE}" stroke-width="2"/>')
s.t(500, 728, "Total", 30, T1, 700); s.t(1420, 728, "$13.10", 36, T1, 700, "end")
s.t(500, 790, "Payment", 22, T2, 600)
for i, p in enumerate(["Cash", "Card"]):
    x = 640 + i * 200
    s.r(x, 760, 180, 50, fill=CARD, stroke=ACC if i == 0 else LINE)
    s.t(x + 90, 794, ("● " if i == 0 else "○ ") + p, 22, T1, 400, "middle")
s.f(2, 630, 755)
s.btn(500, 850, 300, "Cancel", "Esc / Ⓑ"); s.f(4, 490, 845)
s.btn(1120, 850, 300, "Hold to confirm", "Hold Enter / Ⓐ 0.6 s", primary=True); s.f(3, 1110, 845)
s.r(1120, 850, 120, 6, fill="#0b0d10", stroke="none", rx=3)
s.note("Prices: contract §12, Tuesday deal, applyTax floor to $0.05 (10.50 → 13.10; tax line = total − subtotal). Weight tiles disabled when jar grams < weight.")
s.note("Confirm is hold-to-confirm by default (prevents double sale); setting 'Hold actions → Press' makes it a single press. Cancel releases the reservation (spec §67, §88).")
s.note("Payment is abstract (spec §24-25). Focus: weight → payment → Confirm → Cancel. Panel 1000×840, total 36.")
screens.append(s)

# 09 feedback
s = S("ux_09_feedback", "UX-09 Feedback after sale")
world(s, "customer turning to leave"); hud(s)
s.r(96, 70, 560, 150, fill="#0f1215e6", stroke=OK, rx=10)
s.t(124, 112, "✓ Sale · Strain A · 3.5 g", 24, T1, 700)
s.t(124, 148, "+ $13.10   ·   jar 214 g → 210.5 g", 22, T2)
s.t(124, 190, "Customer: “Thanks, I'll let you know.”", 20, T3)
s.r(1484, 210, 324, 40, fill="none", stroke=OK, rx=8, dash="6 4")
s.t(1500, 238, "+$13.10 (no count-up if reduced motion)", 16, OK)
s.note("Toast top-left, 4 s, non-blocking, never steals focus. Sale line is OBSERVED (transaction ledger); the customer line is flavour, not a score.")
s.note("No % satisfaction (spec §51). Outcome words, if any, use Strong/Good/Possible-style language set by DES-001. Shift sales on the HUD ticks once.")
s.note("Toast on reject/leave uses ⚠ + WARN orange and the customer's line. All toasts also logged in the shift summary (not in slice UI).")
screens.append(s)

os.makedirs(OUT, exist_ok=True)
for s in screens:
    p = os.path.join(OUT, s.name + ".svg")
    open(p, "w", encoding="utf-8").write(s.svg())
    assert os.path.getsize(p) < 500_000, p
print(len(screens), "written")
