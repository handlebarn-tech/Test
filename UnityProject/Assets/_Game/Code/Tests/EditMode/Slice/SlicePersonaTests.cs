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

        public static readonly Persona Perfect = new Persona { Name = "perfect", TrueChip = true, BestCard = true, PickSec = 25, PosSec = 20, RepickSec = 10 };
        public static readonly Persona Careless = new Persona { Name = "careless", PickSec = 25, PosSec = 20, RepickSec = 10 };
        public static readonly Persona Slow = new Persona { Name = "slow", TrueChip = true, BestCard = true, PickSec = 50, PosSec = 40, RepickSec = 20 };
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

        /// <summary>Plays one seeded shift. Perfect picks the card with the best fit + price (cards 1-3 plus one More options page);
        /// careless picks a random chip and a random card, blind to budget. Both sell the stated weight.</summary>
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
                Assert.Less(guard, 200000, $"{p.Name} seed {seed}: shift never ended");
                sim.Tick(step);
                var c = sim.Serving;
                if (c == null) continue;
                if (c != cur) { cur = c; tried.Clear(); next = c.ServiceStart + p.PickSec; }
                if (sim.Time < next) continue;
                if (sim.Pending != null) { Assert.IsNull(sim.Confirm(c.Grams)); continue; }

                var card = Choose(sim, p, rng, tried);
                tried.Add(card.Strain.Key);
                next = sim.Time + (sim.Present(card).Response == Response.Accept ? p.PosSec : p.RepickSec);
            }
            return sim;
        }

        static Card Choose(ShiftSim sim, Persona p, System.Random rng, HashSet<string> tried)
        {
            var c = sim.Serving;
            bool Ok(Card k) => k.HasPrice && !tried.Contains(k.Strain.Key) && sim.Inventory.Grams(k.Rep.Id) >= c.Grams;
            var fams = sim.Data.Intents.families;
            for (int attempt = 0; attempt < 20; attempt++)
            {
                if (sim.Results == null || attempt > 0)
                {
                    sim.Search(p.TrueChip ? c.TrueFamily : fams[rng.Next(fams.Length)]);
                    if (p.BestCard && sim.Results.MoreAvailable) sim.MoreOptions();
                }
                var ok = sim.Results.Cards.Where(Ok).ToList();
                if (ok.Count == 0) { Assert.IsFalse(p.TrueChip, $"customer {c.Index}: no card can fill {c.Grams} g"); continue; }
                if (!p.BestCard) return ok[rng.Next(ok.Count)];
                var cfg = sim.Cfg;
                return ok.OrderByDescending(k => cfg.wFit * sim.Fit(c.TrueFamily, k.Strain.Key) + cfg.wPrice * ShiftSim.PriceFit(k.CheckoutPostTax, c.Budget)).First();
            }
            Assert.Fail($"customer {c.Index}: no chip gave a fillable card");
            return null;
        }

        public static double Average(Persona p, int seeds = 20, Action<SliceConfig> tweak = null) =>
            Enumerable.Range(1, seeds).Average(s =>
            {
                var d = Load();
                tweak?.Invoke(d.Config);
                return Run(d, p, s).Report().AvgSatisfaction;
            });

        // TEMP exploration grid (removed before handoff).
        [Test]
        public void Explore_TuningGrid()
        {
            var watch = System.Diagnostics.Stopwatch.StartNew();
            var budgets = new[] { new[] { 4.0, 6.0 }, new[] { 3.0, 5.0 }, new[] { 2.5, 4.0 }, new[] { 2.0, 3.5 } };
            var patience = new[] { 1.0, 0.75, 0.5 };
            var lines = new List<string>();
            foreach (var b in budgets)
            foreach (var pm in patience)
            {
                void Tweak(SliceConfig cfg) { cfg.budgetPerGram = b; foreach (var a in cfg.archetypes) a.patienceSec *= pm; }
                var avgs = Persona.All.Select(p => Average(p, 20, Tweak)).ToList();
                lines.Add($"budget {string.Join("/", b)} patience x{pm}: " + string.Join("  ", Persona.All.Select((p, i) => $"{p.Name}={avgs[i]:0.0}")) + $"  [{watch.Elapsed.TotalSeconds:0}s]");
                Debug.Log("[Tuning] " + lines.Last());
                if (watch.Elapsed.TotalMinutes > 20) break;
            }
            Debug.Log("[Tuning]\n" + string.Join("\n", lines));
        }
    }
}
