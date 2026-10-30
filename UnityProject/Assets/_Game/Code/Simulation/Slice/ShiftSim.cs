using System;
using System.Collections.Generic;
using System.Linq;
using Dispo.Domain.Engine;

namespace Dispo.Simulation.Slice
{
    /// <summary>One result card (§3.1 step 4): engine strain + its rep batch, priced for the customer's stated weight.</summary>
    public sealed class Card
    {
        public StrainResult Strain;
        public Batch Rep;
        public double PricePreTax, PricePostTax;   // card display (tool priceFloor); NaN when the tier has no price for that weight
        public double CheckoutPostTax;             // what the POS will charge (DEC-035 nickel rounding)
        public string TierLabel, ClusterLabel, AnxietyLabel;
        public bool HasPrice => !double.IsNaN(PricePostTax);
    }

    public sealed class SearchResult
    {
        public int Ask;                  // index of the customer's ask the cards are priced for
        public IntentFamily Chip;
        public Outcome Outcome;
        public List<Card> Cards = new List<Card>();
        public bool MoreAvailable;
    }

    public enum Response { Blocked, Accept, Reject, Leave }

    public sealed class PresentResult
    {
        public Response Response;
        public string Line;              // reason / blocked message ("" on accept)
        public double Fit, PriceFit, SpeedFit, WaitPenalty, Satisfaction;
    }

    /// <summary>PostTax = checkout total, nearest $0.05 (DEC-035); CardPostTax = the tool's priceFloor display (v7.11.4) for cards.</summary>
    public sealed class PriceLines { public double Msrp, PreTax, Tax, PostTax, CardPostTax; public string DealName; }

    /// <summary>One register line (GAME-006): the accepted card for one ask, at a weight the player can step.</summary>
    public sealed class CartLine
    {
        public int Ask;
        public Card Card;
        public double Grams, Fit;
        public PriceLines Price;         // null when the tier has no price at this weight
        public string BatchId => Card.Rep.Id;
        public double PreTax => Price?.PreTax ?? double.NaN;
    }

    /// <summary>
    /// The slice shift (SLICE_DESIGN §1-§5): arrivals, queue + patience, service flow, scoring, POS and the report.
    /// Unity-free; the presentation layer calls Tick() and the terminal/POS methods.
    /// </summary>
    public sealed class ShiftSim
    {
        public readonly SliceData Data;
        public readonly SliceConfig Cfg;
        public readonly InventoryService Inventory;
        public readonly List<Customer> Customers;
        public readonly List<Customer> Queue = new List<Customer>();   // [0] = front (slot 0); index ≥ queueSlots waits at spawn
        public readonly List<SaleEvent> Sales = new List<SaleEvent>();
        public Customer Serving { get; private set; }
        public SearchResult Results { get; private set; }
        public readonly List<CartLine> Cart = new List<CartLine>();     // GAME-006: 1-cartMaxLines accepted lines, sold together
        public bool RegisterOpen { get; private set; }                  // the POS is up (search/present wait until Add item)
        public Card Pending => RegisterOpen ? Cart[Cart.Count - 1].Card : null;   // the slice's single accepted card (last line)
        public double Time { get; private set; }
        public bool IsOver => Customers.All(c => c.State == CustomerState.Done);
        public event Action<Customer> Left;

        readonly Dictionary<string, Batch> _batches;
        readonly HashSet<string> _seen = new HashSet<string>();
        double _speedFit;   // speedFit of the last accepted pick (§3.3: service start → card pick)

        public ShiftSim(SliceData data)
        {
            Data = data; Cfg = data.Config;
            var rng = new Random(Cfg.seed);
            Customers = CustomerGenerator.Generate(data, rng);
            var bestsellers = data.Intents.families.Select(f => Recommend(f, 1).Strains.FirstOrDefault()?.RepBatchId).Where(id => id != null);
            Inventory = new InventoryService(data.Catalog, Cfg, rng, bestsellers);
            Inventory.Sold += Sales.Add;
            _batches = data.Catalog.Batches.ToDictionary(b => b.Id);
        }

        public void Tick(double dt)
        {
            Time += dt;
            foreach (var c in Customers)
                if (c.State == CustomerState.NotArrived && c.SpawnTime <= Time) { c.State = CustomerState.Queued; Queue.Add(c); }
            foreach (var c in Queue.ToList())
            {
                c.Patience -= dt;   // §5: drains only while queued
                if (c.Patience > 0) continue;
                c.Patience = 0; c.QueueWait = Time - c.SpawnTime;
                Finish(c, CustomerOutcome.Walkout);
            }
            if (Serving == null && Queue.Count > 0)
            {
                Serving = Queue[0]; Queue.RemoveAt(0);
                Serving.State = CustomerState.Serving; Serving.ServiceStart = Time; Serving.QueueWait = Time - Serving.SpawnTime;
                Results = null; Cart.Clear(); RegisterOpen = false; _seen.Clear();
            }
        }

        // ---------- terminal ----------

        /// <summary>§3.1 step 3: engine on live stock for the chosen chip.</summary>
        public SearchResult Search(IntentFamily chip, bool autoFilled = false)
        {
            Require(Serving != null && !RegisterOpen && CurrentAsk != null, "search needs a customer at the counter, an open ask and no open POS");
            Serving.Chip = CurrentAsk.Chip = chip.id; Serving.AutoFilled = autoFilled;
            _seen.Clear();
            var r = Recommend(chip, Cfg.resultCount);
            Results = new SearchResult { Ask = CurrentAskIndex, Chip = chip, Outcome = r.Outcome };
            Append(r.Strains);
            Results.MoreAvailable = Recommend(chip, Cfg.moreOptionsN).Strains.Any(s => !_seen.Contains(s.Key));
            return Results;
        }

        /// <summary>§10 More options: rerun with n = moreOptionsN, append the next moreOptionsStep unseen.</summary>
        public SearchResult MoreOptions()
        {
            Require(Results != null && !RegisterOpen, "more options needs a search and no open POS");
            var unseen = Recommend(Results.Chip, Cfg.moreOptionsN).Strains.Where(s => !_seen.Contains(s.Key)).ToList();
            Append(unseen.Take(Cfg.moreOptionsStep));
            Results.MoreAvailable = unseen.Count > Cfg.moreOptionsStep;
            return Results;
        }

        /// <summary>§3.1 steps 5-7 and §3.2-3.5, for the current ask. ACCEPT adds a cart line and opens the register (UX_PS1 §1).</summary>
        public PresentResult Present(Card card)
        {
            Require(Serving != null && !RegisterOpen && CurrentAsk != null, "present needs a customer at the counter, an open ask and no open POS");
            var c = Serving;
            var ask = CurrentAsk;
            var price = Price(card.Rep, ask.Grams);
            if (Free(card.Rep.Id) < ask.Grams || price == null) return new PresentResult { Response = Response.Blocked, Line = Data.Lines.notEnough };

            var line = new CartLine { Ask = CurrentAskIndex, Card = card, Grams = ask.Grams, Price = price };
            var p = Score(c, ask, card, line, Time - c.ServiceStart);
            c.LastFit = p.Fit; c.LastSatisfaction = p.Satisfaction;
            if (p.Satisfaction >= Cfg.acceptThreshold)
            {
                p.Response = Response.Accept; p.Line = "";
                line.Fit = p.Fit; _speedFit = p.SpeedFit;
                Cart.Add(line); RegisterOpen = true;
                return p;
            }

            c.Rejections++;
            p.Line = p.PriceFit < 0.5 ? Data.Lines.rejectPrice : p.Fit < 0.5 ? Data.Lines.rejectFit : Data.Lines.rejectOther;
            if (c.Rejections >= Cfg.maxRejections) { p.Response = Response.Leave; Finish(c, CustomerOutcome.NoSale); }
            else p.Response = Response.Reject;
            return p;
        }

        // ---------- POS ----------

        /// <summary>POS lines for a batch at a weight (§3.7: tax line = total − subtotal so the floor always adds up).</summary>
        public PriceLines Price(Batch rep, double grams)
        {
            var pc = Data.Catalog.Pricing;
            var q = Pricing.GetEffectivePrices(pc, rep.Tier, Cfg.shiftDayOfWeek);
            if (!q.Prices.TryGetValue(grams, out var pre)) return null;
            pc.Tiers.TryGetValue(rep.Tier ?? "", out var msrp);
            double post = CheckoutRound(pre * (1 + pc.TaxRate / 100));
            return new PriceLines { Msrp = msrp != null && msrp.TryGetValue(grams, out var m) ? m : pre, PreTax = pre, PostTax = post, Tax = post - pre,
                CardPostTax = Pricing.ApplyTax(pre, pc.TaxRate), DealName = q.DealName };
        }

        /// <summary>DEC-035: the real register rounds the after-tax total to the nearest $0.05 (same 4-dp pre-round as priceFloor).</summary>
        public static double CheckoutRound(double x) =>
            x > 0 ? Math.Round(JsMath.Round(x * 10000) / 10000 * 20, MidpointRounding.AwayFromZero) / 20 : 0;

        /// <summary>DEC-036 M3: store clock (hours) for a sim time.</summary>
        public double ClockHours => Cfg.shiftStartHour + Time / 3600;

        /// <summary>
        /// §10 #6 per line: each weight must be the stated one and the jars must hold the cart (lines on one batch add up);
        /// DEC-036 M1 on the cart's summed flower grams. On sale: one SaleEvent per line, the after-tax total rounded once on the
        /// cart (DEC-035), the last line taking the rounding so Σ events = the register total. Returns the blocking line, or null.
        /// </summary>
        public string Confirm()
        {
            Require(RegisterOpen, "nothing accepted");
            var c = Serving;
            var l = Data.Lines;
            if (CartGrams > Cfg.adultUseLimitGrams) return l.overLimit;   // DEC-036 M1, A.R.S. 36-2858(A)(1)(c)
            var wrong = Cart.FirstOrDefault(x => x.Grams != c.Asks[x.Ask].Grams);
            if (wrong != null) return string.Format(l.wrongWeight, l.Weight(c.Asks[wrong.Ask].Grams));
            if (Cart.GroupBy(x => x.BatchId).Any(g => Inventory.Grams(g.Key) < g.Sum(x => x.Grams))) return l.notEnough;

            var total = CartPrice();
            double rate = 1 + Data.Catalog.Pricing.TaxRate / 100, paid = 0;
            for (int i = 0; i < Cart.Count; i++)
            {
                var x = Cart[i];
                double post = i == Cart.Count - 1 ? total.PostTax - paid : x.PreTax * rate;
                paid += post;
                Inventory.Sell(new SaleEvent
                {
                    BatchId = x.BatchId, StrainName = x.Card.Strain.Name, CustomerIndex = c.Index, Grams = x.Grams,
                    PricePreTax = x.PreTax, PricePostTax = post,
                });
            }
            // §3.4 with the mean item fit; an ask left out of the cart counts 0 [GDD].
            c.LastFit = c.Asks.Select((a, i) => Cart.Where(x => x.Ask == i).Select(x => x.Fit).DefaultIfEmpty(0).Max()).Average();
            c.LastSatisfaction = Satisfaction(Cfg, c.LastFit, PriceFit(total.PostTax, c.Budget), _speedFit, WaitPenalty(Cfg, c.QueueWait));
            Finish(c, CustomerOutcome.Bought);
            return null;
        }

        /// <summary>The slice's single-line POS: set the last line's weight, then <see cref="Confirm()"/>.</summary>
        public string Confirm(double grams)
        {
            Require(RegisterOpen, "nothing accepted");
            SetLineGrams(Cart.Count - 1, grams);
            return Confirm();
        }

        /// <summary>POS Cancel: empties the cart, back to the cards; no inventory change (no reservation, §4).</summary>
        public void Cancel() { Cart.Clear(); CloseRegister(); }

        // ---------- cart (GAME-006) ----------

        /// <summary>First ask with no cart line, or null when every ask is in the cart.</summary>
        public Ask CurrentAsk => CurrentAskIndex < 0 ? null : Serving.Asks[CurrentAskIndex];
        public int CurrentAskIndex => Serving == null ? -1 : Enumerable.Range(0, Serving.Asks.Count).Where(i => Cart.All(x => x.Ask != i)).DefaultIfEmpty(-1).First();
        public double CartGrams => Cart.Sum(x => x.Grams);
        public bool CanAddItem => RegisterOpen && CurrentAsk != null && Cart.Count < Cfg.cartMaxLines;

        /// <summary>Jar grams not already in the cart.</summary>
        public double Free(string batchId) => Inventory.Grams(batchId) - Cart.Where(x => x.BatchId == batchId).Sum(x => x.Grams);

        /// <summary>Register totals: Σ line pre-tax, tax, after-tax total rounded once on the cart (DEC-035).</summary>
        public PriceLines CartPrice() => CartPrice(Cart);

        PriceLines CartPrice(IReadOnlyCollection<CartLine> lines)
        {
            double pre = lines.Sum(x => x.PreTax), post = CheckoutRound(pre * (1 + Data.Catalog.Pricing.TaxRate / 100));
            return new PriceLines { Msrp = lines.Sum(x => x.Price?.Msrp ?? double.NaN), PreTax = pre, PostTax = post, Tax = post - pre,
                CardPostTax = double.NaN, DealName = lines.Select(x => x.Price?.DealName).FirstOrDefault(n => n != null) };
        }

        /// <summary>"+ Add item": close the register, keep the cart, search for the next ask.</summary>
        public void AddItem()
        {
            Require(CanAddItem, "add item needs an open register, an open ask and a free line");
            RegisterOpen = false; Results = null; _seen.Clear();
        }

        /// <summary>Cart chip / R: back to the register without adding.</summary>
        public void OpenRegister() { Require(Serving != null && Cart.Count > 0, "the cart is empty"); RegisterOpen = true; }

        /// <summary>The ✕ on a line. The emptied cart closes the register (UX_PS1 §2).</summary>
        public void RemoveLine(int i)
        {
            Require(RegisterOpen, "no open POS");
            Cart.RemoveAt(i);
            if (Cart.Count == 0) CloseRegister();
        }

        public void SetLineGrams(int i, double grams)
        {
            Require(RegisterOpen, "no open POS");
            Cart[i].Grams = grams;
            Cart[i].Price = Price(Cart[i].Card.Rep, grams);
        }

        /// <summary>Line stepper −/+ through the price weights; a weight the jar can't hold is skipped. False when there is no step.</summary>
        public bool StepLine(int i, int dir)
        {
            var x = Cart[i];
            double room = Free(x.BatchId) + x.Grams;
            foreach (var w in Data.Catalog.Pricing.Weights.Where(w => dir * w > dir * x.Grams).OrderBy(w => dir * w))
                if (w <= room && Price(x.Card.Rep, w) != null) { SetLineGrams(i, w); return true; }
            return false;
        }

        void CloseRegister()
        {
            RegisterOpen = false;
            if (Results != null && Results.Ask != CurrentAskIndex) Results = null;   // those cards are priced for another ask's weight
        }

        // ---------- scoring ----------

        PresentResult Score(Customer c, Ask ask, Card card, CartLine line, double t)
        {
            double fit = Fit(ask.Family, card.Strain.Key);
            // DEC-044: the budget is checked against the POS total the customer pays (the cart with this line), not the card's priceFloor.
            double total = CartPrice(Cart.Append(line).ToList()).PostTax;
            double priceFit = PriceFit(total, c.Budget), speedFit = SpeedFit(Cfg, t), wait = WaitPenalty(Cfg, c.QueueWait);
            return new PresentResult { Fit = fit, PriceFit = priceFit, SpeedFit = speedFit, WaitPenalty = wait,
                Satisfaction = Satisfaction(Cfg, fit, priceFit, speedFit, wait) };
        }

        /// <summary>§3.3; budget 0 = no budget.</summary>
        public static double PriceFit(double price, double budget) =>
            budget <= 0 || price <= budget ? 1 : Math.Max(0, 1 - 2 * (price - budget) / budget);

        /// <summary>§3.3; t = service start → card pick.</summary>
        public static double SpeedFit(SliceConfig cfg, double t) =>
            t <= cfg.fastSeconds ? 1 : Math.Max(0, 1 - (t - cfg.fastSeconds) / (cfg.slowSeconds - cfg.fastSeconds));

        /// <summary>§3.3.</summary>
        public static double WaitPenalty(SliceConfig cfg, double queueWait) =>
            Math.Min(cfg.waitPenaltyCap, cfg.waitPenaltyPerSec * Math.Max(0, queueWait - cfg.waitGraceSeconds));

        /// <summary>§3.4.</summary>
        public static double Satisfaction(SliceConfig cfg, double fit, double priceFit, double speedFit, double waitPenalty) =>
            Math.Round(100 * Clamp01(cfg.wFit * fit + cfg.wPrice * priceFit + cfg.wSpeed * speedFit - waitPenalty), MidpointRounding.AwayFromZero);

        /// <summary>§3.2: Ms / Ms_top against the true family on live stock; relaxed pass × fitRelaxedFactor; else 0.</summary>
        public double Fit(IntentFamily truth, string strainKey)
        {
            var all = new ShopState { ResultCount = int.MaxValue };
            var cat = Data.Catalog;
            var strict = Recommender.FindStrains(cat, truth.Crit, truth.Neg, truth.primary, all);
            var f = Ratio(strict, strainKey);
            if (f.HasValue) return f.Value;
            var crit = truth.Crit.ToDictionary(kv => kv.Key, kv => (int)Math.Floor(kv.Value * EngineConstants.FallbackCritFactor));
            var neg = truth.Neg.ToDictionary(kv => kv.Key, kv => Math.Min(EngineConstants.DisplayMax, kv.Value + EngineConstants.FallbackCapAdd));
            var r = Ratio(Recommender.FindStrains(cat, crit, neg, truth.primary, all), strainKey);
            return r.HasValue ? Cfg.fitRelaxedFactor * r.Value : 0;
        }

        static double? Ratio(List<StrainResult> list, string key)
        {
            int i = list.FindIndex(s => s.Key == key);
            if (i < 0) return null;
            double top = list[0].Ms;
            if (top <= 0) return i == 0 ? 1 : 0;
            return Clamp01(list[i].Ms / top);
        }

        // ---------- report ----------

        public ShiftReport Report()
        {
            var cs = Customers;
            var served = cs.Where(c => c.ServiceStart >= 0 && c.EndTime >= 0).ToList();
            var sold = cs.Where(c => c.Outcome == CustomerOutcome.Bought).ToList();
            var chipped = cs.Where(c => !c.AutoFilled).SelectMany(c => c.Asks).Where(a => a.Chip != null).ToList();
            var r = new ShiftReport
            {
                CustomersServed = sold.Count,
                Walkouts = cs.Count(c => c.Outcome == CustomerOutcome.Walkout),
                NoSales = cs.Count(c => c.Outcome == CustomerOutcome.NoSale),
                RevenuePostTax = Sales.Sum(s => s.PricePostTax),
                RevenuePreTax = Sales.Sum(s => s.PricePreTax),
                GramsSold = Sales.Sum(s => s.Grams),
                AvgServiceSeconds = served.Count > 0 ? served.Average(c => c.EndTime - c.ServiceStart) : 0,
                AvgQueueWaitSeconds = cs.Average(c => c.QueueWait),
                AvgSatisfaction = cs.Average(c => c.Outcome == CustomerOutcome.Walkout ? 0 : Math.Max(0, c.LastSatisfaction)),
                AvgRecFit = sold.Count > 0 ? sold.Average(c => c.LastFit) : 0,
                InterpretationAccuracy = chipped.Count > 0 ? 100.0 * chipped.Count(a => a.Chip == a.Family.id) / chipped.Count : 0,
                UnitsPerSale = sold.Count > 0 ? (double)Sales.Count / sold.Count : 0,
                TopIntents = cs.SelectMany(c => c.Asks).GroupBy(a => a.Family.id).OrderByDescending(g => g.Count()).ToDictionary(g => g.Key, g => g.Count()),
                SoldOut = Inventory.SoldOutIds.Select(Describe).ToList(),
                LowStock = Inventory.JarBatchIds.Where(Inventory.IsLow).Select(Describe).ToList(),
            };
            r.Stars = r.AvgSatisfaction >= Cfg.starCutoff3 ? 3 : r.AvgSatisfaction >= Cfg.starCutoff2 ? 2 : 1;
            r.RoughShift = r.Walkouts + r.NoSales >= Cfg.roughShiftThreshold;
            return r;
        }

        public string Describe(string batchId) => $"{_batches[batchId].StrainName} ({_batches[batchId].BatchCode})";
        public Batch Batch(string id) => _batches[id];

        /// <summary>§6 anxiety label (_anxLevel L16377).</summary>
        public string AnxietyLabel(int risk) =>
            risk < Cfg.anxietyLowBelow ? Data.Lines.anxietyLow : risk < Cfg.anxietyModerateBelow ? Data.Lines.anxietyModerate : Data.Lines.anxietyHigh;

        // ---------- internals ----------

        RecommendResult Recommend(IntentFamily f, int n) =>
            Recommender.Recommend(Data.Catalog, f.Crit, f.Neg, f.primary, new ShopState { ResultCount = n });

        void Append(IEnumerable<StrainResult> strains)
        {
            foreach (var s in strains)
            {
                _seen.Add(s.Key);
                var rep = _batches[s.RepBatchId];
                var price = Price(rep, Serving.Asks[Results.Ask].Grams);
                Results.Cards.Add(new Card
                {
                    Strain = s, Rep = rep,
                    PricePreTax = price?.PreTax ?? double.NaN, PricePostTax = price?.CardPostTax ?? double.NaN,
                    CheckoutPostTax = price?.PostTax ?? double.NaN,
                    TierLabel = Labels.TierLabel(rep.Tier), ClusterLabel = Labels.ClusterLabel(s.Cluster), AnxietyLabel = AnxietyLabel(s.AnxietyRisk),
                });
            }
        }

        void Finish(Customer c, CustomerOutcome outcome)
        {
            c.Outcome = outcome; c.State = CustomerState.Done; c.EndTime = Time;
            Queue.Remove(c);
            if (Serving == c) { Serving = null; Results = null; Cart.Clear(); RegisterOpen = false; }
            Left?.Invoke(c);
        }

        static double Clamp01(double x) => x < 0 ? 0 : x > 1 ? 1 : x;
        static void Require(bool ok, string what) { if (!ok) throw new InvalidOperationException(what); }
    }

    /// <summary>End-of-shift report: every field in SLICE_DESIGN §1. Seconds are sim seconds.</summary>
    public sealed class ShiftReport
    {
        public int CustomersServed, Walkouts, NoSales, Stars;
        public double RevenuePostTax, RevenuePreTax, GramsSold, AvgServiceSeconds, AvgQueueWaitSeconds, AvgSatisfaction, AvgRecFit, InterpretationAccuracy;
        public double UnitsPerSale;   // GAME-006: sale lines per buying customer (real store ≈ 2, RES-001 O13)
        public Dictionary<string, int> TopIntents;
        public List<string> SoldOut, LowStock;
        public bool RoughShift;
    }
}
