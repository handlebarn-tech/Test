using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Dispo.Domain.Engine;
using Dispo.Simulation.Slice;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Gates.Tests
{
    /// <summary>
    /// QA-002 Gate A (SPEC_DECISION_PRESSURE §0A, §124, DP-028; DEC-058): gameplay state may change what the player tells the
    /// TFS engine, never what the engine answers for the same input. Every gameplay PR keeps this class green.
    /// Baseline = the pure engine on a freshly loaded catalog; every sim state must match it card for card.
    /// </summary>
    public class TfsParityGateTests
    {
        static Dictionary<string, object> O(object o) => (Dictionary<string, object>)o;
        static List<object> A(object o) => (List<object>)o;

        /// <summary>Every gameplay key in SliceConfig turned hard; inventory and pricing keys untouched.</summary>
        static void Hard(SliceConfig c)
        {
            foreach (var a in c.archetypes) a.patienceSec *= 0.4;
            c.rushPatienceMult = 0.3;
            c.budgetPerGram = new[] { 1.0, 2.0 };
            c.acceptThreshold = 95;
            c.maxRejections = 1;
            c.arrivalGapNormalSec = 10; c.arrivalGapRushSec = 3;
            c.wFit = 0.2; c.wPrice = 0.6; c.wSpeed = 0.2;
            c.seed = 7;
        }

        static void TickUntil(ShiftSim sim, Func<ShiftSim, bool> done, string what)
        {
            for (int i = 0; !done(sim); i++) { Assert.Less(i, 5000, "never reached: " + what); sim.Tick(1); }
            Assert.IsNotNull(sim.Serving, what + ": a customer must be at the counter");
        }

        /// <summary>(a) fresh, (b) mid-shift with a full queue, (c) rush window, (d) every gameplay key changed, in the rush.</summary>
        public static IEnumerable<string> States() => new[] { "fresh", "midShiftFullQueue", "rush", "hardConfigRush" };

        static ShiftSim Sim(string state)
        {
            var sim = new ShiftSim(DpScenario.Data(state == "hardConfigRush" ? Hard : (Action<SliceConfig>)null));
            sim.Tick(0);
            switch (state)
            {
                case "midShiftFullQueue": TickUntil(sim, s => s.Queue.Count >= s.Cfg.queueSlots, state); break;
                case "rush":
                case "hardConfigRush": TickUntil(sim, s => s.Queue.Any(c => c.Rush), state); break;
            }
            return sim;
        }

        static RecommendResult Engine(Catalog cat, IntentFamily f, int n) =>
            Recommender.Recommend(cat, f.Crit, f.Neg, f.primary, new ShopState { ResultCount = n });

        static Catalog _fresh;
        static Catalog Fresh => _fresh ?? (_fresh = DpScenario.Data().Catalog);

        [TestCaseSource(nameof(States))]
        public void SliceChips_CardsEqualFreshEngine(string state)
        {
            var sim = Sim(state);
            Assert.AreEqual(0, sim.Sales.Count, "no sales: inventory held equal");
            foreach (var chip in sim.Data.Intents.families)
            {
                var want = Engine(Fresh, chip, sim.Cfg.resultCount);
                var got = sim.Search(chip);
                Assert.AreEqual(want.Outcome, got.Outcome, $"{state} {chip.id}: outcome");
                Assert.AreEqual(Gate.Sig(want.Strains), Gate.Sig(got.Cards.Select(k => k.Strain)), $"{state} {chip.id}: cards");
                CollectionAssert.AreEqual(want.Strains.Select(s => s.RepBatchId), got.Cards.Select(k => k.Rep.Id), $"{state} {chip.id}: rep batch on the card");
            }
        }

        static IEnumerable<string> GoldenQueries() =>
            A(O(Json.Parse(File.ReadAllText(Path.Combine(Application.dataPath, "../../Docs/Reconstruction/golden_cases.json"))))["cases"])
                .Select(c => (string)O(c)["q"]).Distinct();

        /// <summary>The ParserGoldenTests queries through Responder on the sim's live catalog equal the fresh catalog's answers.</summary>
        [TestCaseSource(nameof(States))]
        public void ParserQueries_SameAnswerInEveryState(string state)
        {
            var sim = Sim(state);
            int dow = sim.Cfg.shiftDayOfWeek, n = 0;
            foreach (var q in GoldenQueries())
            {
                Assert.AreEqual(Gate.Sig(Responder.Ask(Fresh, q, new ShopState(), dow)), Gate.Sig(Responder.Ask(sim.Data.Catalog, q, new ShopState(), dow)), $"{state}: '{q}'");
                n++;
            }
            Assert.Greater(n, 30);
        }

        /// <summary>The one allowed difference: a sell-out. The answer then equals the fresh engine with the same stock change, and the batch is gone.</summary>
        [Test]
        public void SellOut_IsTheOnlyAllowedChange()
        {
            var sim = Sim("rush");
            foreach (var chip in sim.Data.Intents.families)
            {
                var rep = sim.Search(chip).Cards[0].Rep.Id;
                sim.Inventory.Sell(new SaleEvent { BatchId = rep, Grams = sim.Inventory.Grams(rep) });
                Assert.IsFalse(sim.Data.Catalog.Batches.Single(b => b.Id == rep).InStock);
                var cat = DpScenario.Data().Catalog;
                foreach (var id in sim.Inventory.SoldOutIds) cat.SetInStock(id, false);

                var got = sim.Search(chip);
                Assert.IsFalse(got.Cards.Any(k => k.Rep.Id == rep), $"{chip.id}: sold-out {rep} returned");
                Assert.AreEqual(Gate.Sig(Engine(cat, chip, sim.Cfg.resultCount).Strains), Gate.Sig(got.Cards.Select(k => k.Strain)), chip.id);
                foreach (var q in GoldenQueries())
                    Assert.AreEqual(Gate.Sig(Responder.Ask(cat, q, new ShopState(), sim.Cfg.shiftDayOfWeek)),
                        Gate.Sig(Responder.Ask(sim.Data.Catalog, q, new ShopState(), sim.Cfg.shiftDayOfWeek)), $"after {rep}: '{q}'");
            }
        }

        /// <summary>
        /// Customer fields the player cannot know (§5). GAME-017: add the KNOWN-profile composer test next to Search below,
        /// over the same variants, and assert the composed query string never contains a hidden avoidance or unstated budget.
        /// </summary>
        public static IEnumerable<(string what, Action<Customer> set)> HiddenVariants(SliceData d) =>
            d.Intents.families.Select(f => ("TrueFamily=" + f.id, (Action<Customer>)(c => c.TrueFamily = f)))
                .Concat(new[] { 0.0, 1, 35, 10000 }.Select(b => ("Budget=" + b, (Action<Customer>)(c => c.Budget = b))))
                .Concat(new[] { ("PatienceLow", (Action<Customer>)(c => c.Patience = 0.01)), ("Rejections=1", (Action<Customer>)(c => c.Rejections = 1)) });

        [Test]
        public void Search_SeesOnlyThePlayersChip()
        {
            var ps = typeof(ShiftSim).GetMethod(nameof(ShiftSim.Search)).GetParameters().Select(p => p.ParameterType);
            CollectionAssert.AreEqual(new[] { typeof(IntentFamily), typeof(bool) }, ps, "Search input = the chip (+ the auto-fill flag) only");

            var sim = Sim("fresh");
            foreach (var chip in sim.Data.Intents.families)
            {
                var want = Gate.Sig(Engine(Fresh, chip, sim.Cfg.resultCount).Strains);
                foreach (var (what, set) in HiddenVariants(sim.Data))
                {
                    set(sim.Serving);
                    Assert.AreEqual(want, Gate.Sig(sim.Search(chip).Cards.Select(k => k.Strain)), $"chip {chip.id} with hidden {what}");
                }
            }
        }

        [TestCaseSource(typeof(DpScenario), nameof(DpScenario.Ids))]
        public void Scenario(string id)
        {
            var s = DpScenario.Load(id);
            var run = DpScenario.Run(s);
            var e = O(s["expect"]);
            Debug.Log($"[QA-002] {id} query={run.Query} cards=\n{string.Join("\n", run.Cards)}\noutcome={run.Outcome}");
            if (e.TryGetValue("query", out var q)) Assert.AreEqual(q, run.Query, "TFS query");
            if (e.TryGetValue("engineOutcome", out var eo)) Assert.AreEqual(eo, run.EngineOutcome.ToString());
            foreach (var b in A(e.TryGetValue("absentReps", out var ar) ? ar : new List<object>()))
                Assert.IsFalse(run.Cards.Any(k => k.EndsWith("|" + b)), $"{b} shown");
            foreach (var k in A(e.TryGetValue("absentStrains", out var ak) ? ak : new List<object>()))
                Assert.IsFalse(run.Cards.Any(x => x.StartsWith(k + "|")), $"{k} shown");
            if (e.TryGetValue("cards", out var cs)) Assert.AreEqual((int)(double)cs, run.Cards.Count, "card count");
            if (e.TryGetValue("outcome", out var oc)) Assert.AreEqual(oc, run.Outcome.ToString());
        }
    }
}
