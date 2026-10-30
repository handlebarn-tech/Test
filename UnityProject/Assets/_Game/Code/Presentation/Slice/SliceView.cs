using System.Collections.Generic;
using System.Linq;
using Dispo.Domain.Engine;
using Dispo.Simulation.Slice;
using UnityEngine;
using UnityEngine.UIElements;

namespace Dispo.Presentation.Slice
{
    /// <summary>
    /// UI Toolkit screens for the slice (UX_SLICE §3, with SLICE_DESIGN §10 rulings: single-select tiles, Inspect, More options;
    /// no Compare, questions, budget stepper, role tag or why line). Built in code on one UIDocument; styles in UI/Slice/Slice.uss.
    /// Each screen is rebuilt on Render(); the HUD, toasts, jar labels and debug overlay refresh in Tick().
    /// </summary>
    public sealed class SliceView
    {
        static readonly string[] ShownDomains = { DomainIds.Sedation, DomainIds.Uplift, DomainIds.AnxietyRelief, DomainIds.PainInflammation, "focus_cognitive" };

        readonly SliceGame _g;
        readonly VisualElement _root, _screen, _toasts, _jarLayer, _debug;
        readonly Label _clock, _sales, _queue, _prompt;
        readonly Dictionary<string, Label> _jarLabels = new Dictionary<string, Label>();
        readonly List<(VisualElement el, float until)> _toastList = new List<(VisualElement, float)>();
        Button _confirm;
        bool _debugOn, _wasRed;

        public string Message = "";

        public SliceView(VisualElement root, StyleSheet style, SliceGame g)
        {
            _g = g;
            _root = root;
            if (style) root.styleSheets.Add(style);
            root.AddToClassList("slice-root");
            root.pickingMode = PickingMode.Ignore;

            _jarLayer = Add(root, "jar-layer");
            var hud = Add(root, "hud");
            _clock = AddLabel(hud, "", "hud-clock");
            _sales = AddLabel(hud, "", "hud-sales");
            _queue = AddLabel(hud, "", "hud-queue");
            _prompt = AddLabel(root, "", "prompt");
            _screen = Add(root, "screen");
            _toasts = Add(root, "toasts");
            _debug = Add(root, "debug");
            _debugOn = false;
            Render();
        }

        public void ToggleDebug() => _debugOn = !_debugOn && (Debug.isDebugBuild || Application.isEditor);
        public bool DebugVisible { get => _debugOn; set => _debugOn = value && (Debug.isDebugBuild || Application.isEditor); }

        // ---------------- per frame ----------------

        public void Tick()
        {
            var sim = _g.Sim;
            int mins = (int)(sim.ClockHours * 60);
            _clock.text = $"{mins / 60:00}:{mins % 60:00}";
            _sales.text = $"Sales ${sim.Sales.Sum(s => s.PricePostTax):0.00}";
            _queue.text = sim.Covering ? CounterLine() : $"Queue {sim.Queue.Count}";
            _queue.EnableInClassList("counter-line", sim.Covering);
            // UX_PS1 §4: while covering the stand, the HUD becomes the Counter line strip, also over the ID panel.
            bool hudOn = _g.Screen == SliceScreen.World || (_g.Screen == SliceScreen.IdCheck && sim.Covering);
            _clock.parent.style.display = hudOn ? DisplayStyle.Flex : DisplayStyle.None;
            bool world = _g.Screen == SliceScreen.World;
            _prompt.text = world && _g.CanCheckId ? sim.Data.Lines.standPrompt
                : world && _g.CanTalk ? "E  Talk" : world && sim.Serving != null && _g.CustomerAtCounter ? "Go to the register"
                : world && sim.Covering ? string.Format(sim.Data.Lines.standHud, sim.StandDone, sim.StandTotal) : "";
            _prompt.style.display = _prompt.text.Length > 0 ? DisplayStyle.Flex : DisplayStyle.None;

            for (int i = _toastList.Count - 1; i >= 0; i--)
                if (Time.unscaledTime > _toastList[i].until) { _toastList[i].el.RemoveFromHierarchy(); _toastList.RemoveAt(i); }

            JarLabels();
            if (_confirm != null) _confirm.text = _g.HoldProgress > 0 ? $"Confirm… {_g.HoldProgress * 100:0}%" : "Hold to confirm";
            DebugOverlay();
        }

        /// <summary>UX_PS1 §4 Counter line strip: one patience word + icon per queued customer (max 5, then +n), stand count.</summary>
        string CounterLine()
        {
            var sim = _g.Sim;
            var l = sim.Data.Lines;
            string[] icons = { "●", "◐", "▲" };
            var rows = new List<string> { string.Format(l.counterLine, sim.Queue.Count) };
            foreach (var c in sim.Queue.Take(5))
            {
                double f = c.Patience / c.PatienceMax;
                int w = f > 0.75 ? 0 : f > sim.Cfg.impatientFraction ? 1 : 2;   // [GDD] Relaxed / Waiting / Impatient
                rows.Add($"{icons[w]} {l.patienceWords[w]}");
            }
            if (sim.Queue.Count > 5) rows.Add($"+{sim.Queue.Count - 5} more");
            rows.Add(string.Format(l.standWaiting, sim.Stand.Count));
            return string.Join("\n", rows);
        }

        /// <summary>§4: LOW / SOLD OUT labels over the jars, projected into the panel.</summary>
        void JarLabels()
        {
            var cam = _g.ViewCamera;
            var inv = _g.Sim.Inventory;
            foreach (var kv in _g.JarTops)
            {
                string text = inv.IsSoldOut(kv.Key) ? "SOLD OUT" : inv.IsLow(kv.Key) ? "LOW" : null;
                if (!_jarLabels.TryGetValue(kv.Key, out var label))
                {
                    if (text == null) continue;
                    label = _jarLabels[kv.Key] = AddLabel(_jarLayer, "", "jar-label");
                }
                label.text = text ?? "";
                label.EnableInClassList("st-bad", text == "SOLD OUT");
                bool visible = text != null && cam && _root.panel != null && _g.Screen == SliceScreen.World
                               && Vector3.Dot(cam.transform.forward, kv.Value - cam.transform.position) > 0
                               && Vector3.Distance(cam.transform.position, kv.Value) < 9f;
                label.style.display = visible ? DisplayStyle.Flex : DisplayStyle.None;
                if (!visible) continue;
                // Viewport → panel layout: independent of Screen size, so it holds when camera or panel render to a texture (REVIEW-W3D N1).
                var p = JarLabelPanelPos(kv.Value, cam);
                label.style.left = p.x - 30;
                label.style.top = p.y - 12;
            }
        }

        /// <summary>Panel position (px) of a world point seen by a full-panel camera.</summary>
        public Vector2 JarLabelPanelPos(Vector3 world, Camera cam)
        {
            var vp = cam.WorldToViewportPoint(world);
            return new Vector2(vp.x * _root.layout.width, (1 - vp.y) * _root.layout.height);
        }

        public Label JarLabel(string batchId) => _jarLabels.TryGetValue(batchId, out var l) ? l : null;

        void DebugOverlay()
        {
            _debug.style.display = _debugOn ? DisplayStyle.Flex : DisplayStyle.None;
            if (!_debugOn) return;
            var sim = _g.Sim;
            _debug.Clear();
            AddLabel(_debug, "DEBUG (dev build) — true intents", "debug-title");
            foreach (var c in sim.Customers)
                AddLabel(_debug, $"#{c.Index:00} {c.State,-10} {c.Archetype.label,-13} {c.TrueFamily.id,-8} {c.Grams,4} g  budget {(c.HasBudget ? "$" + c.Budget : "—"),-5} "
                    + $"fit {(c.LastFit < 0 ? "—" : c.LastFit.ToString("0.00"))}  sat {(c.LastSatisfaction < 0 ? "—" : c.LastSatisfaction.ToString("0"))}  "
                    + $"pat {c.Patience:0}/{c.PatienceMax:0}  {c.Outcome}", "debug-line");
            if (_g.FallbackAnchors.Count > 0) AddLabel(_debug, $"TEMP anchors: {_g.FallbackAnchors.Count} (ART-002 pending)", "debug-line");
        }

        public void Toast(string line1, string line2, bool warn) => Toast(line1, line2, warn ? "st-warn" : null, _g.Sim.Cfg.toastSeconds);

        /// <summary>UX_PS1 §6: a strike toast has the --bad border and stays strikeToastSeconds.</summary>
        public void Toast(string line1, string line2, string state, double seconds)
        {
            if (_g.Screen == SliceScreen.Report) return;
            var t = Add(_toasts, "toast");
            if (state != null) t.AddToClassList(state);
            AddLabel(t, line1, "toast-1");
            if (!string.IsNullOrEmpty(line2)) AddLabel(t, line2, "toast-2");
            _toastList.Add((t, Time.unscaledTime + (float)seconds));
        }

        // ---------------- screens ----------------

        public void Render()
        {
            _screen.Clear();
            // UX_SLICE §5 / UX_COUNTER_INTEL §10 text scale (the register and limit meter honour it, GAME-007).
            _root.EnableInClassList("text-125", _g.TextScale == 125);
            _root.EnableInClassList("text-150", _g.TextScale == 150);
            _root.EnableInClassList("register-open", _g.Screen == SliceScreen.Pos);
            _root.EnableInClassList("id-open", _g.Screen == SliceScreen.IdCheck);
            if (_g.Screen == SliceScreen.Report) { _toasts.Clear(); _toastList.Clear(); }   // nothing on top of the report
            _confirm = null;
            var s = _g.Screen;
            _screen.pickingMode = s == SliceScreen.World ? PickingMode.Ignore : PickingMode.Position;
            _screen.EnableInClassList("dim", s != SliceScreen.World && s != SliceScreen.Dialogue && s != SliceScreen.IdCheck);   // ID panel dims only behind itself
            switch (s)
            {
                case SliceScreen.Dialogue: Dialogue(); break;
                case SliceScreen.Query: Terminal(Query); break;
                case SliceScreen.Results: Terminal(Results); break;
                case SliceScreen.Detail: Terminal(Detail); break;
                case SliceScreen.Pos: Pos(); break;
                case SliceScreen.Report: Report(); break;
                case SliceScreen.CoverPrompt: CoverPrompt(); break;
                case SliceScreen.IdCheck: IdPanel(); break;
            }
        }

        void Dialogue()
        {
            var c = _g.Sim.Serving;
            var box = Add(_screen, "dialogue");
            var sub = Add(box, "dialogue-sub");
            AddLabel(sub, $"Customer · {c.Archetype.label}", "speaker");
            AddLabel(sub, c.Rejections > 0 && _g.LastReject != null ? _g.LastReject : c.Line, "line");
            var opts = Add(box, "dialogue-options");
            AddButton(opts, "1  Look it up", _g.LookItUp, "primary");
            if (_g.Sim.Results != null) AddButton(opts, "2  Edit search", _g.EditSearch);
        }

        void Terminal(System.Action<VisualElement> body)
        {
            var sim = _g.Sim;
            var c = sim.Serving;
            var term = Add(_screen, "terminal");
            var strip = Add(term, "request-strip");
            AddLabel(strip, c.Archetype.label, "archetype");
            AddLabel(strip, $"“{c.Line}”", "request");
            // UX_PS1 §2: tick each clause already in the cart; the cart chip goes to the register (R).
            if (c.Asks.Count > 1)
                for (int i = 0; i < c.Asks.Count; i++)
                    AddLabel(strip, (sim.Cart.Any(x => x.Ask == i) ? "✓ " : "○ ") + c.Asks[i].Clause, "hint");
            if (sim.Cart.Count > 0)
                AddButton(strip, string.Format(sim.Data.Lines.cartChip, sim.Cart.Count, sim.Cfg.cartMaxLines, sim.CartGrams.ToString("0.#")), _g.GoToRegister).tooltip = sim.Data.Lines.goToRegister;
            body(Add(term, "terminal-body"));
            if (!string.IsNullOrEmpty(Message)) AddLabel(term, "⚠ " + Message, "message st-bad");
            AddButton(term, "Back (Esc)", _g.Back, "back");
        }

        void Query(VisualElement body)
        {
            AddLabel(body, "What are they looking for?", "h1");
            var tiles = Add(body, "tiles");
            foreach (var f in _g.Sim.Data.Intents.families)
            {
                var b = AddButton(tiles, f.chip, () => _g.ChooseChip(f), "tile");
                b.EnableInClassList("selected", _g.Sim.Serving.Chip == f.id);
            }
        }

        void Results(VisualElement body)
        {
            var r = _g.Sim.Results;
            var l = _g.Sim.Data.Lines;
            var head = Add(body, "row");
            AddLabel(head, $"Search: {r.Chip.chip}", "h1");
            AddButton(head, "Edit search", _g.EditSearch);
            if (r.Outcome == Outcome.Fallback) AddLabel(body, "◐ " + l.fallbackBanner, "banner st-warn");
            if (r.Outcome == Outcome.None) { AddLabel(body, l.noneMatched, "h1"); return; }
            var cards = new ScrollView(ScrollViewMode.Horizontal);
            cards.AddToClassList("cards");
            body.Add(cards);
            for (int i = 0; i < r.Cards.Count; i++) CardView(cards, r.Cards[i], i == 0, r.Outcome);
            if (r.MoreAvailable) AddButton(body, "More options (M)", _g.More, "more");
        }

        void CardView(VisualElement parent, Card k, bool top, Outcome outcome)
        {
            var l = _g.Sim.Data.Lines;
            var card = Add(parent, "card");
            card.EnableInClassList("is-top", top);
            card.EnableInClassList("is-fallback", outcome == Outcome.Fallback);
            AddLabel(card, k.Strain.Name, "card-name");
            AddLabel(card, $"{k.Rep.Brand} · {k.TierLabel} · {k.Strain.Profile.Values.Sum():0.0}% terps", "card-sub");
            AddLabel(card, outcome == Outcome.Fallback ? l.fitFallback : l.fitOk, outcome == Outcome.Fallback ? "fit st-warn" : "fit st-ok");
            AddLabel(card, k.ClusterLabel, "card-cluster");
            AddLabel(card, k.HasPrice ? $"${k.PricePostTax:0.00}  ·  {l.Weight(_g.Sim.Serving.Asks[_g.Sim.Results.Ask].Grams)}" : "no price", "price");
            AddLabel(card, $"{_g.Sim.Inventory.Grams(k.Rep.Id):0.#} g in jar", "card-grams");
            AddLabel(card, k.AnxietyLabel, "chip " + AnxClass(k.Strain.AnxietyRisk));
            var row = Add(card, "row");
            AddButton(row, "Inspect", () => _g.Inspect(k));
            AddButton(row, ChooseText, () => _g.Choose(k), "primary").SetEnabled(_g.Sim.CurrentAsk != null);
        }

        string ChooseText => _g.Sim.Cart.Count > 0 ? _g.Sim.Data.Lines.addToCart : "Choose";

        string AnxClass(int risk) => risk < _g.Sim.Cfg.anxietyLowBelow ? "st-ok" : risk < _g.Sim.Cfg.anxietyModerateBelow ? "st-warn" : "st-bad";

        void Detail(VisualElement body)
        {
            var k = _g.DetailCard;
            var sim = _g.Sim;
            AddLabel(body, k.Strain.Name, "h1");
            var cols = Add(body, "row detail");
            var left = Add(cols, "col");
            AddLabel(left, "HEURISTIC · terpene model", "evidence");
            foreach (var d in ShownDomains)
            {
                int v = k.Strain.Domains.TryGetValue(d, out var x) ? x : 0;
                var bar = Add(left, "bar");
                AddLabel(bar, d.Replace('_', ' '), "bar-name");
                var track = Add(bar, "bar-track");
                Add(track, "bar-fill").style.width = Length.Percent(v);
                AddLabel(bar, v.ToString(), "bar-value");
            }
            AddLabel(left, "INFERRED · cluster", "evidence");
            AddLabel(left, $"{k.ClusterLabel} ({Labels.ClusterName(k.Strain.Cluster)})");
            AddLabel(left, k.AnxietyLabel, "chip " + AnxClass(k.Strain.AnxietyRisk));
            AddLabel(left, "A model of the terpene data, not a promise of effects.", "caveat");

            var right = Add(cols, "col");
            AddLabel(right, "OBSERVED · batch", "evidence");
            var b = k.Rep;
            int weeks = _g.AgeWeeks(b);
            AddLabel(right, $"Batch {b.BatchCode} · {b.Brand} · {k.TierLabel}");
            AddLabel(right, $"COA {(b.TestDate.HasValue ? b.TestDate.Value.ToString("yyyy-MM-dd") : "unknown")}{(weeks >= 0 ? $" · {weeks} wk old" : "")} · {b.Total:0.0}% terps");
            AddLabel(right, $"{sim.Inventory.Grams(b.Id):0.#} g in jar");
            AddLabel(right, "Top terpenes: " + string.Join(", ", k.Strain.Profile.OrderByDescending(kv => kv.Value).Take(3)
                .Select(kv => $"{(sim.Data.Catalog.Terpenes.TryGetValue(kv.Key, out var t) ? t.Name : kv.Key)} {kv.Value:0.00}%")));
            foreach (var w in sim.Data.Catalog.Pricing.Weights)
            {
                var p = sim.Price(b, w);
                AddLabel(right, p == null ? $"{sim.Data.Lines.Weight(w)}: —" : $"{sim.Data.Lines.Weight(w)}: ${p.CardPostTax:0.00}");
            }
            var row = Add(body, "row");
            AddButton(row, ChooseText, () => _g.Choose(k), "primary");
        }

        void Pos()
        {
            var sim = _g.Sim;
            var c = sim.Serving;
            var l = sim.Data.Lines;
            // UX_PS1 §2-3: lines + Add item, then meter / totals / payment / Confirm. At ≥125 % text the two columns sit side by
            // side in the safe area so Confirm never scrolls off (UX_COUNTER_INTEL §10); at 100 % they stack.
            var panel = Add(_screen, "pos");
            var pos = Add(panel, "pos-col");
            AddLabel(pos, "POS", "h1");
            AddLabel(pos, "✓ " + l.idVerified, "st-ok");   // DEC-036 M2: checked at the check-in desk
            // Cart lines: name and batch · tier ellipsize; − g + / price / ✕ are fixed columns (REVIEW-W4W m1).
            for (int i = 0; i < sim.Cart.Count; i++)
            {
                int n = i;
                var x = sim.Cart[i];
                var lineRow = Add(pos, "cart-line");
                var info = Add(lineRow, "cart-info");
                AddLabel(info, x.Card.Strain.Name, "cart-name").tooltip = x.Card.Strain.Name;
                AddLabel(info, $"batch {x.Card.Rep.BatchCode} · {x.Card.TierLabel}", "cart-sub");
                AddButton(lineRow, "−", () => _g.PosStep(n, -1), "cart-step");
                AddLabel(lineRow, $"{x.Grams} g", "cart-grams");
                AddButton(lineRow, "+", () => _g.PosStep(n, 1), "cart-step");
                AddLabel(lineRow, double.IsNaN(x.PreTax) ? "—" : $"${x.PreTax:0.00}", "cart-price");
                AddButton(lineRow, "✕", () => _g.PosRemove(n), "cart-step").tooltip = l.removeLine;
            }
            var add = AddButton(pos, sim.Cart.Count >= sim.Cfg.cartMaxLines ? string.Format(l.cartFull, sim.Cfg.cartMaxLines) : l.addItem, _g.AddItem);
            add.SetEnabled(sim.CanAddItem);
            pos = Add(panel, "pos-col");
            Meter(pos);
            var p = sim.CartPrice();
            if (!double.IsNaN(p.PreTax))
            {
                if (sim.Cart.Count == 1) Line(pos, "MSRP", p.Msrp);
                if (sim.Cart.Count == 1 && p.DealName != null) Line(pos, p.DealName, p.PreTax - p.Msrp);
                Line(pos, "Subtotal", p.PreTax);
                Line(pos, $"Tax {sim.Data.Catalog.Pricing.TaxRate}%", p.Tax);
                Line(pos, "Total", p.PostTax, "total");
            }
            AddLabel(pos, $"Scale: {sim.CartGrams:0.00} g (assisted)", "scale");
            if (!string.IsNullOrEmpty(Message)) AddLabel(pos, "⚠ " + Message, "message st-bad");
            // Payment and Confirm share a row so a red 3-line cart fits the 972 px safe height at 100 % (GAME-007 capture check).
            var row = Add(pos, "row");
            AddButton(row, "Cash", () => { });
            AddButton(row, "Card", () => { });
            _confirm = AddButton(row, "Hold to confirm", () => { }, "primary");
            _confirm.SetEnabled(sim.Meter != MeterState.Red);   // UX_PS1 §3: red disables Confirm (the POS blocks it anyway, DEC-036 M1)
            _confirm.RegisterCallback<PointerDownEvent>(_ => _g.PosHold(true), TrickleDown.TrickleDown);
            _confirm.RegisterCallback<PointerUpEvent>(_ => _g.PosHold(false));
            _confirm.RegisterCallback<PointerLeaveEvent>(_ => _g.PosHold(false));
            AddButton(row, "Cancel", _g.PosCancel);
            AddLabel(pos, $"Customer asked for {string.Join(" + ", c.Asks.Select(a => l.Weight(a.Grams)))}", "hint");
        }

        /// <summary>UX_PS1 §4 cover prompt (ps1_04): centred card, Y / N.</summary>
        void CoverPrompt()
        {
            var l = _g.Sim.Data.Lines;
            var box = Add(_screen, "cover-prompt");
            AddLabel(box, l.coverPromptTitle, "h1 st-warn");
            AddLabel(box, string.Format(l.coverPromptBody, _g.Sim.Cfg.coverCheckInCount));
            AddLabel(box, l.coverPromptCost, "hint");
            var row = Add(box, "row");
            AddButton(row, l.coverAccept + " (Y)", _g.AcceptCover, "primary");
            AddButton(row, l.coverDecline + " (N)", _g.DeclineCover);
        }

        /// <summary>
        /// UX_PS1 §4 ID panel (ps1_05): header + in-game date, the card at ID-1 ratio (vertical IDs portrait), no verdict shown.
        /// At 125/150 % the decision fields are also listed full size in a readout column (UX_COUNTER_INTEL §10: never truncate).
        /// </summary>
        void IdPanel()
        {
            var sim = _g.Sim;
            var l = sim.Data.Lines;
            var c = _g.IdCustomer;
            var id = c.Id;
            var panel = Add(_screen, "id-panel");
            var head = Add(panel, "id-head");
            AddLabel(head, string.Format(l.idPanelTitle, sim.StandDone + 1, sim.StandTotal), "h1");
            AddLabel(head, string.Format(l.idToday, sim.Today.ToString("ddd MM/dd/yyyy", System.Globalization.CultureInfo.InvariantCulture)), "id-today");
            var body = Add(panel, "id-body");
            var card = Add(body, "id-card " + (id.Format == IdFormat.Vertical ? "id-v" : "id-h"));
            string type = l.idTypeNames[(int)id.Type];
            AddLabel(card, id.State.Length > 0 ? $"{id.State} · {type}" : type, "id-band");
            var inner = Add(card, "id-inner");
            Add(inner, "id-photo");
            var fields = Add(inner, "id-fields");
            string D(System.DateTime d) => d.ToString("MM/dd/yyyy", System.Globalization.CultureInfo.InvariantCulture);
            var rows = new[] { ("NAME", id.Name), ("DOB", D(id.Dob)), ("EXP", D(id.Expires)), ("TYPE", type), ("FORMAT", id.Format == IdFormat.Vertical ? "Vertical" : "Horizontal") };
            foreach (var (k, v) in rows)
            {
                var f = Add(fields, "id-field");
                AddLabel(f, k, "id-key");
                AddLabel(f, v, "id-value" + (k == "NAME" ? " id-name" : ""));
            }
            var side = Add(body, "id-side");
            var readout = Add(side, "id-readout");
            foreach (var (k, v) in rows.Skip(1))
            {
                var f = Add(readout, "id-field");
                AddLabel(f, k, "id-key");
                AddLabel(f, v, "id-value");
            }
            var buttons = Add(side, "id-buttons");
            AddButton(buttons, l.idAdmit + " (A)", _g.IdAdmit, "primary");
            AddButton(buttons, l.idRefuse + " (R)", _g.IdRefuse);
            AddButton(buttons, "Back (Esc)", _g.Back);
        }

        /// <summary>UX_PS1 §3 limit meter: Flower {g} / 28 g, 75 % tick, amber/red state words (never colour only).</summary>
        void Meter(VisualElement parent)
        {
            var sim = _g.Sim;
            var l = sim.Data.Lines;
            var state = sim.Meter;
            var meter = Add(parent, "meter meter-" + state.ToString().ToLowerInvariant());
            var head = Add(meter, "meter-head");
            AddLabel(head, l.meterFlower, "meter-label");
            AddLabel(head, string.Format(l.meterValue, sim.CartGrams.ToString("0.#"), sim.Cfg.adultUseLimitGrams.ToString("0.#")), "meter-value");
            var track = Add(meter, "meter-track");
            Add(track, "meter-fill").style.width = Length.Percent((float)System.Math.Min(100, sim.MeterFraction * 100));
            Add(track, "meter-tick").style.left = Length.Percent((float)(sim.Cfg.meterAmberFraction * 100));
            if (state == MeterState.Amber) AddLabel(meter, l.nearLimit, "meter-state st-warn");
            if (state == MeterState.Red)
            {
                AddLabel(meter, "✗ " + l.overLimit, "meter-state st-bad");
                AddLabel(meter, l.trimHint, "meter-hint");
            }
            // Entering red fires the existing overLimit toast once (UX_PS1 §3).
            if (state == MeterState.Red && !_wasRed) Toast("⚠ " + l.overLimit, "", true);
            _wasRed = state == MeterState.Red;
        }

        void Line(VisualElement parent, string name, double v, string cls = null)
        {
            var row = Add(parent, "price-line" + (cls != null ? " " + cls : ""));
            AddLabel(row, name);
            AddLabel(row, (v < 0 ? "−$" : "$") + System.Math.Abs(v).ToString("0.00"), "amount");
        }

        void Report()
        {
            var r = _g.FinalReport;
            var box = Add(_screen, "report");
            AddLabel(box, $"Shift report  {new string('★', r.Stars)}{new string('☆', 3 - r.Stars)}", "h1");
            if (r.RoughShift) AddLabel(box, "⚠ Rough shift", "banner st-warn");
            void Row(string k, string v) { var row = Add(box, "price-line"); AddLabel(row, k); AddLabel(row, v, "amount"); }
            Row("Customers served", r.CustomersServed.ToString());
            Row("Walkouts", r.Walkouts.ToString());
            Row("No sale", r.NoSales.ToString());
            Row("Revenue (post-tax)", $"${r.RevenuePostTax:0.00}");
            Row("Revenue (pre-tax)", $"${r.RevenuePreTax:0.00}");
            Row("Grams sold", $"{r.GramsSold:0.#} g");
            Row("Units per sale", $"{r.UnitsPerSale:0.0}");
            Row("Avg service time", $"{r.AvgServiceSeconds:0} s");
            Row("Avg queue wait", $"{r.AvgQueueWaitSeconds:0} s");
            Row("Avg satisfaction", $"{r.AvgSatisfaction:0}");
            Row("Avg recommendation fit", $"{r.AvgRecFit:0.00}");
            Row("Interpretation accuracy", $"{r.InterpretationAccuracy:0}%");
            Row("Top intents", string.Join(", ", r.TopIntents.Select(kv => $"{kv.Key} {kv.Value}")));
            Row("Sold out", r.SoldOut.Count == 0 ? "—" : string.Join(", ", r.SoldOut));
            Row("Low stock", $"{r.LowStock.Count} jars");
            // UX_PS1 §6 Compliance block (GAME-008/009 add ID and medical rows).
            AddLabel(box, "Compliance", "h1");
            Row("Strikes", r.Strikes.Count + (r.ManagerReview ? "  ⚠ Manager review" : ""));
            foreach (var s in r.Strikes) Row($"    {_g.ClockText(s.Time)} · {s.Reason}", "");
            Row("IDs checked", r.IdsChecked.ToString());
            Row("Bad IDs caught", r.BadIdsCaught.ToString());
            Row("Valid IDs refused", r.ValidIdsRefused.ToString());
            Row("Over-limit trims", r.OverLimitTrims.ToString());
        }

        // ---------------- helpers ----------------

        static VisualElement Add(VisualElement parent, string classes)
        {
            var e = new VisualElement();
            foreach (var c in classes.Split(' ')) e.AddToClassList(c);
            parent.Add(e);
            return e;
        }

        static Label AddLabel(VisualElement parent, string text, string classes = null)
        {
            var l = new Label(text);
            if (classes != null) foreach (var c in classes.Split(' ')) l.AddToClassList(c);
            parent.Add(l);
            return l;
        }

        static Button AddButton(VisualElement parent, string text, System.Action onClick, string classes = null)
        {
            var b = new Button(onClick) { text = text };
            if (classes != null) foreach (var c in classes.Split(' ')) b.AddToClassList(c);
            parent.Add(b);
            return b;
        }
    }
}
