using System.IO;
using System.Linq;
using Dispo.Domain.Engine;
using Dispo.Simulation.Slice;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Slice.Tests
{
    /// <summary>GAME-009: medical customers, 14-day allotment, medical tax, out-of-state cards (Docs/Tasks/Active/GAME-009.md).</summary>
    public class MedicalTests
    {
        static string Read(string rel) => File.ReadAllText(Path.Combine(Application.dataPath, rel));
        static string Cat(string f) => Read("_Game/Data/Catalog/" + f);
        static SliceData Load() => SliceData.Load(Cat("batches.json"), Cat("terpenes.json"), Cat("engine_tables.json"), Cat("pricing.json"),
            Read("_Game/Data/Slice/SliceConfig.json"), Read("_Game/Data/Slice/SliceIntents.json"), Read("_Game/Data/Slice/SliceLines.json"));

        /// <summary>Customer 1 as a MED patient with <paramref name="history"/> g in the last 14 days; every ask accepted.</summary>
        static ShiftSim MedCart(double history, bool outOfState, params double[] grams)
        {
            var sim = new ShiftSim(Load());
            sim.Tick(0);
            var c = sim.Serving;
            var f = c.TrueFamily;
            c.Medical = true; c.OutOfStateCard = outOfState; c.History14d = history; c.Budget = 0; c.OverLimit = false;
            c.Asks = grams.Select(g => new Ask { Family = f, Grams = g }).ToList();
            foreach (var g in grams)
            {
                if (sim.RegisterOpen) sim.AddItem();
                var card = sim.Search(f).Cards.First(k => sim.Free(k.Rep.Id) >= g);
                Assert.AreEqual(Response.Accept, sim.Present(card).Response);
            }
            return sim;
        }

        static double[] Stock(ShiftSim sim) => sim.Inventory.JarBatchIds.Select(sim.Inventory.Grams).ToArray();

        [Test]
        public void Medical3_5g_Total_IsPreTimes1_091_RoundedToTheNickel()
        {
            var sim = MedCart(0, false, 3.5);
            Assert.IsTrue(sim.MedicalSale);
            Assert.AreEqual(9.1, sim.TaxRate, 1e-9);
            var pre = sim.Cart[0].PreTax;
            var p = sim.CartPrice();
            Assert.AreEqual(ShiftSim.CheckoutRound(pre * 1.091), p.PostTax, 1e-9, "F4 9.1 %, DEC-035 nickel");
            Assert.AreEqual(p.PostTax - p.PreTax, p.Tax, 1e-9);
            Assert.AreEqual(Pricing.ApplyTax(pre, 9.1), sim.Price(sim.Cart[0].Card.Rep, 3.5).CardPostTax, 1e-9, "cards: tool priceFloor at the medical rate");
            Assert.IsNull(sim.Confirm());
            var r = sim.Report();
            Assert.IsTrue(sim.Sales.Single().Medical);
            Assert.AreEqual(1, r.MedSales);
            Assert.AreEqual(p.Tax, r.MedTaxCollected, 1e-9);
            Assert.AreEqual(0, r.AdultUseTaxCollected, 1e-9);
        }

        [Test]
        public void FortyTwoGrams_PassesWith70Left_BlockedWith35Left()
        {
            var cfg = Load().Config;
            Assert.AreEqual(70.87, cfg.medicalLimitGrams14d, 1e-9, "A5: 2.5 oz × 28.35");
            var ok = MedCart(cfg.medicalLimitGrams14d - 70, false, 14, 14, 14);
            Assert.AreEqual(70, ok.CartCap, 1e-9);
            Assert.AreEqual(42, ok.CartGrams);
            Assert.AreNotEqual(MeterState.Red, ok.Meter, "the 28 g adult-use cap does not apply to a medical sale");
            Assert.IsNull(ok.Confirm());
            Assert.AreEqual(42, ok.Sales.Sum(s => s.Grams));

            var low = MedCart(cfg.medicalLimitGrams14d - 35, false, 14, 14, 14);
            var stock = Stock(low);
            Assert.AreEqual(MeterState.Red, low.Meter);
            Assert.AreEqual(low.Data.Lines.overMedLimit, low.Confirm());
            CollectionAssert.AreEqual(stock, Stock(low));
            low.RemoveLine(2);   // trims as in GAME-007: 28 g fits the 35 g left
            Assert.IsNull(low.Confirm());
        }

        [Test]
        public void OutOfStateCard_CannotConfirmAsMedical_ThenStrikes_AdultUseSells()
        {
            var sim = MedCart(0, true, 3.5);
            var l = sim.Data.Lines;
            Assert.AreEqual(l.outOfStateMedHint, sim.Confirm(), "1st try: blocked + hint");
            Assert.AreEqual(0, sim.Strikes.Strikes.Count);
            Assert.AreEqual(l.outOfStateMedHint, sim.Confirm(), "2nd try: blocked + strike");
            Assert.AreEqual(1, sim.Strikes.Strikes.Count);
            Assert.AreEqual(l.strikeOutOfStateMed, sim.Strikes.Strikes[0].Reason);
            Assert.AreEqual(0, sim.Sales.Count);
            sim.ToggleSaleType();
            Assert.IsFalse(sim.MedicalSale);
            Assert.AreEqual(sim.Data.Catalog.Pricing.TaxRate, sim.TaxRate, 1e-9, "adult-use 25.1 %");
            Assert.AreEqual(sim.Cfg.adultUseLimitGrams, sim.CartCap, "the 28 g cap applies again");
            var pre = sim.Cart[0].PreTax;
            Assert.IsNull(sim.Confirm());
            Assert.IsFalse(sim.Sales.Single().Medical);
            Assert.AreEqual(ShiftSim.CheckoutRound(pre * 1.251), sim.Sales.Single().PricePostTax, 1e-9);
            var r = sim.Report();
            Assert.AreEqual(0, r.MedSales);
            Assert.AreEqual(1, r.MedCustomers);
            Assert.Greater(r.AdultUseTaxCollected, 0);
        }

        [Test]
        public void OutOfStateAdultUse_KeepsThe28gCap()
        {
            var sim = MedCart(0, true, 14, 14, 7);
            sim.ToggleSaleType();
            Assert.AreEqual(MeterState.Red, sim.Meter, "35 g over the adult-use cap");
            Assert.AreEqual(sim.Data.Lines.overLimit, sim.Confirm());
            sim.RemoveLine(2);
            Assert.IsNull(sim.Confirm());
        }

        [Test]
        public void AdultUsePath_Unchanged()
        {
            var sim = new ShiftSim(Load());
            sim.Tick(0);
            var c = sim.Serving;
            Assume.That(!c.Medical);
            Assert.IsFalse(sim.MedicalSale);
            Assert.AreEqual(25.1, sim.TaxRate, 1e-9);
            Assert.AreEqual(28, sim.CartCap);
            Assert.Throws<System.InvalidOperationException>(() => sim.ToggleSaleType(), "the switch is MED-only");
            var p = sim.Price(new Batch { Tier = "house" }, 3.5);   // Tue: $10.50 × 1.251
            Assert.AreEqual(13.15, p.PostTax, 1e-9);
            Assert.AreEqual(13.10, p.CardPostTax, 1e-9);
        }

        [Test]
        public void Generator_Share_History_OutOfState()
        {
            var d = Load();
            Assert.AreEqual(0.04, d.Config.medicalCustomerShare, 1e-9, "DEC-048: under 5 %");
            string Dump(ShiftSim s) => string.Join("\n", s.Customers.Select(c => $"{c.Index}|{c.Medical}|{c.OutOfStateCard}|{c.History14d}"));
            Assert.AreEqual(Dump(new ShiftSim(Load())), Dump(new ShiftSim(Load())), "same seed, same patients");

            d.Config.medicalCustomerShare = 1; d.Config.outOfStateMedChance = 1;
            var all = new ShiftSim(d).Customers;
            Assert.IsTrue(all.All(c => c.Medical && c.OutOfStateCard));
            var weights = d.Config.weightOdds.Select(w => w.g).ToArray();
            Assert.IsTrue(all.All(c => c.History14d >= 0 && c.History14d <= d.Config.medicalHistoryMaxBuys * weights.Max()));
            Assert.IsTrue(all.Any(c => c.History14d == 0) && all.Any(c => c.History14d > 0), "0-3 prior buys");

            var none = Load(); none.Config.medicalCustomerShare = 0;
            Assert.IsFalse(new ShiftSim(none).Customers.Any(c => c.Medical));
        }

        [Test]
        public void SimBot_ServesMedicalShift()
        {
            var d = Load();
            d.Config.medicalCustomerShare = 0.5;
            var sim = SliceTests.RunBot(d, 0.5);
            var r = sim.Report();
            Assert.Greater(r.MedCustomers, 0);
            Assert.Greater(r.MedSales, 0);
            Assert.Greater(r.MedTaxCollected, 0);
            Assert.AreEqual(sim.Sales.Sum(s => s.PricePostTax - s.PricePreTax), r.MedTaxCollected + r.AdultUseTaxCollected, 1e-9);
            Assert.IsTrue(sim.Sales.Where(s => s.Medical).All(s => !sim.Customers[s.CustomerIndex - 1].OutOfStateCard), "never an out-of-state medical sale");
            Assert.AreEqual(0, r.Strikes.Count);
        }
    }
}
