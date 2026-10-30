using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace Dispo.Domain.Engine
{
    /// <summary>Per-shift settings the tool keeps as page state (_prefs, _activeTiers, _customerProfile).</summary>
    public sealed class ShopState
    {
        public int ResultCount = 3;                                  // _prefs.resultCount L17517
        public HashSet<string> ActiveTiers = new HashSet<string>();  // tier chips L18594; empty = all
        public bool NewCustomer;                                     // _customerProfile === 'new'
        /// <summary>V73-NT5: true = v7.11.4 (an empty tier passes the House chip); false = game fix (matches no chip).</summary>
        public bool EmptyTierCountsAsHouse = true;
    }

    public sealed class IntentQuery
    {
        public Dictionary<string, int> Crit = new Dictionary<string, int>(), Neg = new Dictionary<string, int>();
        public string Primary, Label;
    }

    public sealed class StrainResult
    {
        public string Key, Name, Tier;
        public double Ms;
        public int Cluster, AnxietyRisk, BatchCount;
        public int? Cluster2;
        public bool InStock;
        public Dictionary<string, int> Domains;
        public Dictionary<string, double> Raw, Profile;
    }

    public enum Outcome { Ok, Fallback, None }

    public sealed class FindCall
    {
        public Dictionary<string, int> Crit, Neg;
        public List<StrainResult> Top;
    }

    public sealed class RecommendResult
    {
        public Outcome Outcome;
        public List<StrainResult> Strains;
        public List<FindCall> Calls = new List<FindCall>();
    }

    public static class Intents
    {
        // _parseQueryCore L16214 wantsSedation, applied to the intent key instead of the query text.
        static readonly Regex WantsSedation = new Regex(
            @"\b(heavy|heavier|sedating|sedation|knock.?out|couch.?lock|sleep|sleepy|don'?t care|don'?t mind|just knock|pass out|bed.?time|night.?time|night)\b");

        /// <summary>
        /// Direct INTENTS lookup (L15619) for an NPC-emitted key, then the parser's single-key rules:
        /// conflict resolution L16200 (no negation hints, so the positive request wins) and pain-functional default L16211.
        /// Returns null for an unknown key.
        /// </summary>
        public static IntentQuery Resolve(Catalog cat, string key, bool painFunctional = true)
        {
            if (!cat.Intents.TryGetValue(key, out var e)) return null;
            var q = new IntentQuery { Crit = new Dictionary<string, int>(e.D), Neg = new Dictionary<string, int>(e.Neg), Primary = e.Primary, Label = e.Label };
            foreach (var d in q.Neg.Keys.ToList())
                if (q.Crit.TryGetValue(d, out var c) && q.Neg[d] <= c + 5) q.Neg.Remove(d);
            if (q.Primary != null && !q.Crit.ContainsKey(q.Primary))
            {
                q.Primary = null; int best = 0;
                foreach (var kv in q.Crit) if (kv.Value > best) { best = kv.Value; q.Primary = kv.Key; }
            }
            if (q.Crit.TryGetValue(DomainIds.PainInflammation, out var pain) && pain != 0 && !q.Neg.ContainsKey(DomainIds.Sedation)
                && !(q.Crit.TryGetValue(DomainIds.Sedation, out var sed) && sed >= EngineConstants.PainSedationCritMax)
                && painFunctional && !WantsSedation.IsMatch(key))
                q.Neg[DomainIds.Sedation] = EngineConstants.PainFunctionalCap;
            return q;
        }
    }

    public static class Recommender
    {
        /// <summary>analyzeGroup L15516 (scoring parts only; the age badge is display).</summary>
        public static StrainResult AnalyzeGroup(Catalog cat, StrainGroup g)
        {
            var p = Scoring.AverageProfile(g.Batches);
            var cl = Scoring.ClassifyCluster(p);
            var rep = g.Batches[0];
            int live = g.Batches.Count(b => b.InStock); // profileIds L15475
            return new StrainResult
            {
                Key = g.Key, Name = g.Name, Tier = rep.Tier, InStock = rep.InStock,
                BatchCount = live > 0 ? live : g.Batches.Count,
                Profile = p, Domains = Scoring.ScoreDomains(cat, p), Raw = Scoring.ScoreRaw(cat, p),
                Cluster = cl.Primary, Cluster2 = cl.Secondary, AnxietyRisk = Scoring.CalcAnxietyRisk(p),
            };
        }

        /// <summary>findStrains L15355 (slice: no exclusions, like-X, maxAnx, exclude or maxPrice options).</summary>
        public static List<StrainResult> FindStrains(Catalog cat, IReadOnlyDictionary<string, int> crit, IReadOnlyDictionary<string, int> neg,
            string primary, ShopState state)
        {
            var results = new List<StrainResult>();
            foreach (var g in cat.Groups())
            {
                var rep = g.Batches[0];
                if (!rep.InStock) continue;
                if (state.ActiveTiers.Count > 0)
                {
                    string t = string.IsNullOrEmpty(rep.Tier) ? (state.EmptyTierCountsAsHouse ? "house" : null) : rep.Tier;
                    if (t == null || !state.ActiveTiers.Contains(t)) continue;
                }
                var a = AnalyzeGroup(cat, g);
                int Disp(string d) => a.Domains.TryGetValue(d, out var v) ? v : 0;
                if (!crit.All(kv => Disp(kv.Key) >= kv.Value) || !neg.All(kv => Disp(kv.Key) <= kv.Value)) continue;

                double ms = 0;
                foreach (var kv in crit)
                {
                    if (primary != null && EngineConstants.PrimaryOnly.Contains(primary) && kv.Key != primary) continue;
                    a.Raw.TryGetValue(kv.Key, out var raw);
                    ms += raw * (kv.Key == primary ? EngineConstants.PrimaryWeight : 1.0);
                }
                foreach (var kv in neg)
                {
                    int actual = Disp(kv.Key);
                    if (actual > 0 && kv.Value > 0) ms -= (double)actual / kv.Value * EngineConstants.NegPenalty;
                }
                if (cat.ClusterBonus.TryGetValue(a.Cluster, out var bonus))
                    foreach (var kv in bonus) if (crit.ContainsKey(kv.Key)) ms += kv.Value;
                if (!string.IsNullOrEmpty(rep.Tier) && cat.TierNudge.TryGetValue(rep.Tier, out var nudge)) ms += nudge;
                if (state.NewCustomer)
                {
                    a.Profile.TryGetValue("beta_myrcene", out var myr);
                    ms -= myr >= 1.20 ? 0.45 : myr >= 0.80 ? 0.22 : 0; // L15420
                }
                a.Ms = ms;
                results.Add(a);
            }
            if (state.NewCustomer) results = results.Where(r => r.AnxietyRisk <= EngineConstants.NewCustomerMaxAnx).ToList(); // applyProfileFilter L14827
            return results.OrderByDescending(r => r.Ms).Take(state.ResultCount).ToList(); // stable, like V8 sort
        }

        /// <summary>respond L16637-16646: findStrains, then one relaxed retry (crit × 0.60 floored, caps +12 ≤ 99).</summary>
        public static RecommendResult Recommend(Catalog cat, IReadOnlyDictionary<string, int> crit, IReadOnlyDictionary<string, int> neg,
            string primary, ShopState state)
        {
            var res = new RecommendResult();
            var top = Call(res, cat, crit.ToDictionary(kv => kv.Key, kv => kv.Value), neg.ToDictionary(kv => kv.Key, kv => kv.Value), primary, state);
            if (top.Count > 0) { res.Outcome = Outcome.Ok; res.Strains = top; return res; }
            var c2 = crit.ToDictionary(kv => kv.Key, kv => (int)Math.Floor(kv.Value * EngineConstants.FallbackCritFactor));
            var n2 = neg.ToDictionary(kv => kv.Key, kv => Math.Min(EngineConstants.DisplayMax, kv.Value + EngineConstants.FallbackCapAdd));
            top = Call(res, cat, c2, n2, primary, state);
            res.Outcome = top.Count > 0 ? Outcome.Fallback : Outcome.None;
            res.Strains = top;
            return res;
        }

        static List<StrainResult> Call(RecommendResult res, Catalog cat, Dictionary<string, int> crit, Dictionary<string, int> neg, string primary, ShopState state)
        {
            var top = FindStrains(cat, crit, neg, primary, state);
            res.Calls.Add(new FindCall { Crit = crit, Neg = neg, Top = top });
            return top;
        }
    }
}
