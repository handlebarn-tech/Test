using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using Dispo.Domain.Engine;
using Dispo.Simulation.Slice;
using UnityEngine;

namespace Dispo.Gates.Tests
{
    /// <summary>What a scenario run produced: the TFS query the player sent, the cards it got, and how the customer left.</summary>
    public sealed class DpRun
    {
        public string Query;                                   // chip id + crit/neg/primary actually passed to the engine
        public List<string> Cards = new List<string>();        // Gate.Sig of every card shown (search + more options)
        public Outcome EngineOutcome;
        public List<Response> Responses = new List<Response>();
        public string LastBlock;                               // last POS blocking line, null if none
        public CustomerOutcome Outcome;
    }

    /// <summary>
    /// QA-002 decision-pressure scenario harness (SPEC_DECISION_PRESSURE §115). A scenario is one JSON file in
    /// Data/Tests/DpScenarios: seed, catalog snapshot (batches.json md5 from the catalog manifest), stock overrides,
    /// the customer at the counter (true fields) and the player's actions. Run plays it on the pure ShiftSim.
    /// </summary>
    public static class DpScenario
    {
        static string Read(string rel) => File.ReadAllText(Path.Combine(Application.dataPath, "_Game", rel));
        static Dictionary<string, object> O(object o) => (Dictionary<string, object>)o;
        static List<object> A(object o) => o == null ? new List<object>() : (List<object>)o;

        public static string Dir => Path.Combine(Application.dataPath, "_Game/Data/Tests/DpScenarios");
        public static IEnumerable<string> Ids() => Directory.GetFiles(Dir, "*.json").Select(Path.GetFileNameWithoutExtension).OrderBy(x => x);
        public static Dictionary<string, object> Load(string id) => O(Json.Parse(File.ReadAllText(Path.Combine(Dir, id + ".json"))));

        /// <summary>Fresh slice data with the parser tables (SliceData.Load leaves them out); optional config edit before the sim exists.</summary>
        public static SliceData Data(Action<SliceConfig> tune = null)
        {
            string Cat(string f) => Read("Data/Catalog/" + f);
            var d = new SliceData
            {
                Catalog = Catalog.Load(Cat("batches.json"), Cat("terpenes.json"), Cat("engine_tables.json"), Cat("pricing.json"), Cat("parser_tables.json")),
                Config = SliceConfig.FromJson(Read("Data/Slice/SliceConfig.json")),
                Intents = SliceIntents.FromJson(Read("Data/Slice/SliceIntents.json")),
                Lines = SliceLines.FromJson(Read("Data/Slice/SliceLines.json")),
            };
            tune?.Invoke(d.Config);
            return d;
        }

        public static string CatalogMd5() =>
            A(O(Json.Parse(Read("Data/Catalog/manifest.json")))["outputs"]).Select(O).Single(x => (string)x["file"] == "batches.json")["md5"] as string;

        public static DpRun Run(Dictionary<string, object> s)
        {
            string id = (string)s["id"];
            if ((string)s["catalogMd5"] != CatalogMd5()) throw new InvalidOperationException($"{id}: written for catalog {s["catalogMd5"]}, catalog is {CatalogMd5()}");
            var d = Data(c => c.seed = (int)(double)s["seed"]);
            var sim = new ShiftSim(d);

            // Stock overrides go through the real sale path, so the engine sees them exactly like a sell-down (grams can only drop).
            foreach (var o in A(s.TryGetValue("stock", out var st) ? st : null).Select(O))
            {
                string b = (string)o["batch"];
                double cut = sim.Inventory.Grams(b) - (double)o["grams"];
                if (cut < 0) throw new InvalidOperationException($"{id}: {b} holds {sim.Inventory.Grams(b)} g, cannot raise to {o["grams"]}");
                if (cut > 0) sim.Inventory.Sell(new SaleEvent { BatchId = b, Grams = cut });
            }
            sim.Sales.Clear();   // shortcut: setup sales are not part of the scenario; a report-level scenario needs a setup hook instead

            sim.Tick(0);
            var c = sim.Serving;
            var cu = O(s["customer"]);
            var arch = d.Config.archetypes.Single(a => a.id == (string)cu["archetype"]);
            c.Archetype = arch;
            c.TrueFamily = d.Intents.Get((string)cu["trueFamily"]);
            c.Grams = (double)cu["grams"];
            c.Budget = (double)cu["budget"];
            c.Line = CustomerGenerator.RenderLine(d.Lines, d.Lines.Openers(arch.id)[(int)(double)cu["openerIndex"]], c.TrueFamily.cores[0], c.Grams, c.Budget);

            var run = new DpRun();
            foreach (var a in A(s["actions"]).Select(O))
            {
                switch ((string)a["do"])
                {
                    case "search":
                        var chip = d.Intents.Get((string)a["chip"]);
                        var r = sim.Search(chip);
                        run.Query = Query(chip);
                        run.EngineOutcome = r.Outcome;
                        run.Cards = r.Cards.Select(k => Gate.Sig(k.Strain)).ToList();
                        break;
                    case "more":
                        run.Cards = sim.MoreOptions().Cards.Select(k => Gate.Sig(k.Strain)).ToList();
                        break;
                    case "present":
                        run.Responses.Add(sim.Present(sim.Results.Cards[(int)(double)a["card"]]).Response);
                        break;
                    case "confirm":
                        run.LastBlock = sim.Confirm(a.TryGetValue("grams", out var g) ? (double)g : c.Grams);
                        break;
                    case "cancel":
                        sim.Cancel();
                        break;
                    default: throw new InvalidOperationException($"{id}: unknown action {a["do"]}");
                }
            }
            run.Outcome = c.Outcome;
            return run;
        }

        public static string Query(IntentFamily f) =>
            $"{f.id}|crit:{string.Join(",", f.Crit.OrderBy(x => x.Key).Select(x => x.Key + "=" + x.Value))}|neg:{string.Join(",", f.Neg.OrderBy(x => x.Key).Select(x => x.Key + "=" + x.Value))}|primary:{f.primary}";
    }

    /// <summary>The card fingerprint Gate A compares: strain key, Ms to 4 dp, rep batch.</summary>
    public static class Gate
    {
        public static string Sig(StrainResult s) => s == null ? "-" : $"{s.Key}|{s.Ms.ToString("0.0000", CultureInfo.InvariantCulture)}|{s.RepBatchId}";
        public static string Sig(IEnumerable<StrainResult> xs) => string.Join("\n", xs.Select(Sig));
        public static string Sig(QueryResponse r) =>
            $"{r.Kind}|{r.Outcome}\n{Sig(r.Strains)}\ncard:{Sig(r.Card)}\nnear:{Sig(r.Near)}\ntags:{string.Join(",", r.RoleTags)}";
    }
}
