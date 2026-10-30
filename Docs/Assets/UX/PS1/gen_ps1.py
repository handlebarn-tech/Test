# Generates UX-002 (PS1) wireframes (static SVG). Usage: python -I gen_ps1.py <outdir>
# Same drawing kit and tokens as ../gen_wireframes.py (UX-001), copied so that script stays untouched.
import sys, os
from xml.sax.saxutils import escape

OUT = sys.argv[1]
W, H, STRIP = 1920, 1080, 150
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
    def btn(s, x, y, w, txt, key, primary=False, h=56, off=False):
        s.r(x, y, w, h, fill=ACC if primary and not off else CARD, stroke=ACC if primary and not off else LINE, rx=8)
        s.t(x + w / 2, y + 36, txt, 22, T3 if off else ("#0b0d10" if primary else T1), 700, "middle")
        if key: s.t(x + w / 2, y + h + 24, key, 16, T3, 400, "middle")
    def f(s, n, x, y):  # focus-order marker (annotation layer)
        s.el.append(f'<g class="note"><circle cx="{x}" cy="{y}" r="17" fill="{NOTE}"/><text x="{x}" y="{y+7}" font-size="18" font-weight="700" fill="#000" text-anchor="middle">{n}</text></g>')
    def note(s, txt): s.notes.append(txt)
    def svg(s):
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H+STRIP}" viewBox="0 0 {W} {H+STRIP}" font-family="Segoe UI, Arial, sans-serif">',
             f'<title>{escape(s.title)}</title>', f'<rect width="{W}" height="{H}" fill="{BG}"/>']
        o += s.el
        o.append(f'<rect x="96" y="54" width="{W-192}" height="{H-108}" fill="none" stroke="{NOTE}" stroke-width="1.5" stroke-dasharray="10 8" class="note"/>')
        o.append(f'<rect x="0" y="{H}" width="{W}" height="{STRIP}" fill="#ffffff"/>')
        o.append(f'<text x="24" y="{H+36}" font-size="24" font-weight="700" fill="#111">{escape(s.title)}  ·  1920×1080 @100% text  ·  pink = annotation (focus order, safe area)</text>')
        for i, n in enumerate(s.notes):
            o.append(f'<text x="24" y="{H+70+i*26}" font-size="19" fill="#222">{escape(n)}</text>')
        o.append('</svg>')
        return "\n".join(o)

def world(s, hint="first-person store view (graybox)"):
    s.r(0, 0, W, H, fill=WORLD, stroke="none", rx=0)
    s.t(W / 2, 470, hint, 28, "#4a525e", 400, "middle")

def dim(s): s.el.append(f'<rect width="{W}" height="{H}" fill="#000" opacity="0.55"/>')

def hud(s, queue="👥 Queue 3"):
    s.r(1484, 70, 324, 128, fill="#0f1215cc", stroke="none")
    s.t(1508, 112, "◷ 2:47 PM", 26, T1, 600)
    s.t(1508, 150, "$ 412.35 shift sales", 22, T2)
    s.t(1508, 184, queue, 22, T2)

def meter(s, x, y, w, label, val, cap, col, state):
    s.t(x, y + 22, label, 22, T2, 600)
    s.t(x + w, y + 22, f"{val} / {cap}", 22, T1, 700, "end")
    s.r(x, y + 38, w, 20, fill="#11141a", stroke="none", rx=10)
    s.r(x, y + 38, int(w * min(1.0, float(val.split()[0]) / float(cap.split()[0]))), 20, fill=col, stroke="none", rx=10)
    s.r(x + int(w * 0.75), y + 34, 2, 28, fill=T3, stroke="none", rx=1)  # amber mark
    s.t(x, y + 90, state, 20, col, 700)

def pos_frame(s, badge, badgecol, lines, sub, tax_lbl, total, focus=True):
    """POS cart panel 1000×900: badge, up to 3 lines, + Add item, meter slot (y 560), totals, buttons."""
    dim(s)
    s.r(460, 90, 1000, 900, fill=PANEL, stroke=LINE, rx=16)
    s.t(500, 148, "Register", 28, T1, 700)
    s.chip(1100, 120, badge, badgecol)
    for i, (name, g, price, sel) in enumerate(lines):
        y = 180 + i * 96
        s.r(500, y, 920, 80, fill=CARD, stroke=ACC if sel else LINE, sw=4 if sel else 2)
        s.t(524, y + 34, name, 24, T1, 700)
        s.t(524, y + 62, "‹batch› · House Fresh", 16, T3)
        s.btn(860, y + 12, 56, "−", None, h=56); s.t(978, y + 50, g, 24, T1, 700, "middle"); s.btn(1040, y + 12, 56, "+", None, h=56)
        s.t(1290, y + 50, price, 24, T1, 600, "end")
        s.btn(1316, y + 12, 88, "✕", None, h=56)
        if focus and i == 0: s.f(1, 490, y + 6)
    ya = 180 + len(lines) * 96
    s.btn(500, ya, 280, "+ Add item" if len(lines) < 3 else "Cart full (3)", "A", off=len(lines) >= 3)
    if focus: s.f(2, 490, ya)
    s.t(1000, 708, "Subtotal", 22, T2); s.t(1420, 708, sub, 22, T1, 400, "end")
    s.t(1000, 748, tax_lbl, 22, T2); s.t(1420, 748, "$x.xx", 22, T1, 400, "end")
    s.el.append(f'<line x1="1000" y1="770" x2="1420" y2="770" stroke="{LINE}" stroke-width="2"/>')
    s.t(1000, 812, "Total", 30, T1, 700); s.t(1420, 812, total, 36, T1, 700, "end")

def pos_buttons(s, confirm_off=False, focus=True):
    s.btn(500, 880, 300, "Cancel", "Esc / Ⓑ")
    s.btn(1120, 880, 300, "Hold to confirm", "Hold Enter / Ⓐ 0.6 s", primary=True, off=confirm_off)
    if focus: s.f(4, 490, 875); s.f(3, 1110, 875)

screens = []

# 01 results with a cart in progress
s = S("ps1_01_results_cart", "PS1-01 Results with a cart in progress (add another item)")
dim(s)
s.r(160, 90, 1600, 900, fill=PANEL, stroke=LINE, rx=16)
s.t(200, 145, "Search: Energy", 28, T1, 700); s.t(1720, 145, "Esc / Ⓑ  Back", 18, T3, 400, "end")
s.r(200, 170, 1520, 64, fill="#11141a", stroke="none", rx=8)
s.t(224, 211, "“A half of something for sleep  ✓   and an eighth of something for energy.”", 22, T2)
s.r(1380, 250, 340, 90, fill="#11141a", stroke=ACC, rx=10)
s.t(1400, 284, "🛒 Cart 1 / 3 · 14 g", 22, T1, 700)
s.t(1400, 322, "R  Go to register", 18, T3)
s.f(5, 1370, 250)
for i, (n, x) in enumerate([("Strain D", 200), ("Strain E", 710), ("Strain F", 1220)]):
    w = 490 if i < 2 else 500
    y = 360
    s.r(x, y, w, 470, fill=CARD, stroke=ACC if i == 0 else LINE, sw=4 if i == 0 else 2)
    if i == 0: s.r(x, y, 8, 470, fill=ACC, stroke="none", rx=4)
    s.t(x + 28, y + 50, f"{i+1}  {n}", 28, T1, 700)
    s.t(x + 28, y + 82, "‹Brand› · House Fresh · ‹n›% terps", 18, T3)
    s.chip(x + 28, y + 104, "✓ Good fit", OK)
    s.t(x + 28, y + 186, "$xx.xx · an eighth", 34, T1, 700)
    s.t(x + 28, y + 226, "‹g› in jar", 18, T3)
    s.btn(x + 28, y + 370, 140, "Inspect", "I / Ⓨ")
    s.btn(x + 186, y + 370, w - 214, "Add to cart", "Enter / Ⓐ", primary=True)
    if i == 0: s.f(1, x + 186, y + 365)
s.note("Cart open (≥1 line): the card's Choose becomes 'Add to cart' (same key). It presents the item; on ACCEPT the line is added and the register opens.")
s.note("Request strip ticks each clause already in the cart (✓). Cart chip top-right: lines / 3 and summed grams; R or click → register without adding.")
s.note("With 3 lines in the cart, 'Add to cart' is disabled with 'Cart full (3)'. Prices are placeholders; GAME-006 computes them (DEC-035, round once on the total).")
screens.append(s)

# 02 POS cart, meter amber
s = S("ps1_02_pos_cart", "PS1-02 Register: cart lines + purchase-limit meter (amber)")
world(s)
pos_frame(s, "✓ 21+ ID verified", OK,
          [("Strain A", "14 g", "$xx.xx", True), ("Strain D", "3.5 g", "$xx.xx", False), ("Strain B", "3.5 g", "$xx.xx", False)],
          "$xx.xx", "Tax 25.1%", "$xx.xx")
meter(s, 500, 560, 440, "Flower", "21.0 g", "28 g", WARN, "⚠ Near the 1 oz limit")
s.t(500, 690, "Concentrate row: hidden until PS3", 16, T3)
s.t(500, 790, "Payment", 22, T2, 600)
s.btn(620, 760, 150, "● Cash", None, h=50); s.btn(780, 760, 150, "○ Card", None, h=50)
pos_buttons(s)
s.note("Line: name · batch · − weight + (steps through 3.5/7/14/28, disabled where jar grams < weight) · line price (pre-tax) · ✕ remove. Totals sum the lines; tax once on the cart.")
s.note("Meter = cart flower g / 28 g. Neutral under 75 % (mark), ⚠ amber 75–100 %, ✗ red over. Status = icon + word, never colour only. Concentrate row appears in PS3 (5 g).")
s.note("Focus: line 1 (↑↓ lines, ← → or −/+ weight, Del remove) → + Add item → Confirm → Cancel. '+ Add item' returns to Query with the request strip.")
screens.append(s)

# 03 POS over the limit
s = S("ps1_03_pos_over", "PS1-03 Register: over the limit (trim decision)")
world(s)
pos_frame(s, "✓ 21+ ID verified", OK,
          [("Strain A", "28 g", "$xx.xx", True), ("Strain C", "3.5 g", "$xx.xx", False)],
          "$xx.xx", "Tax 25.1%", "$xx.xx")
meter(s, 500, 560, 440, "Flower", "31.5 g", "28 g", BAD, "✗ Over the 1 oz limit")
s.r(500, 760, 440, 50, fill="none", stroke=BAD, rx=8)
s.t(520, 792, "Remove a line or step a weight down", 20, T2)
pos_buttons(s, confirm_off=True)
s.r(96, 70, 560, 110, fill="#0f1215e6", stroke=BAD, rx=10)
s.t(124, 112, "✗ Over the 1 oz limit", 24, T1, 700)
s.t(124, 150, "Customer: “An ounce of A and an eighth of C.”", 20, T3)
s.note("Over cap: meter red, Confirm disabled (no over-limit sale path, RES-001 O4), the existing 'Over the 1 oz limit' toast fires once when the cart first goes over.")
s.note("The hint never names which line to drop: choosing what to keep is the decision (SPEC_COMP002 §2). Trimming the customer's primary item costs fit (GAME-007).")
s.note("Cancel with an over-limit cart = no-sale (customer leaves). Payment row is hidden in these frames only to keep the hint visible; it stays in the build.")
screens.append(s)

# 04 cover check-in prompt + walk to the ID stand
s = S("ps1_04_cover_prompt", "PS1-04 Rush: 'cover the ID stand?' prompt")
world(s, "counter view; ID stand is left inside the entrance (DEC-048)")
hud(s, "👥 Queue 4 · ⚡ Rush")
s.r(560, 300, 800, 300, fill=PANEL, stroke=WARN, rx=16)
s.t(600, 360, "⚠ The ID stand is backed up", 28, T1, 700)
s.t(600, 404, "Cover it for the next 3 arrivals?", 22, T2)
s.t(600, 440, "Your counter line keeps waiting while you're away.", 20, T3)
s.btn(600, 500, 300, "Cover the stand", "Y / Ⓐ", primary=True); s.f(1, 590, 495)
s.btn(1020, 500, 300, "Stay at counter", "N / Ⓑ"); s.f(2, 1010, 495)
s.note("Shown once on rush start at coverCheckInChance; does not pause the sim; auto-declines after 8 s [GDD]. Declining = no ID events (SPEC_COMP002 §3).")
s.note("Accept → a world marker + HUD line '◆ ID stand · 0/3' guide the player to the stand (anchor near the entry door, left; TEMP fallback per GAME-008).")
s.note("Wording assumes the player covers the guard's stand; whether a budtender ever does this is a question for Nolan (handoff Q1).")
screens.append(s)

# 05 ID card panel
s = S("ps1_05_id_panel", "PS1-05 ID stand: card inspect, Admit / Refuse; counter queue stays visible")
world(s, "entry vestibule, arrival at the stand")
s.el.append(f'<rect width="1340" height="{H}" fill="#000" opacity="0.55"/>')
s.r(120, 90, 1200, 900, fill=PANEL, stroke=LINE, rx=16)
s.t(160, 148, "ID stand · arrival 1 of 3", 28, T1, 700)
s.t(1280, 148, "Today: Tue 10/27/2026", 24, T1, 700, "end")
# horizontal card 856×540 scaled 0.9
s.r(160, 190, 770, 486, fill="#e9edf2", stroke="#9aa3ae", rx=24)
s.r(160, 190, 770, 60, fill="#2f5d8a", stroke="none", rx=24)
s.t(190, 232, "ARIZONA · DRIVER LICENSE", 24, "#ffffff", 700)
s.r(190, 280, 220, 280, fill="#c7ccd3", stroke="#9aa3ae", rx=8)
s.t(300, 430, "photo", 20, "#5b636e", 400, "middle")
for i, (k, v) in enumerate([("NAME", "‹generated›"), ("DOB", "11/14/2005"), ("EXP", "11/14/2030"), ("TYPE", "Driver license"), ("FORMAT", "Horizontal")]):
    s.t(440, 300 + i * 56, k, 16, "#5b636e", 700); s.t(440, 324 + i * 56, v, 24, "#111", 700)
s.r(960, 190, 320, 486, fill=CARD, stroke=LINE, dash="8 6")
s.t(1120, 400, "Vertical cards", 20, T3, 400, "middle"); s.t(1120, 428, "render portrait", 20, T3, 400, "middle"); s.t(1120, 456, "(540×856) here", 20, T3, 400, "middle")
s.t(160, 720, "Assist 'ID age helper' (off): shows 'Age 20 · expires in 4 y'.", 18, T3)
s.f(1, 150, 185)  # focus starts on the card so a stray Enter cannot admit
s.btn(160, 860, 360, "Refuse", "R / Ⓧ"); s.f(3, 150, 855)
s.btn(900, 860, 380, "Admit", "A / Ⓐ", primary=True); s.f(2, 890, 855)
# counter queue strip (forced on while covering)
s.r(1380, 90, 440, 420, fill="#0f1215e6", stroke=LINE, rx=12)
s.t(1404, 132, "Counter line (4)", 22, T1, 700)
for i, (w, c) in enumerate([("Relaxed", OK), ("Waiting", WARN), ("Waiting", WARN), ("Impatient", BAD)]):
    s.t(1404, 180 + i * 48, f"{i+1}.", 22, T3); s.chip(1440, 156 + i * 48, ("● " if c == OK else "◐ " if c == WARN else "▲ ") + w, c)
s.t(1404, 380, "◆ Stand: 2 waiting", 22, T2)
s.t(1404, 420, "◷ 2:52 PM · $ 412.35", 20, T3)
s.r(1380, 540, 440, 120, fill="#0f1215e6", stroke=OK, rx=10)
s.t(1404, 584, "✓ Refused: under 21", 22, T1, 700)
s.t(1404, 620, "result toast (4 s)", 18, T3)
s.note("Card shows photo, DOB, expiry, state, type, format (horizontal/vertical); the in-game date sits top-right of the panel. No verdict is shown: reading it is the decision.")
s.note("While covering, the HUD becomes the 'Counter line' strip: one patience word+icon per queued customer (forced on, not the assist) + arrivals waiting at the stand.")
s.note("Esc closes the panel; walking away leaves the remaining arrivals at the stand. Example: DOB 11/14/2005 on 10/27/2026 = age 20 → Refuse is correct.")
screens.append(s)

# 06 medical POS
s = S("ps1_06_pos_medical", "PS1-06 Register: medical customer (MED badge, 14-day meter)")
world(s)
pos_frame(s, "✓ MED card verified", OK, [("Strain A", "28 g", "$xx.xx", True), ("Strain E", "14 g", "$xx.xx", False)], "$xx.xx", "Tax 9.1% (medical)", "$xx.xx")
meter(s, 500, 560, 440, "14-day remaining", "42.0 g", "49.4 g", WARN, "⚠ 7.4 g left after this sale")
s.t(500, 690, "Allotment 70.87 g · 21.5 g bought in the last 14 days", 16, T3)
s.t(500, 790, "Sale type", 22, T2, 600)
s.btn(640, 760, 160, "● Medical", None, h=50); s.btn(810, 760, 170, "○ Adult-use", None, h=50); s.f(5, 630, 755)
pos_buttons(s)
s.note("MED badge replaces '21+ ID verified'. Meter = cart flower g / (70.87 g − 14-day history); 28 g cap does not apply; amber/red rules as the flower meter.")
s.note("Tax line reads 'Tax 9.1% (medical)'; same pre-tax line prices as adult-use (DEC-048). Sale type switch defaults to Medical; Adult-use swaps tax + meter to 28 g.")
s.note("Medical customers are rare (< 5 %, DEC-048). Payment row moves to the right of Sale type in the build (omitted here for space).")
screens.append(s)

# 07 out-of-state medical card
s = S("ps1_07_pos_med_oos", "PS1-07 Register: out-of-state medical card")
world(s)
pos_frame(s, "⚠ Card: out-of-state", WARN, [("Strain B", "7 g", "$xx.xx", False)], "$xx.xx", "Tax 9.1% (medical)", "$xx.xx", focus=False)
meter(s, 500, 560, 440, "14-day remaining", "7.0 g", "70.9 g", OK, "")
s.t(500, 790, "Sale type", 22, T2, 600)
s.btn(640, 760, 160, "● Medical", None, h=50); s.btn(810, 760, 170, "○ Adult-use", None, h=50); s.f(1, 800, 755)
pos_buttons(s, focus=False)
s.r(96, 70, 640, 140, fill="#0f1215e6", stroke=WARN, rx=10)
s.t(124, 112, "⚠ Can't ring an out-of-state card as medical", 22, T1, 700)
s.t(124, 148, "Switch the sale to Adult-use (21+, 1 oz limit).", 20, T2)
s.t(124, 186, "hint: first wrong Confirm only; after that = strike", 16, T3)
s.note("Cue is the badge only ('⚠ Card: out-of-state'); no banner up front, so spotting it is the decision (SPEC_COMP002 §4, GAP-COMP-04).")
s.note("Confirm as Medical: 1st time blocked + hint toast; later times blocked + strike. Switching to Adult-use: tax 25.1 %, meter becomes Flower / 28 g.")
s.note("Switch key: T toggles Sale type (mouse: click). Normal POS focus order; marker 1 only points at the switch.")
screens.append(s)

# 08 strike toast + report rows
s = S("ps1_08_strike_report", "PS1-08 Strike toast and shift report compliance rows")
world(s)
s.r(96, 70, 640, 150, fill="#0f1215e6", stroke=BAD, rx=10)
s.t(124, 112, "✗ Strike · An invalid ID got through", 24, T1, 700)
s.t(124, 148, "Stores can be fined up to $2,000 per violation.", 20, T2)
s.t(124, 190, "6 s · logged to the shift report", 16, T3)
dim(s)
s.r(560, 250, 800, 780, fill=PANEL, stroke=LINE, rx=16)
s.t(600, 306, "Shift report ★★☆", 28, T1, 700)
s.t(600, 350, "… slice rows unchanged (customers, revenue, satisfaction …)", 18, T3)
s.t(600, 400, "Compliance", 24, T1, 700)
rows = [("Strikes", "2  ⚠ Manager review"), ("  14:31 · An invalid ID got through", ""), ("  15:02 · Rang an out-of-state card as medical", ""),
        ("IDs checked", "3"), ("Bad IDs caught", "1"), ("Valid IDs refused", "0"), ("Over-limit trims", "1"),
        ("Medical sales", "1"), ("Medical tax collected", "$x.xx"), ("Adult-use tax collected", "$xx.xx")]
for i, (k, v) in enumerate(rows):
    y = 444 + i * 44
    s.t(600, y, k, 20 if k.startswith("  ") else 22, T3 if k.startswith("  ") else T2)
    s.t(1320, y, v, 22, WARN if "review" in v else T1, 600, "end")
    s.el.append(f'<line x1="600" y1="{y+14}" x2="1320" y2="{y+14}" stroke="{LINE}" stroke-width="1"/>')
s.btn(1060, 920, 260, "Close", "Esc / Enter")
s.note("Strike toast: top-left like other toasts, ✗ + BAD colour, 6 s (longer than the 4 s sale toast), never steals focus; second line = flavour text for that strike (B4 for IDs).")
s.note("Report: a 'Compliance' block below the slice rows. Strikes row shows count + '⚠ Manager review' at strikeReviewThreshold (2); one indented row per strike: time · reason.")
s.note("Rows with zero events still show 0 (so players learn they exist). Medical rows hidden when the shift had no medical customer. Strikes never end the shift (DEC-032).")
screens.append(s)

os.makedirs(OUT, exist_ok=True)
for s in screens:
    p = os.path.join(OUT, s.name + ".svg")
    open(p, "w", encoding="utf-8").write(s.svg())
    assert os.path.getsize(p) < 500_000, p
print(len(screens), "written")
