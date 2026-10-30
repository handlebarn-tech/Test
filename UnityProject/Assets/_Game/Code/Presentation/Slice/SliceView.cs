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
        bool _debugOn;

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
            _queue.text = $"Queue {sim.Queue.Count}";
            bool hudOn = _g.Screen == SliceScreen.World;
            _clock.parent.style.display = hudOn ? DisplayStyle.Flex : DisplayStyle.None;
            _prompt.text = hudOn && _g.CanTalk ? "E  Talk" : hudOn && sim.Serving != null && _g.CustomerAtCounter ? "Go to the register" : "";
            _prompt.style.display = _prompt.text.Length > 0 ? DisplayStyle.Flex : DisplayStyle.None;

            for (int i = _toastList.Count - 1; i >= 0; i--)
                if (Time.unscaledTime > _toastList[i].until) { _toastList[i].el.RemoveFromHierarchy(); _toastList.RemoveAt(i); }

            JarLabels();
            if (_confirm != null) _confirm.text = _g.HoldProgress > 0 ? $"Confirm… {_g.HoldProgress * 100:0}%" : "Hold to confirm";
            DebugOverlay();
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

        public void Toast(string line1, string line2, bool warn)
        {
            if (_g.Screen == SliceScreen.Report) return;
            var t = Add(_toasts, "toast");
            t.EnableInClassList("st-warn", warn);
            AddLabel(t, line1, "toast-1");
            if (!string.IsNullOrEmpty(line2)) AddLabel(t, line2, "toast-2");
            _toastList.Add((t, Time.unscaledTime + (float)_g.Sim.Cfg.toastSeconds));
        }

        // ---------------- screens ----------------

        public void Render()
        {
            _screen.Clear();
            if (_g.Screen == SliceScreen.Report) { _toasts.Clear(); _toastList.Clear(); }   // nothing on top of the report
            _confirm = null;
            var s = _g.Screen;
            _screen.pickingMode = s == SliceScreen.World ? PickingMode.Ignore : PickingMode.Position;
            _screen.EnableInClassList("dim", s != SliceScreen.World && s != SliceScreen.Dialogue);
            switch (s)
            {
                case SliceScreen.Dialogue: Dialogue(); break;
                case SliceScreen.Query: Terminal(Query); break;
                case SliceScreen.Results: Terminal(Results); break;
                case SliceScreen.Detail: Terminal(Detail); break;
                case SliceScreen.Pos: Pos(); break;
                case SliceScreen.Report: Report(); break;
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
            var term = Add(_screen, "terminal");
            var strip = Add(term, "request-strip");
            AddLabel(strip, _g.Sim.Serving.Archetype.label, "archetype");
            AddLabel(strip, $"“{_g.Sim.Serving.Line}”", "request");
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
            AddLabel(card, k.HasPrice ? $"${k.PricePostTax:0.00}  ·  {l.Weight(_g.Sim.Serving.Grams)}" : "no price", "price");
            AddLabel(card, $"{_g.Sim.Inventory.Grams(k.Rep.Id):0.#} g in jar", "card-grams");
            AddLabel(card, k.AnxietyLabel, "chip " + AnxClass(k.Strain.AnxietyRisk));
            var row = Add(card, "row");
            AddButton(row, "Inspect", () => _g.Inspect(k));
            AddButton(row, "Choose", () => _g.Choose(k), "primary");
        }

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
            AddButton(row, "Choose", () => _g.Choose(k), "primary");
        }

        void Pos()
        {
            var sim = _g.Sim;
            var k = sim.Pending;
            var c = sim.Serving;
            var pos = Add(_screen, "pos");
            AddLabel(pos, "POS", "h1");
            AddLabel(pos, $"{k.Strain.Name} · batch {k.Rep.BatchCode}");
            AddLabel(pos, "✓ " + sim.Data.Lines.idVerified, "st-ok");   // DEC-036 M2: checked at the check-in desk
            var tiles = Add(pos, "row");
            double jar = sim.Inventory.Grams(k.Rep.Id);
            foreach (var w in sim.Data.Catalog.Pricing.Weights)
            {
                var t = AddButton(tiles, $"{w} g", () => _g.PosSelectWeight(w), "tile");
                t.SetEnabled(jar >= w);
                t.EnableInClassList("selected", w == _g.PosGrams);
            }
            var p = sim.Price(k.Rep, _g.PosGrams);
            if (p != null)
            {
                Line(pos, "MSRP", p.Msrp);
                if (p.DealName != null) Line(pos, p.DealName, p.PreTax - p.Msrp);
                Line(pos, "Subtotal", p.PreTax);
                Line(pos, $"Tax {sim.Data.Catalog.Pricing.TaxRate}%", p.Tax);
                Line(pos, "Total", p.PostTax, "total");
            }
            AddLabel(pos, $"Scale: {_g.PosGrams:0.00} g (assisted)", "scale");
            var pay = Add(pos, "row");
            AddButton(pay, "Cash", () => { });
            AddButton(pay, "Card", () => { });
            if (!string.IsNullOrEmpty(Message)) AddLabel(pos, "⚠ " + Message, "message st-bad");
            var row = Add(pos, "row");
            _confirm = AddButton(row, "Hold to confirm", () => { }, "primary");
            _confirm.RegisterCallback<PointerDownEvent>(_ => _g.PosHold(true), TrickleDown.TrickleDown);
            _confirm.RegisterCallback<PointerUpEvent>(_ => _g.PosHold(false));
            _confirm.RegisterCallback<PointerLeaveEvent>(_ => _g.PosHold(false));
            AddButton(row, "Cancel", _g.PosCancel);
            AddLabel(pos, $"Customer asked for {sim.Data.Lines.Weight(c.Grams)}", "hint");
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
            Row("Avg service time", $"{r.AvgServiceSeconds:0} s");
            Row("Avg queue wait", $"{r.AvgQueueWaitSeconds:0} s");
            Row("Avg satisfaction", $"{r.AvgSatisfaction:0}");
            Row("Avg recommendation fit", $"{r.AvgRecFit:0.00}");
            Row("Interpretation accuracy", $"{r.InterpretationAccuracy:0}%");
            Row("Top intents", string.Join(", ", r.TopIntents.Select(kv => $"{kv.Key} {kv.Value}")));
            Row("Sold out", r.SoldOut.Count == 0 ? "—" : string.Join(", ", r.SoldOut));
            Row("Low stock", $"{r.LowStock.Count} jars");
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
