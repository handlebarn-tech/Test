using System.Collections;
using System.Linq;
using Dispo.Presentation.Slice;
using Dispo.Simulation.Slice;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace Dispo.Slice.PlayMode.Tests
{
    /// <summary>GAME-002: auto-play seed 1 through the real flow methods (the ones the UI buttons call).</summary>
    public sealed class SliceBotTests
    {
        [UnitySetUp]
        public IEnumerator LoadSlice()
        {
            yield return SceneManager.LoadSceneAsync("Retail", LoadSceneMode.Single);
            yield return SceneManager.LoadSceneAsync("Gameplay_Slice", LoadSceneMode.Additive);
            yield return null;
        }

        [UnityTearDown]
        public IEnumerator Reset() { Time.timeScale = 1; yield return null; }

        /// <summary>One bot step: talk → look it up → true-family chip → card 1 (next if the jar is short) → stated weight → confirm.</summary>
        public static void Step(SliceGame g)
        {
            var c = g.Sim.Serving;
            if (c == null) return;
            switch (g.Screen)
            {
                case SliceScreen.World: if (g.CustomerAtCounter) g.Talk(); break;
                case SliceScreen.Dialogue: g.LookItUp(); break;
                case SliceScreen.Query: g.ChooseChip(c.TrueFamily); break;
                case SliceScreen.Results:
                    var card = g.Sim.Results.Cards.FirstOrDefault(k => g.Sim.Inventory.Grams(k.Rep.Id) >= c.Grams);
                    Assert.IsNotNull(card, $"customer {c.Index}: no card can fill {c.Grams} g");
                    g.Choose(card);
                    break;
                case SliceScreen.Pos:
                    g.PosSelectWeight(c.Grams);
                    Assert.IsNull(g.PosConfirm());
                    break;
            }
        }

        [UnityTest]
        public IEnumerator Bot_Seed1_FullShift()
        {
            var g = Object.FindAnyObjectByType<SliceGame>();
            Assert.IsNotNull(g, "SliceGame missing from Gameplay_Slice");
            Assert.AreEqual(1, g.Sim.Cfg.seed);
            Time.timeScale = 20;
            float deadline = Time.realtimeSinceStartup + 240;
            while (g.FinalReport == null)
            {
                Assert.Less(Time.realtimeSinceStartup, deadline, $"shift did not end (t={g.Sim.Time:0}, screen {g.Screen})");
                Step(g);
                yield return null;
            }
            Time.timeScale = 1;

            var sim = g.Sim;
            var r = g.FinalReport;
            Debug.Log($"[SliceBot] PlayMode served={r.CustomersServed} walkouts={r.Walkouts} noSales={r.NoSales} revenue={r.RevenuePostTax:0.00} soldOut={string.Join(",", r.SoldOut)} stars={r.Stars} fallbacks={g.FallbackAnchors.Count}");
            Assert.AreEqual(SliceScreen.Report, g.Screen);
            Assert.IsTrue(sim.Customers.All(c => c.State == CustomerState.Done && c.Outcome != CustomerOutcome.None), "all 12 resolve");
            Assert.AreEqual(12, sim.Customers.Count);
            Assert.IsTrue(typeof(ShiftReport).GetFields().All(f => f.GetValue(r) != null), "no null report fields");
            Assert.AreEqual(sim.Sales.Sum(s => s.PricePostTax), r.RevenuePostTax, 1e-9, "revenue = Σ sale events");
            foreach (var id in sim.Sales.Select(s => s.BatchId).Distinct())
                Assert.AreEqual(sim.Inventory.Grams(id) / sim.Cfg.startGramsPerBatch, g.JarFillShown(id), 1e-4, $"jar fill for {id}");
            CollectionAssert.IsNotEmpty(r.SoldOut, "at least one SOLD OUT (DEC-027)");
            Assert.LessOrEqual(sim.ClockHours, sim.Cfg.storeCloseHour, "clock inside store hours (DEC-036 M3)");
            Assert.IsTrue(sim.Sales.All(s => s.Grams <= sim.Cfg.adultUseLimitGrams));
        }
    }
}
