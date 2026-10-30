using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Dispo.Domain.Engine;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Domain.Tests
{
    /// <summary>
    /// Replays the MIG-001 slice goldens (Docs/Reconstruction/golden_cases.json, v7.11.4 executed) against
    /// the imported catalog (Data/Catalog). Goldens are fixture-bound: re-import ⇒ regenerate goldens (GAP-202).
    /// </summary>
    public class EngineGoldenTests
    {
        static readonly string[] SliceCases = { "RC-01", "RC-03", "RC-04", "RC-09", "RC-10", "RC-11", "X-03", "X-04", "X-05", "X-07", "X-18" };
        const double Ms4dp = 0.00005 + 1e-9; // goldens store ms and raw to 4 dp

        static Catalog _cat;
        static Dictionary<string, object> _golden;

        static string ReadCatalog(string f) => File.ReadAllText(Path.Combine(Application.dataPath, "_Game/Data/Catalog", f));

        static Catalog Cat => _cat ?? (_cat = Load());
        static Catalog Load() => Catalog.Load(ReadCatalog("batches.json"), ReadCatalog("terpenes.json"), ReadCatalog("engine_tables.json"), ReadCatalog("pricing.json"));

        static Dictionary<string, object> Golden => _golden ?? (_golden = (Dictionary<string, object>)Json.Parse(
            File.ReadAllText(Path.Combine(Application.dataPath, "../../Docs/Reconstruction/golden_cases.json"))));

        static Dictionary<string, object> O(object o) => (Dictionary<string, object>)o;
        static List<object> A(object o) => (List<object>)o;
        static Dictionary<string, int> Ints(object o) => O(o).ToDictionary(kv => kv.Key, kv => (int)(double)kv.Value);
        static Dictionary<string, object> Case(string id) => A(Golden["cases"]).Select(O).Single(c => (string)c["id"] == id);

        static ShopState StateOf(Dictionary<string, object> c) => new ShopState
        {
            ActiveTiers = new HashSet<string>(c.TryGetValue("tiers", out var t) ? A(t).Cast<string>() : Enumerable.Empty<string>()),
            NewCustomer = c.TryGetValue("profile", out var p) && (string)p == "new",
            ResultCount = c.TryGetValue("resultCount", out var n) ? (int)(double)n : 3,
        };

        [Test]
        public void Catalog_MatchesGoldenSnapshot()
        {
            var meta = O(Golden["meta"]);
            Assert.AreEqual((double)meta["kept"], Cat.Batches.Count);
            Assert.AreEqual((double)meta["groups"], Cat.Groups().Count);
            Assert.AreEqual((double)meta["inStockGroups"], Cat.Groups().Count(g => g.Batches[0].InStock));
        }

        [TestCaseSource(nameof(SliceCases))]
        public void Recommend_MatchesV7114(string id)
        {
            var c = Case(id);
            var parsed = O(c["parsed"]);
            var r = Recommender.Recommend(Cat, Ints(parsed["crit"]), Ints(parsed["neg"]), parsed["primary"] as string, StateOf(c));

            string outcome = (string)c["outcome"];
            Assert.AreEqual(outcome == "fallback" ? Outcome.Fallback : outcome == "none" ? Outcome.None : Outcome.Ok, r.Outcome, "outcome");

            var calls = A(c["findStrainsCalls"]).Select(O).ToList();
            Assert.AreEqual(calls.Count, r.Calls.Count, "findStrains call count");
            for (int i = 0; i < calls.Count; i++)
            {
                CollectionAssert.AreEquivalent(Ints(calls[i]["crit"]), r.Calls[i].Crit, $"call {i} crit");
                CollectionAssert.AreEquivalent(Ints(calls[i]["neg"]), r.Calls[i].Neg, $"call {i} neg");
                var top = A(calls[i]["top"]).Select(O).ToList();
                CollectionAssert.AreEqual(top.Select(t => (string)t["key"]).ToList(), r.Calls[i].Top.Select(s => s.Key).ToList(), $"call {i} ranking");
                for (int j = 0; j < top.Count; j++)
                {
                    var g = top[j]; var s = r.Calls[i].Top[j]; string at = $"call {i} #{j} {s.Key}";
                    Assert.AreEqual((double)g["ms"], s.Ms, Ms4dp, at + " ms");
                    Assert.AreEqual((string)g["name"], s.Name, at + " name");
                    Assert.AreEqual((string)g["tier"], s.Tier, at + " tier");
                    Assert.AreEqual((int)(double)g["batches"], s.BatchCount, at + " batches");
                    Assert.AreEqual((int)(double)g["cluster"], s.Cluster, at + " cluster");
                    Assert.AreEqual(g["cluster2"] == null ? (int?)null : (int)(double)g["cluster2"], s.Cluster2, at + " cluster2");
                    Assert.AreEqual((int)(double)g["anxietyRisk"], s.AnxietyRisk, at + " anxietyRisk");
                    CollectionAssert.AreEquivalent(Ints(g["domains"]), s.Domains, at + " domains");
                }
            }
            CollectionAssert.AreEqual(A(c["shown"]).Cast<string>().ToList(), r.Strains.Select(s => s.Key).ToList(), "shown");
        }

        // NPC intent keys whose v7.11.4 full-parser result equals the direct INTENTS lookup.
        [TestCase("sleep", "RC-01")]
        [TestCase("anxiety", "RC-09")]
        [TestCase("pain", "RC-04")]
        [TestCase("energy", "RC-10")]
        [TestCase("sinking", "X-07")]
        public void IntentKey_MatchesParser(string key, string caseId)
        {
            var parsed = O(Case(caseId)["parsed"]);
            var q = Intents.Resolve(Cat, key);
            CollectionAssert.AreEquivalent(Ints(parsed["crit"]), q.Crit, "crit");
            CollectionAssert.AreEquivalent(Ints(parsed["neg"]), q.Neg, "neg");
            Assert.AreEqual(parsed["primary"] as string, q.Primary, "primary");
        }

        [Test]
        public void IntentKey_UnknownIsNull() => Assert.IsNull(Intents.Resolve(Cat, "something for the day"));

        [Test]
        public void Pricing_AllTiersDaysWeights()
        {
            int n = 0;
            foreach (var kv in O(Golden["pricing"]))
            {
                string tier = kv.Key == "(none)" ? "" : kv.Key;
                foreach (var day in A(kv.Value).Select(O))
                {
                    int dow = (int)(double)day["dow"];
                    var q = Pricing.GetEffectivePrices(Cat.Pricing, tier, dow);
                    Assert.AreEqual(day["deal"] as string, q.DealName, $"{tier} dow {dow} deal");
                    foreach (var row in A(day["rows"]).Select(A))
                    {
                        double w = (double)row[0], pre = (double)row[1], post = (double)row[2];
                        double got = q.Prices.TryGetValue(w, out var v) ? v : 0;
                        Assert.AreEqual(pre, got, 1e-9, $"{tier} dow {dow} {w}g pre");
                        Assert.AreEqual(post, Pricing.ApplyTax(got, Cat.Pricing.TaxRate), 1e-9, $"{tier} dow {dow} {w}g post");
                        n++;
                    }
                }
            }
            Assert.AreEqual(9 * 7 * 4, n);
        }

        [Test]
        public void BatchScores_SingleBatch()
        {
            foreach (var g in A(Golden["batchScores"]).Select(O))
            {
                var b = Cat.Batches.Single(x => x.Id == (string)g["id"]);
                string at = (string)g["id"];
                CollectionAssert.AreEquivalent(Ints(g["domains"]), Scoring.ScoreDomains(Cat, b.Terpenes), at + " domains");
                var raw = Scoring.ScoreRaw(Cat, b.Terpenes);
                foreach (var kv in O(g["raw"])) Assert.AreEqual((double)kv.Value, raw[kv.Key], Ms4dp, at + " raw " + kv.Key);
                var cl = O(g["cluster"]);
                var got = Scoring.ClassifyCluster(b.Terpenes);
                Assert.AreEqual((int)(double)cl["primary"], got.Primary, at + " cluster");
                Assert.AreEqual(cl["secondary"] == null ? (int?)null : (int)(double)cl["secondary"], got.Secondary, at + " cluster2");
                Assert.AreEqual((int)(double)g["anxietyRisk"], Scoring.CalcAnxietyRisk(b.Terpenes), at + " anxiety");
            }
        }

        [Test]
        public void Averaging_ZeroGravityRecencyWeighted()
        {
            var g = O(Golden["averaging"]);
            var group = Cat.Groups().Single(x => x.Key == (string)g["key"]);
            Assert.AreEqual((int)(double)g["batchesTotal"], group.Batches.Count);
            var p = Scoring.AverageProfile(group.Batches);
            var top5 = p.OrderByDescending(kv => kv.Value).Take(5).ToList();
            var want = A(g["avgTop5"]).Select(A).ToList();
            for (int i = 0; i < 5; i++)
            {
                Assert.AreEqual((string)want[i][0], top5[i].Key);
                Assert.AreEqual((double)want[i][1], top5[i].Value, 1e-12);
            }
        }

        // V73-NT5: v7.11.4 lets an empty-tier batch pass the House chip. No in-stock batch has an empty tier in the
        // snapshot, so the defect is shown on a synthetic batch. v7.11.4 value first, then the game-expected value.
        [Test]
        public void TierChip_EmptyTier_V73NT5()
        {
            var cat = Load();
            cat.Batches.Add(new Batch
            {
                Id = "synthetic_empty_tier", StrainName = "Synthetic Empty Tier", BatchCode = "", Brand = "", Tier = "", InStock = true,
                Terpenes = new Dictionary<string, double> { { "beta_myrcene", 1.5 }, { "linalool", 0.4 } },
            });
            var crit = new Dictionary<string, int> { { DomainIds.Sedation, 38 } };
            var neg = new Dictionary<string, int>();
            var keysV7114 = Recommender.FindStrains(cat, crit, neg, DomainIds.Sedation, new ShopState { ResultCount = 99, ActiveTiers = { "house" } }).Select(s => s.Key);
            CollectionAssert.Contains(keysV7114.ToList(), "synthetic empty tier", "v7.11.4: empty tier counts as House");
            var keysGame = Recommender.FindStrains(cat, crit, neg, DomainIds.Sedation,
                new ShopState { ResultCount = 99, ActiveTiers = { "house" }, EmptyTierCountsAsHouse = false }).Select(s => s.Key);
            CollectionAssert.DoesNotContain(keysGame.ToList(), "synthetic empty tier", "game-expected: empty tier matches no chip");
        }

        [Test]
        public void Json_ParsesEscapesAndNumbers()
        {
            var o = (Dictionary<string, object>)Json.Parse("{\"a\":[1,-2.5e1,true,null],\"b\":\"x\\\"\\u00e9\"}");
            CollectionAssert.AreEqual(new object[] { 1.0, -25.0, true, null }, (List<object>)o["a"]);
            Assert.AreEqual("x\"é", o["b"]);
            Assert.Throws<FormatException>(() => Json.Parse("{\"a\":1} x"));
        }
    }
}
