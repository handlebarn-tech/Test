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
    /// GAME-003: every case in golden_cases.json (MIG-001, v7.11.4 executed) replayed from the raw query through the C# parser
    /// and responder, plus golden_cases_game003.json (Tools/Data/golden_game003.js: 54 parser-coverage queries on v7.11.4, and
    /// MC-7 / GAP-206 under v7.11.4 and under the game fix, both executed by the tool's own source).
    /// </summary>
    public class ParserGoldenTests
    {
        const double Dp4 = 0.00005 + 1e-9;
        const int Dow = 4; // the goldens' pinned clock is a Thursday

        static Catalog _cat;
        static Dictionary<string, object> _golden, _game;

        static string Root => Path.Combine(Application.dataPath, "../..");
        static string ReadCatalog(string f) => File.ReadAllText(Path.Combine(Application.dataPath, "_Game/Data/Catalog", f));
        internal static Catalog Cat => _cat ?? (_cat = Load());
        internal static Catalog Load() => Catalog.Load(ReadCatalog("batches.json"), ReadCatalog("terpenes.json"), ReadCatalog("engine_tables.json"),
            ReadCatalog("pricing.json"), ReadCatalog("parser_tables.json"));
        static Dictionary<string, object> Golden => _golden ?? (_golden = O(Json.Parse(File.ReadAllText(Path.Combine(Root, "Docs/Reconstruction/golden_cases.json")))));
        static Dictionary<string, object> Game => _game ?? (_game = O(Json.Parse(File.ReadAllText(Path.Combine(Root, "Docs/Reconstruction/golden_cases_game003.json")))));

        static Dictionary<string, object> O(object o) => (Dictionary<string, object>)o;
        static List<object> A(object o) => (List<object>)o;
        static Dictionary<string, int> Ints(object o) => O(o).ToDictionary(kv => kv.Key, kv => (int)(double)kv.Value);
        static object Get(Dictionary<string, object> d, string k) => d.TryGetValue(k, out var v) ? v : null;

        static IEnumerable<string> MigCaseIds() => A(Golden["cases"]).Select(c => (string)O(c)["id"]);
        static IEnumerable<int> CoverageIndexes() => Enumerable.Range(0, A(Game["v7114"]).Count);

        [TestCaseSource(nameof(MigCaseIds))]
        public void Mig001_FromRawQuery(string id)
        {
            var c = A(Golden["cases"]).Select(O).Single(x => (string)x["id"] == id);
            var state = new ShopState
            {
                ActiveTiers = new HashSet<string>(c.TryGetValue("tiers", out var t) ? A(t).Cast<string>() : Enumerable.Empty<string>()),
                NewCustomer = c.TryGetValue("profile", out var p) && (string)p == "new",
            };
            Check(c, Responder.Ask(Cat, (string)c["q"], state, Dow), "findStrainsCalls", true);
        }

        [TestCaseSource(nameof(CoverageIndexes))]
        public void Game003_ParserCoverage_V7114(int i)
        {
            var c = O(A(Game["v7114"])[i]);
            Check(c, Responder.Ask(Cat, (string)c["q"], new ShopState(), Dow), "calls", false);
        }

        // DEC-016: each parser defect has a v7.11.4 golden (default options) and a game-expected golden (fix on).
        [TestCase("MC-7")]
        [TestCase("GAP-206")]
        public void Defect_V7114AndGameExpected(string id)
        {
            var d = A(Game["defects"]).Select(O).Single(x => (string)x["id"] == id);
            var v = O(d["v7114"]); var g = O(d["game"]);
            Check(v, Responder.Ask(Cat, (string)v["q"], new ShopState(), Dow, ParserOptions.V7114), "calls", false);
            Check(g, Responder.Ask(Cat, (string)g["q"], new ShopState(), Dow, ParserOptions.Game), "calls", false);
        }

        static void Check(Dictionary<string, object> c, QueryResponse r, string callsKey, bool fullCards)
        {
            var gp = O(c["parsed"]); var p = r.Parsed; string q = (string)c["q"];
            Assert.AreEqual((string)gp["intent"], IntentName(p.Intent), q + ": intent");
            if (p.Intent == Intent.Recommend)
            {
                CollectionAssert.AreEquivalent(Ints(gp["crit"]), p.Crit, q + ": crit");
                CollectionAssert.AreEquivalent(Ints(gp["neg"]), p.Neg, q + ": neg");
                Assert.AreEqual(Get(gp, "primary") as string, p.Primary, q + ": primary");
                CollectionAssert.AreEqual(A(gp["lbls"]).Cast<string>().ToList(), p.Lbls, q + ": lbls");
                Assert.AreEqual(Get(gp, "tf") as string, p.Tf, q + ": tf");
                var opts = Get(gp, "opts") == null ? new Dictionary<string, object>() : O(gp["opts"]);
                CollectionAssert.AreEqual(Get(opts, "exclude") == null ? null : A(opts["exclude"]).Cast<string>().ToList(), p.Opts.Exclude, q + ": opts.exclude");
                Assert.AreEqual(Get(opts, "likeKey") as string, p.Opts.LikeKey, q + ": opts.likeKey");
                Assert.AreEqual(Get(opts, "maxPrice") == null ? (double?)null : (double)opts["maxPrice"], p.Opts.MaxPrice, q + ": opts.maxPrice");
            }
            Assert.AreEqual(Get(gp, "groupKey") as string, p.GroupKey, q + ": groupKey");
            CollectionAssert.AreEqual(Get(gp, "strains") == null ? null : A(gp["strains"]).Cast<string>().ToList(), p.Strains, q + ": strains");
            Assert.AreEqual(Get(gp, "terpene") as string, p.Terpene, q + ": terpene");
            CollectionAssert.AreEqual(Get(gp, "excl") == null ? null : A(gp["excl"]).Cast<string>().ToList(), p.Excl?.Select(e => e.Name).ToList(), q + ": excl");
            var pi = Get(gp, "priceIntent") == null ? null : O(gp["priceIntent"]);
            Assert.AreEqual(pi == null ? null : (string)pi["type"], p.PriceIntent == null ? null : PriceName(p.PriceIntent.Type), q + ": priceIntent");
            if (pi != null && pi.ContainsKey("amount")) Assert.AreEqual((int)(double)pi["amount"], p.PriceIntent.Amount, q + ": budget");
            if (gp.ContainsKey("drive")) Assert.AreEqual((bool)gp["drive"], p.Drive, q + ": drive");

            Assert.AreEqual((string)c["outcome"], OutcomeName(r.Outcome), q + ": outcome");
            var calls = A(c[callsKey]).Select(O).ToList();
            var mine = r.Recommend?.Calls ?? new List<FindCall>();
            Assert.AreEqual(calls.Count, mine.Count, q + ": findStrains calls");
            for (int i = 0; i < calls.Count; i++)
            {
                CollectionAssert.AreEquivalent(Ints(calls[i]["crit"]), mine[i].Crit, $"{q}: call {i} crit");
                CollectionAssert.AreEquivalent(Ints(calls[i]["neg"]), mine[i].Neg, $"{q}: call {i} neg");
                var top = A(calls[i]["top"]).Select(O).ToList();
                CollectionAssert.AreEqual(top.Select(x => (string)x["key"]).ToList(), mine[i].Top.Select(s => s.Key).ToList(), $"{q}: call {i} ranking");
                for (int j = 0; j < top.Count; j++)
                {
                    Assert.AreEqual((double)top[j]["ms"], mine[i].Top[j].Ms, Dp4, $"{q}: call {i} #{j} ms");
                    if (fullCards) Brief(top[j], mine[i].Top[j], $"{q}: call {i} #{j}");
                }
            }
            CollectionAssert.AreEqual(A(c["shown"]).Cast<string>().ToList(), Shown(r), q + ": shown");
            if (c.TryGetValue("roleTags", out var rt)) CollectionAssert.AreEqual(A(rt).Select(x => x as string).ToList(), r.RoleTags, q + ": role tags");
            if (c.TryGetValue("exclNote", out var en)) Assert.AreEqual((string)en, r.Kind == ResponseKind.Strain ? r.CardExclNote : r.ExclNote?.Head, q + ": excl note");
            if (c.TryGetValue("compareNote", out var cn)) CollectionAssert.AreEqual(A(cn).Cast<string>().ToList(), new[] { r.Compare.KeyLabel, r.Compare.Line }, q + ": compare note");
            if (c.TryGetValue("terpRank", out var tr))
            {
                var want = A(tr).Select(A).ToList(); var got = r.TerpRank.Take(8).ToList();
                Assert.AreEqual(want.Count, got.Count, q + ": terp rank rows");
                for (int i = 0; i < want.Count; i++)
                {
                    Assert.AreEqual((string)want[i][0], got[i].Name, q + ": terp rank name");
                    Assert.AreEqual((double)want[i][1], got[i].Pct, Dp4, q + ": terp rank pct");
                }
            }
            if (c.TryGetValue("cards", out var cards))
            {
                var mineCards = r.Kind == ResponseKind.Compare ? r.Compare.Strains : new[] { r.Card }.Concat(r.Near).ToList();
                var want = A(cards).Select(O).ToList();
                Assert.AreEqual(want.Count, mineCards.Count, q + ": cards");
                for (int i = 0; i < want.Count; i++) Brief(want[i], mineCards[i], $"{q}: card {i}");
            }
            if (c.TryGetValue("more", out var more))
                CollectionAssert.AreEqual(A(more).Cast<string>().ToList(), Responder.MoreOptions(Cat, p, new ShopState(), Shown(r)).Select(s => s.Key).ToList(), q + ": show more");
        }

        static void Brief(Dictionary<string, object> g, StrainResult s, string at)
        {
            Assert.AreEqual((string)g["key"], s.Key, at + " key");
            Assert.AreEqual((string)g["name"], s.Name, at + " name");
            Assert.AreEqual((string)g["tier"], s.Tier, at + " tier");
            Assert.AreEqual((int)(double)g["batches"], s.BatchCount, at + " batches");
            Assert.AreEqual((int)(double)g["cluster"], s.Cluster, at + " cluster");
            Assert.AreEqual(g["cluster2"] == null ? (int?)null : (int)(double)g["cluster2"], s.Cluster2, at + " cluster2");
            Assert.AreEqual((int)(double)g["anxietyRisk"], s.AnxietyRisk, at + " anxietyRisk");
            CollectionAssert.AreEquivalent(Ints(g["domains"]), s.Domains, at + " domains");
        }

        static List<string> Shown(QueryResponse r) =>
            r.Kind == ResponseKind.Strain ? new[] { r.Card }.Concat(r.Near).Where(x => x != null).Select(x => x.Key).ToList()
            : r.Kind == ResponseKind.Compare ? r.Compare.Strains.Select(x => x.Key).ToList()
            : r.Strains.Select(x => x.Key).ToList();

        static string IntentName(Intent i) => i == Intent.Recommend ? "recommend" : i == Intent.Compare ? "compare" : i == Intent.Strain ? "strain"
            : i == Intent.TerpeneRank ? "terpene_rank" : "unknown";
        static string PriceName(PriceIntentType t) => t == PriceIntentType.NoPrice ? "noPrice" : t == PriceIntentType.HasBudget ? "hasBudget" : "budget";
        static string OutcomeName(ResponseOutcome o) => o == ResponseOutcome.Ok ? "ok" : o == ResponseOutcome.Fallback ? "fallback" : o == ResponseOutcome.None ? "none"
            : o == ResponseOutcome.ExcludedAll ? "excluded-all" : o == ResponseOutcome.Help ? "help" : "not-found";
    }

    /// <summary>GAME-003 feature units with no executed golden: refine chips, Similar, pricing resolution, parser helpers.</summary>
    public class EngineFeatureTests
    {
        static Catalog Cat => ParserGoldenTests.Cat;
        static ParsedQuery Q(string q) => QueryParser.Parse(Cat, q);

        [Test]
        public void Refine_EditsNumbersThenReappliesConflictRule()
        {
            var sleep = Q("something for sleep"); // {sedation:38} pri sedation
            var lighter = Refine.Apply(sleep, "lighter");
            CollectionAssert.AreEquivalent(new Dictionary<string, int> { { DomainIds.AnxietyRelief, 30 } }, lighter.Crit);
            CollectionAssert.AreEquivalent(new Dictionary<string, int> { { DomainIds.Sedation, 40 } }, lighter.Neg);
            Assert.AreEqual(DomainIds.AnxietyRelief, lighter.Primary);
            CollectionAssert.AreEqual(new[] { "sleep", "something lighter" }, lighter.Lbls);

            var pain = Q("pain"); // {pain:38} cap {sedation:55}
            var body = Refine.Apply(pain, "moreBody");
            CollectionAssert.AreEquivalent(new Dictionary<string, int> { { DomainIds.Sedation, 25 }, { DomainIds.PainInflammation, 38 } }, body.Crit);
            Assert.AreEqual(55, body.Neg[DomainIds.Sedation]);
            var heavier = Refine.Apply(pain, "heavier");
            Assert.IsFalse(heavier.Neg.ContainsKey(DomainIds.Sedation));
            Assert.AreEqual(50, heavier.Crit[DomainIds.Sedation]);
            // a cap within 5 of its crit drops the crit (L19601): sedation ≥50 then "functional" caps 40 and removes it
            var fn = Refine.Apply(heavier, "functional");
            Assert.IsFalse(fn.Crit.ContainsKey(DomainIds.Sedation));
            Assert.AreEqual(DomainIds.PainInflammation, fn.Primary);

            var anx = Refine.Apply(sleep, "lowerAnx");
            Assert.AreEqual(42, anx.Opts.MaxAnx);
            var r = Recommender.FindStrains(Cat, anx.Crit, anx.Neg, anx.Primary, new ShopState { ResultCount = 40 }, anx.Opts);
            Assert.IsTrue(r.Count > 0 && r.All(s => s.AnxietyRisk <= 42));
            Assert.Throws<ArgumentException>(() => Refine.Apply(sleep, "nope"));
        }

        [Test]
        public void Similar_InStockNotLikedSortedTop6()
        {
            var res = Similarity.Similar(Cat, new[] { "kush cake" });
            Assert.AreEqual(6, res.Count);
            Assert.IsTrue(res.All(x => x.Strain.InStock && x.Strain.Key != "kush cake" && x.Sim > 0));
            for (int i = 1; i < res.Count; i++) Assert.GreaterOrEqual(res[i - 1].Sim, res[i].Sim);
            // one liked strain: the blend is its own profile, so Similar agrees with a direct cosine
            var kc = Recommender.AnalyzeGroup(Cat, Cat.Group("kush cake"));
            Assert.AreEqual(Similarity.Cosine(kc.Profile, res[0].Strain.Profile), res[0].Sim, 1e-12);
            Assert.AreEqual(1.0, Similarity.Cosine(kc.Profile, kc.Profile), 1e-12);
            Assert.AreEqual(0.0, Similarity.Cosine(kc.Profile, new Dictionary<string, double>()));
            CollectionAssert.IsEmpty(Similarity.Similar(Cat, new string[0]));
        }

        [Test]
        public void Pricing_OverrideBrandClassAndDealTypes()
        {
            var cat = ParserGoldenTests.Load();
            var t = cat.Pricing;
            Assert.AreEqual("t3", Pricing.GetStrainPricingTier(t, "t3", "", "Kush Cake"));
            t.StrainOverrides.Add(new StrainOverride { Name = "kush CAKE", Tier = "t1" });
            Assert.AreEqual("t1", Pricing.GetStrainPricingTier(t, "t3", "", "Kush Cake"));
            t.BrandPricingClass["Acme"] = "house";
            Assert.AreEqual("house", Pricing.GetStrainPricingTier(t, "t2", "Acme", "x"));
            Assert.AreEqual("premium", Pricing.GetStrainPricingTier(t, "premium", "Acme", "x"));
            t.BrandPricingClass["Acme"] = "fttp";
            Assert.AreEqual("fttp", Pricing.GetStrainPricingTier(t, "t2", "Acme", "x"));

            // Sunday has no default deals; custom deals apply in order, first match wins
            t.CustomDeals.Add(new Deal { Id = "a", Name = "pct", Active = true, TargetType = "multiTier", TargetValues = new List<string> { "t4" }, DealType = "pct_msrp",
                Pct = 50, ExcludeWeights = new List<double> { 28 }, OzOverride = 199 });
            t.CustomDeals.Add(new Deal { Id = "b", Name = "use", Active = true, TargetType = "brand", TargetValue = "Zed", DealType = "use_tier", UseTier = "t1" });
            var q = Pricing.GetEffectivePrices(t, "t4", "", "y", 0);
            Assert.AreEqual("pct", q.DealName);
            Assert.AreEqual(23.5, q.Prices[3.5], 1e-9);
            Assert.AreEqual(199, q.Prices[28], 1e-9);
            var u = Pricing.GetEffectivePrices(t, "t3", "Zed", "y", 0);
            Assert.AreEqual("use", u.DealName);
            Assert.AreEqual(t.Tiers["t1"][3.5], u.Prices[3.5], 1e-9);
            // the slice overload is unchanged: default deals by tier
            Assert.AreEqual(Pricing.GetEffectivePrices(Cat.Pricing, "t3", 1).Prices[3.5], 19.99, 1e-9);
            Assert.AreEqual((3.5, 13.10), Pricing.CheapestPostTax(Cat.Pricing, Pricing.GetEffectivePrices(Cat.Pricing, "smalls", 4)));
            Assert.IsNull(Pricing.CheapestPostTax(Cat.Pricing, Pricing.GetEffectivePrices(Cat.Pricing, "", 4)));
        }

        [Test]
        public void Parser_Helpers()
        {
            var ex = QueryParser.ExtractExclusions(Cat, "no pinenes, bcp or linalool please");
            CollectionAssert.AreEqual(new[] { "pinene", "β-Caryophyllene", "Linalool" }, ex.Excl.Select(e => e.Name).ToList());
            CollectionAssert.AreEqual(new[] { "alpha_pinene", "beta_pinene" }, ex.Excl[0].Ids);
            Assert.AreEqual("please", ex.Text);
            Assert.AreEqual("beta_caryophyllene", QueryParser.FindTerpMention(Cat, "most bcp"));
            Assert.AreEqual("linalool", QueryParser.FindTerpMention(Cat, "lavender vibes"));
            Assert.IsNull(QueryParser.FindTerpMention(Cat, "sleep"));
            Assert.IsTrue(QueryParser.Parse(Cat, "I'm driving home after").Drive);
            Assert.IsFalse(QueryParser.Parse(Cat, "no drive, unmotivated").Drive);
            Assert.AreEqual(PriceIntentType.NoPrice, QueryParser.DetectPriceIntent(Cat, "price is not a concern").Type);
            Assert.IsNull(QueryParser.DetectPriceIntent(Cat, "under $99999 for sleep")); // amount out of range, no budget word
            Assert.AreEqual(Intent.Unknown, Q("kush").Intent); // names under 5 letters never fuzzy-match
            Assert.Throws<InvalidOperationException>(() => QueryParser.Parse(Catalog.Load(Read("batches.json"), Read("terpenes.json"), Read("engine_tables.json"), Read("pricing.json")), "sleep"));
        }

        static string Read(string f) => File.ReadAllText(Path.Combine(Application.dataPath, "_Game/Data/Catalog", f));
    }
}
