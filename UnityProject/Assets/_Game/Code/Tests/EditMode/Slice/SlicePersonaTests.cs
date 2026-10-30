using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Dispo.Simulation.Slice;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Slice.Tests
{
    /// <summary>A QA budtender bot (GAME-010). Timings are [GDD] bot pacing, not game config.</summary>
    public sealed class Persona
    {
        public string Name;
        public bool TrueChip, BestCard;           // perfect information vs a random chip and a random card
        public double PickSec, PosSec, RepickSec; // service start → first card, accept → POS confirm, reject → next card

        public static readonly Persona Perfect = new Persona { Name = "perfect", TrueChip = true, BestCard = true, PickSec = 45, PosSec = 30, RepickSec = 15 };
        public static readonly Persona Careless = new Persona { Name = "careless", PickSec = 45, PosSec = 30, RepickSec = 15 };
        public static readonly Persona Slow = new Persona { Name = "slow", TrueChip = true, BestCard = true, PickSec = 90, PosSec = 60, RepickSec = 30 };
        public static readonly Persona[] All = { Perfect, Careless, Slow };
    }

    /// <summary>GAME-010: pure-sim persona bots and the seed sweep behind Docs/Design/TUNING_PS1.md.</summary>
    public class SlicePersonaTests
    {
        static readonly Dictionary<string, string> Texts = new Dictionary<string, string>();
        static string Read(string rel) =>
            Texts.TryGetValue(rel, out var t) ? t : Texts[rel] = File.ReadAllText(Path.Combine(Application.dataPath, "_Game/Data/" + rel));

        /// <summary>Fresh data each run: sales mutate the catalog's stock flags.</summary>
        public static SliceData Load() => SliceData.Load(Read("Catalog/batches.json"), Read("Catalog/terpenes.json"), Read("Catalog/engine_tables.json"),
            Read("Catalog/pricing.json"), Read("Slice/SliceConfig.json"), Read("Slice/SliceIntents.json"), Read("Slice/SliceLines.json"));

        /// <summary>Plays one seeded shift through the cart (GAME-006): per ask search, present, then Add item; Confirm when every ask
        /// is in. Perfect picks the card with the best fit + price (cards 1-3 plus one More options page); careless picks a random chip
        /// and a random card, blind to budget. Both sell the stated weights.</summary>
        public static ShiftSim Run(SliceData d, Persona p, int seed, double step = 0.5)
        {
            d.Config.seed = seed;
            var sim = new ShiftSim(d);
            var rng = new System.Random(seed * 7919 + p.Name.Length);
            Customer cur = null;
            double next = 0;
            var tried = new HashSet<string>();
            for (int guard = 0; !sim.IsOver; guard++)
            {
                Assert.Less(guard, 400000, $"{p.Name} seed {seed}: shift never ended");
                sim.Tick(step);
                var c = sim.Serving;
                if (c == null) continue;
                if (c != cur) { cur = c; tried.Clear(); next = c.ServiceStart + p.PickSec; }
                if (sim.Time < next) continue;
                if (sim.RegisterOpen)
                {
                    // GAME-007 trim rule: perfect/slow drop the last line of a red cart and add an ask only if it fits under the cap;
                    // careless ignores the limit, so a blocked over-limit cart ends in Cancel = the customer refuses (no sale).
                    bool fits = p.TrueChip ? sim.CurrentAsk != null && sim.CartGrams + sim.CurrentAsk.Grams <= sim.Cfg.adultUseLimitGrams : true;
                    if (p.TrueChip && sim.Meter == MeterState.Red) sim.RemoveLine(sim.Cart.Count - 1);
                    else if (sim.CanAddItem && fits) { sim.AddItem(); tried.Clear(); next = sim.Time + p.PickSec; }
                    else if (sim.Confirm() is string blocked) { Assert.IsFalse(p.TrueChip, $"{p.Name} seed {seed} customer {c.Index}: {blocked}"); sim.Cancel(); }
                    continue;
                }
                var card = Choose(sim, p, rng, tried);
                tried.Add(card.Strain.Key);
                var r = sim.Present(card).Response;
                next = sim.Time + (r != Response.Accept ? p.RepickSec : sim.CanAddItem ? 0 : p.PosSec);
            }
            return sim;
        }

        static Card Choose(ShiftSim sim, Persona p, System.Random rng, HashSet<string> tried)
        {
            var c = sim.Serving;
            var ask = sim.CurrentAsk;
            bool Ok(Card k) => k.HasPrice && !tried.Contains(k.Strain.Key) && sim.Free(k.Rep.Id) >= ask.Grams;
            var fams = sim.Data.Intents.families;
            double inCart = sim.Cart.Count > 0 ? sim.CartPrice().PostTax : 0;
            for (int attempt = 0; attempt < 20; attempt++)
            {
                if (sim.Results == null || attempt > 0)
                {
                    sim.Search(p.TrueChip ? ask.Family : fams[rng.Next(fams.Length)]);
                    if (p.BestCard && sim.Results.MoreAvailable) sim.MoreOptions();
                }
                var ok = sim.Results.Cards.Where(Ok).ToList();
                if (ok.Count == 0) { Assert.IsFalse(p.TrueChip, $"customer {c.Index}: no card can fill {ask.Grams} g"); continue; }
                if (!p.BestCard) return ok[rng.Next(ok.Count)];
                var cfg = sim.Cfg;
                return ok.OrderByDescending(k => cfg.wFit * sim.Fit(ask.Family, k.Strain.Key) + cfg.wPrice * ShiftSim.PriceFit(inCart + k.CheckoutPostTax, c.Budget)).First();
            }
            Assert.Fail($"customer {c.Index}: no chip gave a fillable card");
            return null;
        }

        public static List<ShiftReport> Sweep(Persona p, int seeds = 20) =>
            Enumerable.Range(1, seeds).Select(s => Run(Load(), p, s).Report()).ToList();

        static string Row(Persona p, List<ShiftReport> rs) =>
            $"{p.Name,-8} avg {rs.Average(r => r.AvgSatisfaction),5:0.0}  walkouts {rs.Average(r => r.Walkouts):0.0}  noSales {rs.Average(r => r.NoSales):0.0}  units/sale {rs.Average(r => r.UnitsPerSale):0.00}";

        /// <summary>Deliverable 3: seeds 1-20 per persona; prints the table in TUNING_PS1.md. Explicit: about 75 s, run on purpose
        /// (-testFilter Dispo.Slice.Tests.SlicePersonaTests.Sweep_Seeds1To20). Asserts the bands this tuning reaches (see TUNING_PS1.md).</summary>
        [Test, Explicit, Category("Balance"), Timeout(1800000)]
        public void Sweep_Seeds1To20()
        {
            var avg = new Dictionary<string, double>();
            foreach (var p in Persona.All)
            {
                var rs = Sweep(p);
                avg[p.Name] = rs.Average(r => r.AvgSatisfaction);
                Debug.Log("[Balance] " + Row(p, rs));
            }
            Assert.That(avg["perfect"], Is.InRange(80, 95), "perfect band");
            Assert.Greater(avg["perfect"], avg["slow"]);
            Assert.Greater(avg["perfect"], avg["careless"]);
        }

        /// <summary>PS1 exit test, part 1 (ROADMAP_POST_SLICE §2): a perfect-information bot scores &lt; 100 on a seeded 16-customer shift.</summary>
        [Test]
        public void PerfectBot_Seed1_Below100_BeatsCarelessAndSlow()
        {
            var r = Persona.All.ToDictionary(p => p.Name, p => Run(Load(), p, 1).Report());
            foreach (var p in Persona.All) Debug.Log("[Balance] seed 1 " + Row(p, new List<ShiftReport> { r[p.Name] }));
            Assert.AreEqual(16, r["perfect"].CustomersServed + r["perfect"].Walkouts + r["perfect"].NoSales);
            Assert.Less(r["perfect"].AvgSatisfaction, 100, "tension: a perfect player no longer maxes every customer");
            Assert.Greater(r["perfect"].AvgSatisfaction, r["careless"].AvgSatisfaction);
            Assert.Greater(r["perfect"].AvgSatisfaction, r["slow"].AvgSatisfaction);
        }

        /// <summary>PS1 exit test, part 2: a careless bot gets ≥ 1 strike. GAME-007 has the ledger but no strike source (an over-limit
        /// sale is impossible); GAME-008 (ID checks) adds the first. Remove the Ignore there.</summary>
        [Test, Ignore("GAME-008 adds the first strike source")]
        public void CarelessBot_GetsAStrike()
        {
            Assert.GreaterOrEqual(Run(Load(), Persona.Careless, 1).Report().Strikes.Count, 1);
        }

        /// <summary>PS1 hook (GAME-007): over-limit customers on seed 1 are trimmed to a legal sale by perfect, with no strike;
        /// careless, blind to the limit, loses them (Cancel on a red cart = refusal, no sale).</summary>
        [Test]
        public void OverLimit_PerfectTrims_CarelessLosesTheSale()
        {
            var d = Load();
            Assert.Greater(d.Config.overLimitAskChance, 0);
            var perfect = Run(Load(), Persona.Perfect, 1);
            var over = perfect.Customers.Where(c => c.OverLimit).ToList();
            Assert.IsNotEmpty(over, "seed 1 shows the over-limit feature (REVIEW-W5G m4)");
            var r = perfect.Report();
            Assert.AreEqual(over.Count(c => c.Outcome == CustomerOutcome.Bought), r.OverLimitTrims);
            Assert.IsEmpty(r.Strikes);
            Assert.IsTrue(perfect.Sales.GroupBy(x => x.CustomerIndex).All(g => g.Sum(x => x.Grams) <= d.Config.adultUseLimitGrams));
            var careless = Run(Load(), Persona.Careless, 1);
            Assert.AreEqual(0, careless.Report().OverLimitTrims);
            Debug.Log($"[Balance] seed 1 over-limit customers {over.Count}: perfect trims {r.OverLimitTrims}, careless outcomes "
                + string.Join(",", careless.Customers.Where(c => c.OverLimit).Select(c => c.Outcome)));
        }

        /// <summary>The tuning grid behind TUNING_PS1.md. Explicit: minutes per config; edit the axes, run on purpose.</summary>
        [Test, Explicit, Category("Explore"), Timeout(3000000)]
        public void Explore_TuningGrid()
        {
            foreach (var gap in new[] { 150.0 })
            foreach (var rush in new[] { 40.0, 60.0 })
            {
                var cells = Persona.All.Select(p => Row(p, Enumerable.Range(1, 20).Select(s =>
                {
                    var d = Load();
                    d.Config.arrivalGapNormalSec = gap; d.Config.arrivalGapRushSec = rush;
                    return Run(d, p, s).Report();
                }).ToList()));
                Debug.Log($"[Tuning] gap {gap}/{rush}: " + string.Join(" | ", cells));
            }
        }
    }
}
