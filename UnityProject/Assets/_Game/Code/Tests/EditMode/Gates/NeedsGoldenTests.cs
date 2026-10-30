using System.Collections.Generic;
using System.IO;
using System.Linq;
using Dispo.Domain.Engine;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Gates.Tests
{
    /// <summary>
    /// DATA-003: every query the Note-it-as picker can build from Data/Slice/SliceNeeds.json, replayed through the C# parser
    /// and responder with ParserOptions.Game, equals the parse and answer captured from the v7.11.4 tool with the game fixes
    /// (golden_cases_needs.json, Tools/Data/golden_game003.js). A mismatch is a Gate A finding: report it, do not fix it here.
    /// </summary>
    public class NeedsGoldenTests
    {
        const double Dp4 = 0.00005 + 1e-9;
        const int Dow = 4; // the goldens' pinned clock is a Thursday

        static Dictionary<string, object> O(object o) => (Dictionary<string, object>)o;
        static List<object> A(object o) => (List<object>)o;
        static Dictionary<string, int> Ints(object o) => O(o).ToDictionary(kv => kv.Key, kv => (int)(double)kv.Value);
        static object Get(Dictionary<string, object> d, string k) => d != null && d.TryGetValue(k, out var v) ? v : null;

        static Dictionary<string, object> _golden;
        static Dictionary<string, object> Golden => _golden ?? (_golden = O(Json.Parse(File.ReadAllText(Path.Combine(Application.dataPath, "../../Docs/Reconstruction/golden_cases_needs.json")))));
        static Dictionary<string, object> Needs => O(Json.Parse(File.ReadAllText(Path.Combine(Application.dataPath, "_Game/Data/Slice/SliceNeeds.json"))));
        static Catalog _cat;
        static Catalog Cat => _cat ?? (_cat = DpScenario.Data().Catalog);

        /// <summary>Mirrors pickerQueries in golden_game003.js: non-empty ordered component subsets, one term or said line each.</summary>
        static IEnumerable<string> Queries(Dictionary<string, object> need, string join)
        {
            var opts = A(need["components"]).Select(O).Select(c => A(c["terms"]).Select(t => (string)O(t)["text"])
                .Concat(O(c["say"]).Values.SelectMany(v => A(v).Cast<string>())).ToList()).ToList();
            for (int mask = 1; mask < 1 << opts.Count; mask++)
            {
                IEnumerable<List<string>> acc = new[] { new List<string>() };
                for (int i = 0; i < opts.Count; i++)
                    if ((mask & 1 << i) != 0) { var o = opts[i]; acc = acc.SelectMany(a => o.Select(x => a.Concat(new[] { x }).ToList())).ToList(); }
                foreach (var a in acc) yield return string.Join(join, a);
            }
        }

        [Test]
        public void Golden_CoversEveryPickerQuery()
        {
            var needs = A(Needs["needs"]).Select(O).ToList();
            var gold = A(Golden["needs"]).Select(O).ToDictionary(n => (string)n["id"]);
            var cases = new HashSet<string>(A(Golden["cases"]).Select(c => (string)O(c)["q"]));
            CollectionAssert.AreEquivalent(needs.Select(n => (string)n["id"]), gold.Keys, "need ids: regenerate golden_cases_needs.json");
            foreach (var n in needs)
            {
                var g = gold[(string)n["id"]];
                Assert.AreEqual(n["trueQuery"], g["trueQuery"], n["id"] + ": trueQuery");
                var want = Queries(n, (string)Needs["join"]).Select(q => q.Replace("{strain}", (string)g["strainFill"])).Distinct().ToList();
                CollectionAssert.AreEquivalent(want, A(g["queries"]).Cast<string>(), n["id"] + ": picker queries (regenerate the golden)");
                foreach (var q in want) Assert.IsTrue(cases.Contains(q), $"{n["id"]}: no golden for '{q}'");
            }
        }

        static IEnumerable<string> CaseQueries() => A(Golden["cases"]).Select(c => (string)O(c)["q"]);

        [TestCaseSource(nameof(CaseQueries))]
        public void ParseAndAnswer_EqualTool(string q)
        {
            var c = A(Golden["cases"]).Select(O).First(x => (string)x["q"] == q);
            var r = Responder.Ask(Cat, q, new ShopState(), Dow, ParserOptions.Game);
            var gp = O(c["parsed"]); var p = r.Parsed;
            Assert.AreEqual((string)gp["intent"], IntentName(p.Intent), "intent");
            if (p.Intent == Intent.Recommend)
            {
                CollectionAssert.AreEquivalent(Ints(gp["crit"]), p.Crit, "crit");
                CollectionAssert.AreEquivalent(Ints(gp["neg"]), p.Neg, "neg");
                Assert.AreEqual(Get(gp, "primary") as string, p.Primary, "primary");
                CollectionAssert.AreEqual(A(gp["lbls"]).Cast<string>().ToList(), p.Lbls, "lbls");
                Assert.AreEqual(Get(gp, "tf") as string, p.Tf, "tf");
                var opts = Get(gp, "opts") as Dictionary<string, object>;
                CollectionAssert.AreEqual(Get(opts, "exclude") == null ? null : A(opts["exclude"]).Cast<string>().ToList(), p.Opts.Exclude, "opts.exclude");
                Assert.AreEqual(Get(opts, "likeKey") as string, p.Opts.LikeKey, "opts.likeKey");
                Assert.AreEqual(Get(opts, "maxPrice") == null ? (double?)null : (double)opts["maxPrice"], p.Opts.MaxPrice, "opts.maxPrice");
            }
            Assert.AreEqual(Get(gp, "groupKey") as string, p.GroupKey, "groupKey");
            CollectionAssert.AreEqual(Get(gp, "strains") == null ? null : A(gp["strains"]).Cast<string>().ToList(), p.Strains, "strains");
            Assert.AreEqual(Get(gp, "terpene") as string, p.Terpene, "terpene");
            CollectionAssert.AreEqual(Get(gp, "excl") == null ? null : A(gp["excl"]).Cast<string>().ToList(), p.Excl?.Select(e => e.Name).ToList(), "excl");
            var pi = Get(gp, "priceIntent") as Dictionary<string, object>;
            Assert.AreEqual(pi == null ? null : (string)pi["type"], p.PriceIntent == null ? null : PriceName(p.PriceIntent.Type), "priceIntent");
            if (pi != null && pi.ContainsKey("amount")) Assert.AreEqual((int)(double)pi["amount"], p.PriceIntent.Amount, "budget");
            Assert.AreEqual((bool)gp["drive"], p.Drive, "drive");

            Assert.AreEqual((string)c["outcome"], OutcomeName(r.Outcome), "outcome");
            var calls = A(c["calls"]).Select(O).ToList();
            var mine = r.Recommend?.Calls ?? new List<FindCall>();
            Assert.AreEqual(calls.Count, mine.Count, "findStrains calls");
            for (int i = 0; i < calls.Count; i++)
            {
                CollectionAssert.AreEquivalent(Ints(calls[i]["crit"]), mine[i].Crit, $"call {i} crit");
                CollectionAssert.AreEquivalent(Ints(calls[i]["neg"]), mine[i].Neg, $"call {i} neg");
                var top = A(calls[i]["top"]).Select(O).ToList();
                CollectionAssert.AreEqual(top.Select(x => (string)x["key"]).ToList(), mine[i].Top.Select(s => s.Key).ToList(), $"call {i} ranking");
                for (int j = 0; j < top.Count; j++) Assert.AreEqual((double)top[j]["ms"], mine[i].Top[j].Ms, Dp4, $"call {i} #{j} ms");
            }
            CollectionAssert.AreEqual(A(c["shown"]).Cast<string>().ToList(), Shown(r), "shown");
            if (c.TryGetValue("roleTags", out var rt)) CollectionAssert.AreEqual(A(rt).Select(x => x as string).ToList(), r.RoleTags, "role tags");
            if (c.TryGetValue("exclNote", out var en)) Assert.AreEqual((string)en, r.Kind == ResponseKind.Strain ? r.CardExclNote : r.ExclNote?.Head, "excl note");
            if (c.TryGetValue("more", out var more))
                CollectionAssert.AreEqual(A(more).Cast<string>().ToList(), Responder.MoreOptions(Cat, p, new ShopState(), Shown(r)).Select(s => s.Key).ToList(), "show more");
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
}
