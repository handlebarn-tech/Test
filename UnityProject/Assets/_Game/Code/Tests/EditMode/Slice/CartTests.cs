using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using Dispo.Domain.Engine;
using Dispo.Simulation.Slice;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Slice.Tests
{
    /// <summary>GAME-006 cart validation (Docs/Tasks/Active/GAME-006.md).</summary>
    public class CartTests
    {
        static string Read(string rel) => File.ReadAllText(Path.Combine(Application.dataPath, rel));
        static string Cat(string f) => Read("_Game/Data/Catalog/" + f);
        static SliceData Load() => SliceData.Load(Cat("batches.json"), Cat("terpenes.json"), Cat("engine_tables.json"), Cat("pricing.json"),
            Read("_Game/Data/Slice/SliceConfig.json"), Read("_Game/Data/Slice/SliceIntents.json"), Read("_Game/Data/Slice/SliceLines.json"));

        /// <summary>Customer 1 asks for <paramref name="grams"/> of its true family, no budget; each item is searched, accepted and added.</summary>
        static ShiftSim CartOf(params double[] grams)
        {
            var sim = new ShiftSim(Load());
            sim.Tick(0);
            var c = sim.Serving;
            var fam = c.TrueFamily;
            c.Budget = 0;
            c.Asks = grams.Select(g => new Ask { Family = fam, Grams = g }).ToList();
            foreach (var g in grams)
            {
                if (sim.RegisterOpen) sim.AddItem();
                var card = sim.Search(fam).Cards.First(k => sim.Free(k.Rep.Id) >= g);
                Assert.AreEqual(Response.Accept, sim.Present(card).Response);
            }
            Assert.AreEqual(grams.Length, sim.Cart.Count);
            return sim;
        }

        static double[] Stock(ShiftSim sim) => sim.Inventory.JarBatchIds.Select(sim.Inventory.Grams).ToArray();

        [Test]
        public void TwoLineCart_RoundsOnceOnTheTotal()
        {
            var sim = CartOf(3.5, 3.5);
            // Two Tuesday house eighths: $10.50 + $10.50 = $21.00 × 1.251 = $26.271 → $26.25 once; per line it would be 2 × $13.15 = $26.30.
            var house = sim.Price(new Batch { Tier = "house" }, 3.5);
            foreach (var x in sim.Cart) x.Price = house;
            var p = sim.CartPrice();
            Assert.AreEqual(21.00, p.PreTax, 1e-9);
            Assert.AreEqual(26.25, p.PostTax, 1e-9, "DEC-035 nickel rounding once on the cart");
            Assert.AreNotEqual(2 * house.PostTax, p.PostTax);
            Assert.AreEqual(p.PostTax, p.PreTax + p.Tax, 1e-9);

            var real = CartOf(3.5, 7);
            var total = real.CartPrice();
            Assert.AreEqual(ShiftSim.CheckoutRound(real.Cart.Sum(x => x.PreTax) * 1.251), total.PostTax, 1e-9);
            Assert.IsNull(real.Confirm());
            Assert.AreEqual(2, real.Sales.Count, "one Sell event per line");
            Assert.AreEqual(total.PostTax, real.Sales.Sum(s => s.PricePostTax), 1e-9, "Σ line events = the register total");
            Assert.AreEqual(total.PreTax, real.Sales.Sum(s => s.PricePreTax), 1e-9);
        }

        [Test]
        public void HalfPlusHalf_Sells()
        {
            var sim = CartOf(14, 14);
            var c = sim.Serving;
            var before = sim.Cart.GroupBy(x => x.BatchId).ToDictionary(g => g.Key, g => sim.Inventory.Grams(g.Key));
            Assert.AreEqual(28, sim.CartGrams);
            Assert.IsNull(sim.Confirm());
            Assert.AreEqual(2, sim.Sales.Count);
            Assert.AreEqual(28, sim.Sales.Sum(s => s.Grams));
            foreach (var kv in before) Assert.AreEqual(kv.Value - sim.Sales.Where(s => s.BatchId == kv.Key).Sum(s => s.Grams), sim.Inventory.Grams(kv.Key), 1e-9);
            Assert.AreEqual(CustomerOutcome.Bought, c.Outcome);
            Assert.AreEqual(2.0, sim.Report().UnitsPerSale, 1e-9);
        }

        [Test]
        public void HalfHalfEighth_BlockedByM1_NoStockChange()
        {
            var sim = CartOf(14, 14, 3.5);
            var stock = Stock(sim);
            Assert.IsFalse(sim.CanAddItem, "3 lines = cart full");
            Assert.AreEqual(sim.Data.Lines.overLimit, sim.Confirm(), "DEC-036 M1 on the cart's summed grams (31.5 g)");
            CollectionAssert.AreEqual(stock, Stock(sim));
            Assert.AreEqual(0, sim.Sales.Count);
            Assert.IsTrue(sim.RegisterOpen, "the cart stays for the player to fix");
        }

        [Test]
        public void Cancel_LeavesStockUnchanged()
        {
            var sim = CartOf(7, 3.5);
            var stock = Stock(sim);
            sim.Cancel();
            CollectionAssert.AreEqual(stock, Stock(sim));
            Assert.AreEqual(0, sim.Cart.Count);
            Assert.IsFalse(sim.RegisterOpen);
            Assert.IsNull(sim.Pending);
            Assert.AreEqual(0, sim.Sales.Count);
            Assert.AreEqual(0, sim.CurrentAskIndex, "back to the first ask");
        }

        /// <summary>DEC-065: leaving the register keeps a multi-line cart; only Cancel empties it.</summary>
        [Test]
        public void LeaveRegister_KeepsCart_CancelEmpties()
        {
            var sim = CartOf(7, 3.5);
            var stock = Stock(sim);
            sim.LeaveRegister();
            Assert.IsFalse(sim.RegisterOpen);
            Assert.AreEqual(2, sim.Cart.Count, "cart kept");
            Assert.IsNotNull(sim.Results, "back to the cards");
            Assert.IsNull(sim.CurrentAsk);
            Assert.Throws<System.InvalidOperationException>(() => sim.Present(sim.Results.Cards[0]), "nothing left to ask for");
            CollectionAssert.AreEqual(stock, Stock(sim));
            sim.OpenRegister();
            sim.Cancel();
            Assert.AreEqual(0, sim.Cart.Count, "Cancel empties it");
            CollectionAssert.AreEqual(stock, Stock(sim));

            var open = CartOf(7, 3.5);
            open.RemoveLine(0);   // ask 0 (7 g) open again; the cards on screen were priced for ask 1 (3.5 g)
            open.LeaveRegister();
            Assert.AreEqual(1, open.Cart.Count);
            Assert.IsNull(open.Results, "cards priced for another ask's weight are dropped");
        }

        [Test]
        public void RemoveAndStep_Lines()
        {
            var sim = CartOf(7, 3.5);
            Assert.IsTrue(sim.StepLine(1, 1));
            Assert.AreEqual(7, sim.Cart[1].Grams);
            Assert.AreEqual(sim.Price(sim.Cart[1].Card.Rep, 7).PreTax, sim.Cart[1].PreTax, 1e-9);
            StringAssert.StartsWith("I asked for", sim.Confirm(), "stepped off the stated weight");
            Assert.IsTrue(sim.StepLine(1, -1));
            Assert.IsFalse(sim.StepLine(1, -1), "3.5 g is the bottom step");
            sim.RemoveLine(0);
            Assert.AreEqual(0, sim.CurrentAskIndex, "the removed line's ask is open again");
            Assert.IsTrue(sim.CanAddItem);
            sim.RemoveLine(0);
            Assert.IsFalse(sim.RegisterOpen, "an empty cart closes the register");
        }

        [Test]
        public void TwoLinesOnOneBatch_NeedTheJarToHoldBoth()
        {
            var sim = CartOf(3.5);
            var id = sim.Cart[0].BatchId;
            Assert.AreEqual(sim.Inventory.Grams(id) - 3.5, sim.Free(id), 1e-9);
            // Leave exactly 3.5 g: the line fits, a second 3.5 g of the same batch would not.
            sim.Inventory.Sell(new SaleEvent { BatchId = id, Grams = sim.Inventory.Grams(id) - 3.5 });
            sim.Serving.Asks.Add(new Ask { Family = sim.Serving.TrueFamily, Grams = 3.5 });
            sim.AddItem();
            var card = sim.Search(sim.CurrentAsk.Family).Cards.FirstOrDefault(k => k.Rep.Id == id);
            Assume.That(card, Is.Not.Null, "the batch is still a card");
            Assert.AreEqual(Response.Blocked, sim.Present(card).Response);
        }

        [Test]
        public void Generator_SameSeed_SameAsks_SomeTwoItem()
        {
            string Dump(ShiftSim s) => string.Join("\n", s.Customers.Select(c => string.Join(";", c.Asks.Select(a => $"{a.Family.id}|{a.Grams}|{a.Clause}"))));
            var a = new ShiftSim(Load());
            Assert.AreEqual(Dump(a), Dump(new ShiftSim(Load())));
            var two = a.Customers.Where(c => c.Asks.Count == 2).ToList();
            CollectionAssert.IsNotEmpty(two, "seed 1 has a two-item customer");
            Assert.IsTrue(a.Customers.All(c => c.Asks.Count <= 2 && c.Asks.Sum(x => x.Grams) <= a.Cfg.adultUseLimitGrams));
            foreach (var c in two)
            {
                StringAssert.Contains(c.Asks[1].Clause, c.Line);
                if (c.HasBudget) Assert.AreEqual(0, c.Budget % 1, "budget is whole dollars over both items");
            }
        }

        static bool HasWord(string line, string w) => Regex.IsMatch(line, "(?<![a-z])" + Regex.Escape(w) + "(?![a-z])");
        static readonly string[] Banned = { "night", "relax", "chill", "work", "drive", "focus", "first time", "never tried", "heavy" };

        /// <summary>The second clause keeps SliceTests' intent-key safety: only the two families' keywords appear.</summary>
        [Test]
        public void TwoItemLines_PassIntentKeySafety()
        {
            var d = Load();
            var keys = d.Catalog.Intents.Keys.ToList();
            int n = 0;
            foreach (var f1 in d.Intents.families)
            foreach (var core in f1.cores)
            foreach (var f2 in d.Intents.families)
            foreach (var core2 in f2.cores.Where(x => !x.Contains('.')))
            {
                var line = CustomerGenerator.RenderLine(d.Lines, d.Lines.Openers("regular")[0], core, 3.5, 0,
                    CustomerGenerator.SecondClause(d.Lines, core2, 3.5)).ToLowerInvariant();
                Assert.IsTrue(HasWord(line, f1.keyword) && HasWord(line, f2.keyword), line);
                var bad = keys.Where(k => k != f1.keyword && k != f2.keyword && HasWord(line, k)).Concat(Banned.Where(b => HasWord(line, b))).ToList();
                CollectionAssert.IsEmpty(bad, line);
                n++;
            }
            Assert.Greater(n, 50);
        }

        [Test]
        public void SimBot_PlaysTwoItemCustomers()
        {
            var sim = SliceTests.RunBot(Load(), 0.5);
            var r = sim.Report();
            Debug.Log($"[SliceBot] GAME-006 unitsPerSale={r.UnitsPerSale:0.00} served={r.CustomersServed} sales={sim.Sales.Count}");
            Assert.IsTrue(sim.Sales.GroupBy(s => s.CustomerIndex).Any(g => g.Count() == 2), "a 2-item cart sold");
            Assert.Greater(r.UnitsPerSale, 1);
            Assert.IsTrue(sim.Sales.GroupBy(s => s.CustomerIndex).All(g => g.Sum(s => s.Grams) <= sim.Cfg.adultUseLimitGrams));
        }
    }
}
