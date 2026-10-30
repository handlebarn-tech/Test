using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using Dispo.Simulation.Slice;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Slice.Tests
{
    /// <summary>GAME-007: limit meter, over-limit asks and trims, strike ledger (Docs/Tasks/Active/GAME-007.md).</summary>
    public class OverLimitTests
    {
        static string Read(string rel) => File.ReadAllText(Path.Combine(Application.dataPath, rel));
        static string Cat(string f) => Read("_Game/Data/Catalog/" + f);
        static SliceData Load() => SliceData.Load(Cat("batches.json"), Cat("terpenes.json"), Cat("engine_tables.json"), Cat("pricing.json"),
            Read("_Game/Data/Slice/SliceConfig.json"), Read("_Game/Data/Slice/SliceIntents.json"), Read("_Game/Data/Slice/SliceLines.json"));

        /// <summary>Customer 1 asks SPEC_COMP002 §2 shape <paramref name="shape"/> of its true family, no budget; every ask is accepted.</summary>
        static ShiftSim Cart(int shape)
        {
            var sim = new ShiftSim(Load());
            sim.Tick(0);
            var c = sim.Serving;
            var f = c.TrueFamily;
            c.Asks = CustomerGenerator.OverLimitAsks(sim.Data.Lines, shape, f, f.cores[0], f, f.cores[0], f, f.cores[0], out _);
            c.OverLimit = true; c.Budget = 0;
            for (int i = 0; i < c.Asks.Count; i++)
            {
                if (sim.RegisterOpen) sim.AddItem();
                var ask = sim.CurrentAsk;
                var card = sim.Search(ask.Family).Cards.First(k => sim.Free(k.Rep.Id) >= ask.Grams);
                Assert.AreEqual(Response.Accept, sim.Present(card).Response);
            }
            return sim;
        }

        static double[] Stock(ShiftSim sim) => sim.Inventory.JarBatchIds.Select(sim.Inventory.Grams).ToArray();

        [Test]
        public void EachAskShape_IsOverTheCap()
        {
            var d = Load();
            var f = d.Intents.families[0];
            for (int shape = 0; shape < CustomerGenerator.ShapeGrams.Length; shape++)
            {
                var asks = CustomerGenerator.OverLimitAsks(d.Lines, shape, f, f.cores[0], f, f.cores[0], f, f.cores[0], out var spoken);
                Assert.AreEqual(CustomerGenerator.ShapeGrams[shape], asks.Sum(a => a.Grams), $"shape {shape}");
                Assert.Greater(asks.Sum(a => a.Grams), d.Config.adultUseLimitGrams, $"shape {shape} is over 1 oz");
                Assert.IsTrue(asks.All(a => d.Catalog.Pricing.Weights.Contains(a.Grams)), "every ask is a priced weight");
                CollectionAssert.IsNotEmpty(spoken);
            }
            // The generator makes them: at chance 1 every customer is over the cap and all three shapes appear.
            d.Config.overLimitAskChance = 1;
            var cs = new ShiftSim(d).Customers;
            Assert.IsTrue(cs.All(c => c.OverLimit && c.Asks.Sum(a => a.Grams) > d.Config.adultUseLimitGrams));
            CollectionAssert.AreEquivalent(CustomerGenerator.ShapeGrams, cs.Select(c => c.Asks.Sum(a => a.Grams)).Distinct());
            StringAssert.Contains(d.Lines.twoOunces, cs.First(c => c.Asks.Sum(a => a.Grams) == 56).Line);
        }

        static bool HasWord(string line, string w) => Regex.IsMatch(line, "(?<![a-z])" + Regex.Escape(w) + "(?![a-z])");

        [Test]
        public void OverLimitLines_PassIntentKeySafety()
        {
            var d = Load();
            var keys = d.Catalog.Intents.Keys.ToList();
            foreach (var x in d.Intents.families)
            foreach (var y in d.Intents.families)
            for (int shape = 0; shape < 3; shape++)
            {
                var cy = y.cores.First(c => !c.Contains('.'));
                CustomerGenerator.OverLimitAsks(d.Lines, shape, x, x.cores[0], y, cy, y, cy, out var spoken);
                var line = CustomerGenerator.Say(d.Lines, d.Lines.Openers("regular")[0], spoken, 0).ToLowerInvariant();
                var bad = keys.Where(k => k != x.keyword && k != y.keyword && HasWord(line, k)).ToList();
                CollectionAssert.IsEmpty(bad, line);
            }
        }

        [Test]
        public void Meter_NeutralAmberRed()
        {
            var sim = Cart(0);   // 28 + 3.5
            Assert.AreEqual(31.5 / 28, sim.MeterFraction, 1e-9);
            Assert.AreEqual(MeterState.Red, sim.Meter);
            sim.RemoveLine(1);
            Assert.AreEqual(MeterState.Amber, sim.Meter, "28 g = 100 %: amber, not red");
            sim.SetLineGrams(0, 14);
            Assert.AreEqual(MeterState.Neutral, sim.Meter, "14 g = 50 %");
            Assert.AreEqual(0.75, sim.Cfg.meterAmberFraction);
        }

        [Test]
        public void Cart31_5_CannotBeConfirmed_NoStockChange()
        {
            var sim = Cart(0);
            var stock = Stock(sim);
            Assert.AreEqual(31.5, sim.CartGrams);
            Assert.AreEqual(sim.Data.Lines.overLimit, sim.Confirm());
            CollectionAssert.AreEqual(stock, Stock(sim));
            Assert.AreEqual(0, sim.Sales.Count);
            // Refusing (Cancel while still over) = no-sale, nothing sold.
            var c = sim.Serving;
            Assert.IsTrue(sim.Cancel());
            Assert.AreEqual(CustomerOutcome.NoSale, c.Outcome);
            CollectionAssert.AreEqual(stock, Stock(sim));
        }

        /// <summary>SPEC_COMP002 §2 trim options per shape: each one sells.</summary>
        [Test]
        public void EverySpecTrimOption_Sells()
        {
            void Sells(int shape, System.Action<ShiftSim> trim, string what)
            {
                var sim = Cart(shape);
                trim(sim);
                Assert.LessOrEqual(sim.CartGrams, 28, what);
                Assert.IsNull(sim.Confirm(), what);
                Assert.AreEqual(1, sim.Report().OverLimitTrims, what);
            }
            Sells(0, s => s.RemoveLine(1), "31.5: 28 of X");
            Sells(0, s => s.SetLineGrams(0, 14), "31.5: 14 X + 3.5 Y");
            Sells(0, s => s.SetLineGrams(0, 7), "31.5: 7 X + 3.5 Y");
            Sells(1, s => s.RemoveLine(1), "56: 28 g");
            Sells(2, s => s.RemoveLine(2), "35: 14 + 14");
            Sells(2, s => s.SetLineGrams(1, 7), "35: 14 + 7 + 7");
            Sells(2, s => { s.RemoveLine(1); }, "35: 14 + 7");
        }

        [Test]
        public void ThirtyFive_StepDowns_Sell_NeverAboveTheAsk()
        {
            var s2 = Cart(2);
            Assert.IsTrue(s2.StepLine(0, -1));   // 7 + 14 + 7
            Assert.IsNull(s2.Confirm());
            var s3 = Cart(2);
            s3.SetLineGrams(0, 3.5);
            s3.SetLineGrams(1, 7);
            s3.SetLineGrams(2, 14);   // 24.5 g, but Z was asked as 7 g: stepping above an ask is still the wrong weight
            StringAssert.StartsWith("I asked for", s3.Confirm());
        }

        [Test]
        public void TrimmingThePrimary_CostsTheConfiguredPenalty()
        {
            var keep = Cart(0);
            double fx = keep.Cart[0].Fit, fy = keep.Cart[1].Fit;
            keep.RemoveLine(1);                     // drop the second strain: scores normally
            Assert.AreEqual(fx, keep.CartFit(keep.Serving), 1e-9);

            var step = Cart(0);
            step.SetLineGrams(0, 14);               // step the primary down: mean − penalty × primary fit
            Assert.AreEqual(System.Math.Max(0, (fx + fy) / 2 - step.Cfg.primaryTrimFitPenalty * fx), step.CartFit(step.Serving), 1e-9);
            var c = step.Serving;
            Assert.IsNull(step.Confirm());
            Assert.AreEqual(System.Math.Max(0, (fx + fy) / 2 - 0.5 * fx), c.LastFit, 1e-9, "the sale scores with the penalty");

            var drop = Cart(0);
            drop.RemoveLine(0);                     // drop the primary: Y's fit − penalty × X's fit
            Assert.AreEqual(System.Math.Max(0, fy - 0.5 * fx), drop.CartFit(drop.Serving), 1e-9);
        }

        [Test]
        public void StrikeLedger_ReachesTheReport_ManagerReviewAtThreshold()
        {
            var sim = new ShiftSim(Load());
            sim.Tick(0);
            int added = 0;
            sim.Strikes.Added += _ => added++;
            var r0 = sim.Report();
            Assert.AreEqual(0, r0.Strikes.Count);
            Assert.IsFalse(r0.ManagerReview);
            sim.Strike("test reason");
            sim.Tick(30);
            sim.Strike("second");
            var r = sim.Report();
            Assert.AreEqual(2, added);
            CollectionAssert.AreEqual(new[] { "test reason", "second" }, r.Strikes.Select(s => s.Reason));
            Assert.AreEqual(1, r.Strikes[0].CustomerIndex);
            Assert.AreEqual(30, r.Strikes[1].Time - r.Strikes[0].Time, 1e-9);
            Assert.AreEqual(2, sim.Cfg.strikeReviewThreshold);
            Assert.IsTrue(r.ManagerReview);
            Assert.IsFalse(sim.IsOver, "strikes never end the shift (DEC-032)");
        }

        [Test]
        public void SimBot_TrimsOverLimitCustomers()
        {
            var d = Load();
            d.Config.overLimitAskChance = 0.5;
            var sim = SliceTests.RunBot(d, 0.5);
            var r = sim.Report();
            Assert.Greater(r.OverLimitTrims, 0);
            Assert.IsTrue(sim.Sales.GroupBy(s => s.CustomerIndex).All(g => g.Sum(s => s.Grams) <= 28), "never an over-limit sale");
        }
    }
}
