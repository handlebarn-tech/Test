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

        /// <summary>One bot step: talk → look it up → true-family chip → card 1 (next if the jar is short) → Add item while an ask is open
        /// and fits under the cap (GAME-006/007) → trim if red → confirm.</summary>
        static bool _backChecked;

        public static void Step(SliceGame g)
        {
            // GAME-008: cover the stand when asked, and judge each ID correctly (a perfect bot); the stand comes before the counter.
            if (g.Screen == SliceScreen.CoverPrompt) { g.AcceptCover(); return; }
            if (g.Screen == SliceScreen.IdCheck) { if (g.Sim.IdValid(g.IdCustomer)) g.IdAdmit(); else g.IdRefuse(); return; }
            if (g.Screen == SliceScreen.World && g.Sim.Stand.Count > 0) { g.OpenIdPanel(); return; }
            var c = g.Sim.Serving;
            if (c == null) return;
            switch (g.Screen)
            {
                case SliceScreen.World: if (g.CustomerAtCounter) g.Talk(); break;
                case SliceScreen.Dialogue: g.LookItUp(); break;
                case SliceScreen.Query: g.ChooseChip(g.Sim.CurrentAsk.Family); break;
                case SliceScreen.Results:
                    var ask = g.Sim.CurrentAsk;
                    var card = g.Sim.Results.Cards.FirstOrDefault(k => g.Sim.Free(k.Rep.Id) >= ask.Grams);
                    Assert.IsNotNull(card, $"customer {c.Index}: no card can fill {ask.Grams} g");
                    g.Choose(card);
                    break;
                case SliceScreen.Pos:
                    // GAME-007: trim an over-limit cart (drop the last line), add the next ask only if it fits under the cap.
                    if (g.Sim.Meter == MeterState.Red)   // GAME-009: a lone medical line over the allotment rings adult-use instead
                    { if (g.Sim.Cart.Count > 1) g.PosRemove(g.Sim.Cart.Count - 1); else if (g.Sim.MedicalSale) g.ToggleSaleType(); else g.PosCancel(); }
                    else if (g.Sim.CanAddItem && g.Sim.CartGrams + g.Sim.CurrentAsk.Grams <= g.Sim.CartCap) g.AddItem();
                    else if (g.Sim.MedicalSale && g.Sim.Serving.OutOfStateCard) g.ToggleSaleType();   // GAME-009: ring it as adult-use
                    else if (g.Sim.Cart.Count > 1 && !_backChecked)
                    {
                        // DEC-065: Esc on a multi-line cart goes back to the cards and keeps the cart.
                        int n = g.Sim.Cart.Count;
                        g.Back();
                        Assert.AreEqual(SliceScreen.Results, g.Screen);
                        Assert.AreEqual(n, g.Sim.Cart.Count);
                        g.GoToRegister();
                        Assert.AreEqual(SliceScreen.Pos, g.Screen);
                        _backChecked = true;
                    }
                    else Assert.IsNull(g.PosConfirm());
                    break;
            }
        }

        [UnityTest]
        public IEnumerator Bot_Seed1_FullShift()
        {
            var g = Object.FindAnyObjectByType<SliceGame>();
            Assert.IsNotNull(g, "SliceGame missing from Gameplay_Slice");
            Assert.AreEqual(1, g.Sim.Cfg.seed);
            _backChecked = false;
            g.Sim.Cfg.coverCheckInChance = 1;   // GAME-008: the rush always asks, so the bot covers the stand (read at rush start)
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
            Assert.IsTrue(sim.Customers.All(c => c.State == CustomerState.Done && c.Outcome != CustomerOutcome.None), "all resolve");
            Assert.AreEqual(sim.Cfg.customersPerShift, sim.Customers.Count);
            Assert.IsTrue(typeof(ShiftReport).GetFields().All(f => f.GetValue(r) != null), "no null report fields");
            Assert.AreEqual(sim.Sales.Sum(s => s.PricePostTax), r.RevenuePostTax, 1e-9, "revenue = Σ sale events");
            // GAME-005 / W4E m2: sold jars show the nearest PROC-002 fill step (ties up), at least the min visible step above 0 g (DEC-046).
            foreach (var id in sim.Sales.Select(s => s.BatchId).Distinct())
            {
                double fill = sim.Inventory.Fill(id) * 100;
                var visible = g.JarFillSteps(id).Where(s => s > 0 && s >= sim.Cfg.jarMinVisibleStepPct);
                int expected = fill <= 0 ? 0 : visible.OrderBy(s => System.Math.Abs(s - fill)).ThenByDescending(s => s).First();
                Assert.AreEqual(expected / 100f, g.JarFillShown(id), 1e-6, $"jar fill step for {id} ({fill:0.##} %)");
            }
            Assert.IsTrue(sim.Inventory.SoldOutIds.All(id => g.JarFillShown(id) == 0), "SOLD OUT jars show F000");
            CollectionAssert.IsNotEmpty(r.SoldOut, "at least one SOLD OUT (DEC-027)");
            Assert.LessOrEqual(sim.ClockHours, sim.Cfg.storeCloseHour, "clock inside store hours (DEC-036 M3)");
            Assert.IsTrue(sim.Sales.GroupBy(s => s.CustomerIndex).All(s => s.Sum(x => x.Grams) <= (s.First().Medical
                ? sim.MedicalRemaining(sim.Customers[s.Key - 1]) : sim.Cfg.adultUseLimitGrams)), "M1 / 14-day allotment on each cart");
            Assert.IsTrue(sim.Sales.GroupBy(s => s.CustomerIndex).Any(s => s.Count() == 2), "GAME-006: the bot sells a 2-item cart");
            Assert.IsTrue(_backChecked, "DEC-065 Esc-keeps-cart path ran");
            Assert.AreEqual(sim.Cfg.coverCheckInCount, r.IdsChecked, "GAME-008: the covered arrivals were all checked");
            Assert.AreEqual(0, r.Strikes.Count, "a perfect bot gets no strike");
            Assert.AreEqual(0, r.ValidIdsRefused);
        }
    }
}
