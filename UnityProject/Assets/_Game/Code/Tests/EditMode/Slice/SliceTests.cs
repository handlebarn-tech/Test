using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using Dispo.Domain.Engine;
using Dispo.Simulation.Slice;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Slice.Tests
{
    /// <summary>GAME-002 EditMode validation (Docs/Tasks/Active/GAME-002.md).</summary>
    public class SliceTests
    {
        static string Read(string rel) => File.ReadAllText(Path.Combine(Application.dataPath, rel));
        static string Cat(string f) => Read("_Game/Data/Catalog/" + f);

        /// <summary>Fresh data each time: the catalog's stock flags are mutated by sales.</summary>
        static SliceData Load() => SliceData.Load(Cat("batches.json"), Cat("terpenes.json"), Cat("engine_tables.json"), Cat("pricing.json"),
            Read("_Game/Data/Slice/SliceConfig.json"), Read("_Game/Data/Slice/SliceIntents.json"), Read("_Game/Data/Slice/SliceLines.json"));

        static Dictionary<string, object> _golden;
        static Dictionary<string, object> Golden => _golden ?? (_golden = (Dictionary<string, object>)Json.Parse(Read("../../Docs/Reconstruction/golden_cases.json")));
        static Dictionary<string, object> O(object o) => (Dictionary<string, object>)o;
        static List<object> A(object o) => (List<object>)o;
        static Dictionary<string, int> Ints(object o) => O(o).ToDictionary(kv => kv.Key, kv => (int)(double)kv.Value);

        [Test]
        public void Config_JsonHasEveryField()
        {
            var json = O(Json.Parse(Read("_Game/Data/Slice/SliceConfig.json")));
            var missing = typeof(SliceConfig).GetFields().Select(f => f.Name).Where(n => !json.ContainsKey(n)).ToList();
            CollectionAssert.IsEmpty(missing, "SliceConfig.json must set every field (no silent defaults)");
        }

        [Test]
        public void Intents_EachRowEqualsGoldenParse()
        {
            var d = Load();
            Assert.AreEqual(6, d.Intents.families.Length);
            foreach (var f in d.Intents.families)
            {
                var parsed = O(A(Golden["cases"]).Select(O).Single(c => (string)c["id"] == f.rc)["parsed"]);
                CollectionAssert.AreEquivalent(Ints(parsed["crit"]), f.Crit, f.id + " crit");
                CollectionAssert.AreEquivalent(Ints(parsed["neg"]), f.Neg, f.id + " neg");
                Assert.AreEqual(parsed["primary"], f.primary, f.id + " primary");
                Assert.AreEqual(A(parsed["lbls"]).Single(), f.lbl, f.id + " lbl");
            }
            CollectionAssert.AreEquivalent(d.Intents.families.Select(f => f.id), d.Config.familyWeights.Select(w => w.id));
        }

        static readonly string[] Banned = { "night", "relax", "chill", "work", "drive", "focus", "first time", "never tried", "heavy" };
        static bool HasWord(string line, string w) => Regex.IsMatch(line, "(?<![a-z])" + Regex.Escape(w) + "(?![a-z])");

        [Test]
        public void Lines_EveryTemplateVariant_PassesIntentKeySafety()
        {
            var d = Load();
            var keys = d.Catalog.Intents.Keys.ToList();
            int n = 0;
            foreach (var arch in d.Config.archetypes)
            foreach (var opener in d.Lines.Openers(arch.id))
            foreach (var f in d.Intents.families)
            foreach (var core in f.cores)
            foreach (var w in d.Config.weightOdds)
            foreach (var budget in arch.hasBudget ? d.Config.budgetPerGram.Select(b => System.Math.Floor(w.g * b)) : new[] { 0.0 })
            {
                var line = CustomerGenerator.RenderLine(d.Lines, opener, core, w.g, budget).ToLowerInvariant();
                Assert.IsTrue(HasWord(line, f.keyword), $"'{line}' lacks its keyword {f.keyword}");
                var bad = keys.Where(k => k != f.keyword && HasWord(line, k)).Concat(Banned.Where(b => HasWord(line, b))).ToList();
                CollectionAssert.IsEmpty(bad, $"'{line}' ({f.id})");
                n++;
            }
            Assert.Greater(n, 100);
        }

        [Test]
        public void Generator_SameSeed_SameCustomers()
        {
            string Dump(ShiftSim s) => string.Join("\n", s.Customers.Select(c =>
                $"{c.Index}|{c.SpawnTime}|{c.Archetype.id}|{c.TrueFamily.id}|{c.Grams}|{c.Budget}|{c.PatienceMax}|{c.Line}"));
            var a = new ShiftSim(Load());
            var b = new ShiftSim(Load());
            Assert.AreEqual(Dump(a), Dump(b));
            Assert.AreEqual(16, a.Customers.Count, "GAME-010: 16 per shift");
            CollectionAssert.AreEqual(a.Inventory.StartGrams, b.Inventory.StartGrams);
            Assert.AreEqual(0, a.Customers[0].SpawnTime);
            Assert.AreEqual(4 * 150 + 4 * 60 + 7 * 150, a.Customers[15].SpawnTime, "150 s gaps, 60 s gaps before customers 6-9 (GAME-010)");
            Assert.IsTrue(a.Customers.Where(c => c.Rush).Select(c => c.Index).SequenceEqual(new[] { 6, 7, 8, 9 }));
            Assert.IsTrue(a.Customers.All(c => c.HasBudget == c.Archetype.hasBudget));
        }

        [Test]
        public void Inventory_StartFills_FollowDec027()
        {
            var d = Load();
            var inv = new ShiftSim(d).Inventory;
            var c = d.Config;
            Assert.AreEqual(d.Catalog.Batches.Count(b => b.InStock), inv.JarBatchIds.Count);
            foreach (var g in inv.StartGrams.Values)
            {
                Assert.GreaterOrEqual(g, c.startFillMin * c.startGramsPerBatch - 3.5);
                Assert.LessOrEqual(g, c.startFillMax * c.startGramsPerBatch);
                Assert.AreEqual(0, g % 3.5, 1e-9, "start grams are whole 3.5 g units");
            }
            Assert.GreaterOrEqual(inv.JarBatchIds.Count(inv.IsLow), c.minLowStartJars);
        }

        [Test]
        public void Scoring_SanityRows()
        {
            var cfg = Load().Config;
            Assert.AreEqual(100, ShiftSim.Satisfaction(cfg, 1, 1, 1, 0), "exact top pick, no budget, fast, no wait");
            Assert.AreEqual(40, ShiftSim.Satisfaction(cfg, 0, 1, 1, 0), "wrong family");
            Assert.Less(40, cfg.acceptThreshold + 0.0, "→ REJECT");
            Assert.AreEqual(52, ShiftSim.Satisfaction(cfg, 0.2, 1, 1, 0), "fit 0.2 alone");
            Assert.GreaterOrEqual(52, cfg.acceptThreshold, "→ ACCEPT");
        }

        [Test]
        public void Scoring_PriceSpeedWait()
        {
            var cfg = Load().Config;
            Assert.AreEqual(1, ShiftSim.PriceFit(20, 0), "no budget");
            Assert.AreEqual(1, ShiftSim.PriceFit(14, 14));
            Assert.AreEqual(0.5, ShiftSim.PriceFit(17.5, 14), 1e-9);
            Assert.AreEqual(0, ShiftSim.PriceFit(30, 14));
            Assert.AreEqual(1, ShiftSim.SpeedFit(cfg, 20));
            Assert.AreEqual(0.5, ShiftSim.SpeedFit(cfg, 55), 1e-9);
            Assert.AreEqual(0, ShiftSim.SpeedFit(cfg, 200));
            Assert.AreEqual(0, ShiftSim.WaitPenalty(cfg, 60));
            Assert.AreEqual(0.02, ShiftSim.WaitPenalty(cfg, 70), 1e-9);
            Assert.AreEqual(0.30, ShiftSim.WaitPenalty(cfg, 1000), 1e-9);
            Assert.AreEqual(0, ShiftSim.Satisfaction(cfg, 0, 0, 0, 0.3), "clamped at 0");
        }

        [Test]
        public void Fit_TopOfTrueFamily_IsOne_WrongFamily_IsLower()
        {
            var sim = new ShiftSim(Load());
            var d = sim.Data;
            var sleep = d.Intents.Get("sleep");
            var top = Recommender.FindStrains(d.Catalog, sleep.Crit, sleep.Neg, sleep.primary, new ShopState { ResultCount = 3 });
            Assert.AreEqual(1, sim.Fit(sleep, top[0].Key), 1e-9);
            Assert.LessOrEqual(sim.Fit(sleep, top[1].Key), 1);
            var energy = d.Intents.Get("energy");
            var eTop = Recommender.FindStrains(d.Catalog, energy.Crit, energy.Neg, energy.primary, new ShopState { ResultCount = 1 })[0];
            Assert.Less(sim.Fit(sleep, eTop.Key), 0.5, "an energy strain is a poor sleep fit");
        }

        /// <summary>Serve customer 1 with its true family; budget removed so card 1 is accepted.</summary>
        static (ShiftSim sim, Card card) AcceptedSale()
        {
            var sim = new ShiftSim(Load());
            sim.Tick(0);
            var c = sim.Serving;
            c.Budget = 0;
            var r = sim.Search(c.TrueFamily);
            var card = r.Cards.First(x => sim.Inventory.Grams(x.Rep.Id) >= c.Grams);
            Assert.AreEqual(Response.Accept, sim.Present(card).Response);
            return (sim, card);
        }

        [Test]
        public void Sale_DecrementsOnce_CancelChangesNothing()
        {
            var (sim, card) = AcceptedSale();
            var id = card.Rep.Id;
            var c = sim.Serving;
            double g0 = sim.Inventory.Grams(id);
            int events = 0;
            sim.Inventory.Sold += _ => events++;

            sim.Cancel();
            Assert.AreEqual(g0, sim.Inventory.Grams(id), "cancel");
            Assert.IsNull(sim.Pending);
            Assert.AreEqual(Response.Accept, sim.Present(card).Response);
            double wrong = sim.Cfg.weightOdds.Select(w => w.g).First(g => g != c.Grams);
            StringAssert.StartsWith("I asked for", sim.Confirm(wrong));
            Assert.AreEqual(g0, sim.Inventory.Grams(id), "blocked confirm");

            Assert.IsNull(sim.Confirm(c.Grams));
            Assert.AreEqual(g0 - c.Grams, sim.Inventory.Grams(id), 1e-9);
            Assert.AreEqual(1, events);
            Assert.AreEqual(1, sim.Sales.Count);
            Assert.AreEqual(CustomerOutcome.Bought, c.Outcome);
            Assert.IsNull(sim.Serving);
        }

        [Test]
        public void Pos_BlocksWhenJarHasLessThanRequest()
        {
            var (sim, card) = AcceptedSale();
            var id = card.Rep.Id;
            var c = sim.Serving;
            // Another sale leaves 3.5 g less than the request in the jar.
            sim.Inventory.Sell(new SaleEvent { BatchId = id, Grams = sim.Inventory.Grams(id) - (c.Grams - 3.5) });
            double g = sim.Inventory.Grams(id);
            Assert.AreEqual(sim.Data.Lines.notEnough, sim.Confirm(c.Grams));
            Assert.AreEqual(g, sim.Inventory.Grams(id));
            sim.Cancel();
            Assert.AreEqual(Response.Blocked, sim.Present(card).Response, "present is blocked too");
        }

        [Test]
        public void SoldOutBatch_NeverReturned_StrainKeepsNextBatchAsRep()
        {
            var sim = new ShiftSim(Load());
            var cat = sim.Data.Catalog;
            var group = cat.Groups().First(g => g.Batches.Count(b => b.InStock) >= 2);
            var rep = group.Batches[0];
            var next = group.Batches[1];
            var before = Recommender.AnalyzeGroup(cat, group).Profile;

            sim.Inventory.Sell(new SaleEvent { BatchId = rep.Id, Grams = sim.Inventory.Grams(rep.Id) });
            Assert.IsTrue(sim.Inventory.IsSoldOut(rep.Id));
            Assert.IsFalse(rep.InStock);

            var all = Recommender.FindStrains(cat, new Dictionary<string, int>(), new Dictionary<string, int>(), null, new ShopState { ResultCount = int.MaxValue });
            Assert.IsFalse(all.Any(s => s.RepBatchId == rep.Id), "a 0 g batch is never a rep");
            var s2 = all.Single(s => s.Key == group.Key);
            Assert.AreEqual(next.Id, s2.RepBatchId, "the next in-stock batch becomes rep");
            var g2 = cat.Groups().Single(g => g.Key == group.Key);
            CollectionAssert.AreEqual(Scoring.AverageProfile(g2.Batches.Where(b => b.InStock).ToList()), s2.Profile, "re-averaged from what is left");
            CollectionAssert.AreNotEqual(before, s2.Profile);
        }

        [Test]
        public void Prices_MatchGoldenPricingTable_ForShiftDay()
        {
            var sim = new ShiftSim(Load());
            int dow = sim.Cfg.shiftDayOfWeek, n = 0;
            foreach (var tier in O(Golden["pricing"]))
            foreach (var day in A(tier.Value).Select(O).Where(x => (int)(double)x["dow"] == dow))
            foreach (var row in A(day["rows"]).Select(A))
            {
                var p = sim.Price(new Batch { Tier = tier.Key == "(none)" ? "" : tier.Key }, (double)row[0]);
                if ((double)row[1] == 0) { Assert.IsNull(p, "no tier → no price"); continue; }
                Assert.AreEqual((double)row[1], p.PreTax, 1e-9, $"{tier.Key} {row[0]} g pre");
                Assert.AreEqual((double)row[2], p.CardPostTax, 1e-9, $"{tier.Key} {row[0]} g card (tool priceFloor)");
                Assert.AreEqual(ShiftSim.CheckoutRound(p.PreTax * 1.251), p.PostTax, 1e-9, "POS total, nearest $0.05");
                Assert.AreEqual(p.PostTax, p.PreTax + p.Tax, 1e-9);
                n++;
            }
            Assert.Greater(n, 8);
        }

        [Test]
        public void Pos_RoundsToNearestNickel_CardsKeepPriceFloor()
        {
            var sim = new ShiftSim(Load());
            var p = sim.Price(new Batch { Tier = "house" }, 3.5);   // Tue: $10.50 × 1.251 = $13.1355
            Assert.AreEqual(13.10, p.CardPostTax, 1e-9, "card: floor to $0.05 (v7.11.4)");
            Assert.AreEqual(13.15, p.PostTax, 1e-9, "POS: nearest $0.05 (DEC-035)");
            Assert.AreEqual(p.PostTax - p.PreTax, p.Tax, 1e-9);
            Assert.AreEqual(8.75, ShiftSim.CheckoutRound(8.757), 1e-9);
            Assert.AreEqual(8.80, ShiftSim.CheckoutRound(8.775), 1e-9, "half rounds up");
        }

        [Test]
        public void Pos_BlocksOverAdultUseLimit_AllowsOneOunce()
        {
            var cfg = Load().Config;
            Assert.AreEqual(28.0, cfg.adultUseLimitGrams, "A.R.S. 36-2858(A)(1)(c)");
            var (sim, card) = AcceptedSale();
            var c = sim.Serving;
            double g0 = sim.Inventory.Grams(card.Rep.Id);
            c.Grams = 28.5;
            Assert.AreEqual(sim.Data.Lines.overLimit, sim.Confirm(28.5));
            Assert.AreEqual(g0, sim.Inventory.Grams(card.Rep.Id), "blocked sale changes nothing");
            Assert.AreEqual(0, sim.Sales.Count);

            // 28 g passes: serve a fresh customer with a jar that holds an ounce.
            var sim2 = new ShiftSim(Load());
            sim2.Tick(0);
            var c2 = sim2.Serving;
            c2.Budget = 0; c2.Grams = 28;
            var k = sim2.Search(c2.TrueFamily).Cards.First(x => sim2.Inventory.Grams(x.Rep.Id) >= 28);
            Assert.AreEqual(Response.Accept, sim2.Present(k).Response);
            Assert.IsNull(sim2.Confirm(28));
            Assert.AreEqual(28, sim2.Sales.Single().Grams);
        }

        [Test]
        public void ShiftClock_InsideStoreHours()
        {
            var d = Load();
            var cfg = d.Config;
            Assert.AreEqual(8, cfg.storeOpenHour);
            Assert.AreEqual(22, cfg.storeCloseHour);
            var sim = RunBot(d, 0.5);
            Assert.GreaterOrEqual(cfg.shiftStartHour, cfg.storeOpenHour);
            Assert.LessOrEqual(sim.ClockHours, cfg.storeCloseHour, "the bot shift ends before close");
            // Worst case: every customer waits out full patience and then the slowest service.
            double worst = sim.Customers.Max(c => c.SpawnTime) + (cfg.archetypes.Max(a => a.patienceSec) + cfg.slowSeconds) * cfg.customersPerShift;
            Assert.LessOrEqual(cfg.shiftStartHour + worst / 3600, cfg.storeCloseHour);
        }

        /// <summary>REVIEW-W3A n1: SetInStock must also reset Group(key) and the parser's per-catalog caches.</summary>
        [Test]
        public void SellOut_ResetsGroupLookupAndParserCaches()
        {
            var cat = Catalog.Load(Cat("batches.json"), Cat("terpenes.json"), Cat("engine_tables.json"), Cat("pricing.json"), Cat("parser_tables.json"));
            var group = cat.Groups().First(g => g.Batches.Count(b => b.InStock) >= 2);
            var rep = group.Batches[0];
            // Warm every cache first.
            Assert.AreEqual(rep.Id, cat.Group(group.Key).Batches[0].Id);
            var before = Dispo.Domain.Engine.QueryParser.Parse(cat, group.Name.ToLowerInvariant());
            Assert.AreEqual(group.Key, before.GroupKey, "parser finds the strain by name");
            Dispo.Domain.Engine.QueryParser.ExtractExclusions(cat, "no myrcene");

            cat.SetInStock(rep.Id, false);

            var g2 = cat.Group(group.Key);
            Assert.AreNotSame(group, g2, "Group(key) rebuilt, not the cached group");
            Assert.AreNotEqual(rep.Id, g2.Batches[0].Id, "sold-out batch is no longer the rep");
            Assert.IsTrue(g2.Batches[0].InStock);
            var after = Dispo.Domain.Engine.QueryParser.Parse(cat, group.Name.ToLowerInvariant());
            Assert.AreEqual(group.Key, after.GroupKey);
            Assert.AreNotEqual(rep.Id, cat.Group(after.GroupKey).Batches[0].Id, "parser lookup lands on an in-stock batch");
            Assert.IsNotEmpty(Dispo.Domain.Engine.QueryParser.ExtractExclusions(cat, "no myrcene").Excl, "exclusion cache rebuilds");
        }

        /// <summary>DEC-044: PriceFit uses the POS total (nearest $0.05), not the card's priceFloor.</summary>
        [Test]
        public void PriceFit_UsesPosTotal_NotCardFloor()
        {
            var sim = new ShiftSim(Load());
            sim.Tick(0);
            var c = sim.Serving;
            c.Grams = 14;   // 14 g smalls Tue: $28 × 1.251 = $35.028 → card $35.00, POS $35.05
            var cards = sim.Search(c.TrueFamily).Cards;
            foreach (var k in cards) Assert.AreEqual(sim.Price(k.Rep, c.Grams).PostTax, k.CheckoutPostTax, 1e-9, "card carries the POS total");
            var card = cards.FirstOrDefault(k => k.CheckoutPostTax > k.PricePostTax && sim.Inventory.Grams(k.Rep.Id) >= c.Grams);
            Assume.That(card, Is.Not.Null, "needs a card whose POS total rounds up");
            c.Budget = card.PricePostTax;   // affordable at the card price, 5 cents short at the register
            var r = sim.Present(card);
            Assert.AreEqual(ShiftSim.PriceFit(card.CheckoutPostTax, c.Budget), r.PriceFit, 1e-12);
            Assert.Less(r.PriceFit, 1);
        }

        [Test]
        public void MoreOptions_BlockedWhilePosOpen()
        {
            var (sim, _) = AcceptedSale();
            Assert.IsNotNull(sim.Pending);
            Assert.Throws<System.InvalidOperationException>(() => sim.MoreOptions());
            sim.Cancel();
            Assert.DoesNotThrow(() => sim.MoreOptions());
        }

        [Test]
        public void Labels_ClusterAndTier_FromSource()
        {
            Assert.AreEqual("Anxiety / Mental Calm", Labels.ClusterLabel(6));
            Assert.AreEqual("House Smalls", Labels.TierLabel("smalls"));
            Assert.AreEqual("", Labels.TierLabel(null));
        }

        /// <summary>Pure-sim version of the PlayMode bot: per ask, true-family chip, card 1 (next card if the jar is short), stated weight;
        /// Add item while an ask is open (GAME-006), then confirm the cart.</summary>
        public static ShiftSim RunBot(SliceData d, double step)
        {
            var sim = new ShiftSim(d);
            for (int guard = 0; !sim.IsOver; guard++)
            {
                Assert.Less(guard, 100000, "shift never ended");
                sim.Tick(step);
                var c = sim.Serving;
                if (c == null) continue;
                if (sim.RegisterOpen)
                {
                    // GAME-007: trim an over-limit cart (drop the last line); add the next ask only if it fits under the cap.
                    if (sim.Meter == MeterState.Red) { sim.RemoveLine(sim.Cart.Count - 1); continue; }
                    if (sim.CanAddItem && sim.CartGrams + sim.CurrentAsk.Grams <= sim.Cfg.adultUseLimitGrams) sim.AddItem();
                    else { Assert.IsNull(sim.Confirm()); continue; }
                }
                var ask = sim.CurrentAsk;
                var r = sim.Results ?? sim.Search(ask.Family);
                var card = r.Cards.FirstOrDefault(x => sim.Free(x.Rep.Id) >= ask.Grams);
                Assert.IsNotNull(card, $"customer {c.Index}: no card can fill {ask.Grams} g");
                sim.Present(card);
            }
            return sim;
        }

        [Test]
        public void SimBot_Seed1_ResolvesAll_ReportComplete_SellsOut()
        {
            var sim = RunBot(Load(), 0.5);
            var r = sim.Report();
            foreach (var s in sim.Sales) Debug.Log($"[SliceBot] sale c{s.CustomerIndex} {sim.Customers[s.CustomerIndex - 1].TrueFamily.id} {s.StrainName} {s.BatchId} {s.Grams} g {s.GramsBefore}->{s.GramsAfter} start {sim.Inventory.StartGrams[s.BatchId]}");
            Debug.Log($"[SliceBot] served={r.CustomersServed} walkouts={r.Walkouts} noSales={r.NoSales} revenue={r.RevenuePostTax} soldOut={string.Join(",", r.SoldOut)} low={r.LowStock.Count} sat={r.AvgSatisfaction} stars={r.Stars}");
            Assert.IsTrue(sim.Customers.All(c => c.Outcome != CustomerOutcome.None));
            Assert.AreEqual(sim.Cfg.customersPerShift, r.CustomersServed + r.Walkouts + r.NoSales);
            Assert.AreEqual(sim.Sales.Sum(s => s.PricePostTax), r.RevenuePostTax, 1e-9);
            Assert.IsTrue(typeof(ShiftReport).GetFields().All(f => f.GetValue(r) != null), "no null report fields");
            CollectionAssert.IsNotEmpty(r.SoldOut, "DEC-027: the seed-1 bot shift shows at least one SOLD OUT");
        }

        [Test]
        public void JarFillStep_NearestStep_TiesUp_MinVisible()
        {
            var steps = new[] { 0, 10, 20, 40, 70, 100 };
            Assert.AreEqual(0, JarFillStep.For(0, steps, 20), "0 g = SOLD OUT");
            Assert.AreEqual(20, JarFillStep.For(0.01, steps, 20), "DEC-046: above 0 g shows the min visible step");
            Assert.AreEqual(10, JarFillStep.For(0.01, steps, 10));
            Assert.AreEqual(20, JarFillStep.For(0.15, steps, 10), "tie 10/20 goes up");
            Assert.AreEqual(70, JarFillStep.For(0.55, steps, 20), "tie 40/70 goes up");
            Assert.AreEqual(40, JarFillStep.For(0.5, steps, 20));
            Assert.AreEqual(100, JarFillStep.For(451.5 / 454, steps, 20), "a 451.5 g jar reads full");
        }
    }
}
