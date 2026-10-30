using System;
using System.Collections.Generic;
using System.Linq;

namespace Dispo.Domain.Engine
{
    public enum ResponseKind { Recommend, Strain, Compare, TerpeneRank, PriceOnly, Help }

    /// <summary>Ok/Fallback/None as respond's recommend; ExcludedAll = no strain verified clear; NotFound = unknown strain/terpene.</summary>
    public enum ResponseOutcome { Ok, Fallback, None, ExcludedAll, Help, NotFound }

    public sealed class CompareResult
    {
        public List<StrainResult> Strains;
        public string KeyDomain, KeyLabel, Winner; // winner = strain name
        public int Diff;
        public bool Notably => Diff >= 10;
        /// <summary>"Kush Cake scores notably higher (12 pts)" (L16562).</summary>
        public string Line => $"{Winner} scores {(Notably ? "notably " : "")}higher ({Diff} pts)";
    }

    public sealed class TerpRankRow
    {
        public string Key, Name;
        public double Pct;
        public int BatchCount;
    }

    public sealed class QueryResponse
    {
        public ParsedQuery Parsed;
        public ResponseKind Kind;
        public ResponseOutcome Outcome;
        public bool DriveNotice;                 // L19557
        public ExclusionNote ExclNote;           // recommend / terpene rank
        // Recommend
        public RecommendResult Recommend;
        public List<StrainResult> Strains = new List<StrainResult>();
        public List<string> RoleTags = new List<string>(); // per strain; the tool shows them only when Outcome == Ok
        public bool AskEffectForBudget;          // a budget but no effect (L16662)
        // Strain lookup
        public StrainResult Card;
        public ExclStatus CardExcl = ExclStatus.Clear;
        /// <summary>The strain card's exclusion line (L16548), or null when the strain is clear.</summary>
        public string CardExclNote;
        public List<StrainResult> Near = new List<StrainResult>(); // OOS card: in stock and close to it (Ms = cosine)
        // Compare / terpene rank / price only
        public CompareResult Compare;
        public List<TerpRankRow> TerpRank;
        public List<(string Name, double Grams, double Post)> LowestPrices; // price-only "budget"
    }

    /// <summary>respond L16539-16678 without HTML: routes a parsed query to strain lookup, compare, terpene rank, price-only or recommend.</summary>
    public static class Responder
    {
        /// <summary>DOMS labels L15042 (antimicrobial is never compared).</summary>
        public static readonly IReadOnlyList<(string Id, string Label)> DomainLabels = new[]
        {
            (DomainIds.Sedation, "Sedation"), (DomainIds.Uplift, "Uplift"), (DomainIds.AnxietyRelief, "Anxiety Relief"),
            (DomainIds.PainInflammation, "Pain / Inflam"), (DomainIds.FocusCognitive, "Focus / Cogn"),
        };

        /// <summary>Parse + respond, i.e. the tool's submit(q) (L19542).</summary>
        public static QueryResponse Ask(Catalog cat, string q, ShopState state, int dow, ParserOptions o = null) =>
            Respond(cat, QueryParser.Parse(cat, q, o), state, dow);

        public static QueryResponse Respond(Catalog cat, ParsedQuery p, ShopState state, int dow)
        {
            var r = new QueryResponse { Parsed = p, DriveNotice = p.Drive };
            switch (p.Intent)
            {
                case Intent.Strain: return StrainLookup(cat, p, state, r);
                case Intent.Compare: return CompareStrains(cat, p, r);
                case Intent.TerpeneRank: return TerpeneRank(cat, p, state, r);
                case Intent.Recommend: return RecommendFor(cat, p, state, dow, r);
            }
            if (p.PriceIntent != null) return PriceOnly(cat, p, state, dow, r);
            r.Kind = ResponseKind.Help; r.Outcome = ResponseOutcome.Help;
            return r;
        }

        static QueryResponse StrainLookup(Catalog cat, ParsedQuery p, ShopState state, QueryResponse r) // L16541-16554
        {
            r.Kind = ResponseKind.Strain;
            var g = cat.Group(p.GroupKey);
            if (g == null) { r.Outcome = ResponseOutcome.NotFound; return r; }
            var ex = p.Excl != null && p.Excl.Count > 0 ? p.Excl : null;
            r.Card = Recommender.AnalyzeGroup(cat, g);
            r.CardExcl = ex == null ? ExclStatus.Clear : Exclusions.Status(g, ex);
            string nm = ex == null ? "" : string.Join(" or ", ex.Select(e => e.Name));
            if (r.CardExcl == ExclStatus.Contains) r.CardExclNote = $"{r.Card.Name} contains {nm}.";
            else if (r.CardExcl == ExclStatus.Unknown) r.CardExclNote = $"{r.Card.Name} has no {nm} result on file, so it is not verified free of {nm}.";
            r.Outcome = ResponseOutcome.Ok;
            if (g.Batches[0].InStock) return r;
            r.Near = cat.Groups().Where(k => k.Key != g.Key && k.Batches[0].InStock && (ex == null || Exclusions.Status(k, ex) == ExclStatus.Clear))
                .Select(k => { var b = Recommender.AnalyzeGroup(cat, k); b.Ms = Similarity.Cosine(r.Card.Profile, b.Profile); return b; })
                .OrderByDescending(b => b.Ms).Take(state.ResultCount > 0 ? state.ResultCount : 3).ToList();
            return r;
        }

        static QueryResponse CompareStrains(Catalog cat, ParsedQuery p, QueryResponse r) // L16556-16563
        {
            r.Kind = ResponseKind.Compare;
            var groups = p.Strains.Select(cat.Group).ToList();
            if (groups.Any(g => g == null)) { r.Outcome = ResponseOutcome.NotFound; return r; }
            var a = groups.Select(g => Recommender.AnalyzeGroup(cat, g)).ToList();
            var bd = DomainLabels.Select(d => { var v = a.Select(x => x.Domains[d.Id]).ToList(); return (d.Id, d.Label, Diff: v.Max() - v.Min()); })
                .OrderByDescending(x => x.Diff).First();
            var winner = a.Aggregate((w, x) => x.Domains[bd.Id] > w.Domains[bd.Id] ? x : w);
            r.Compare = new CompareResult { Strains = a, KeyDomain = bd.Id, KeyLabel = bd.Label, Diff = bd.Diff, Winner = winner.Name };
            r.Outcome = ResponseOutcome.Ok;
            return r;
        }

        static QueryResponse TerpeneRank(Catalog cat, ParsedQuery p, ShopState state, QueryResponse r) // L16565-16592
        {
            r.Kind = ResponseKind.TerpeneRank;
            if (!cat.Terpenes.ContainsKey(p.Terpene)) { r.Outcome = ResponseOutcome.NotFound; return r; }
            r.TerpRank = cat.Groups().Where(g => g.Batches[0].InStock && Recommender.PassesTierChips(g.Batches[0], state)
                    && (p.Excl == null || Exclusions.Status(g, p.Excl) == ExclStatus.Clear))
                .Select(g =>
                {
                    var live = g.Batches.Count(b => b.InStock);
                    var prof = Scoring.AverageProfile(g.Batches);
                    return new TerpRankRow { Key = g.Key, Name = g.Name, Pct = prof.TryGetValue(p.Terpene, out var v) ? v : 0, BatchCount = live > 0 ? live : g.Batches.Count };
                })
                .Where(x => x.Pct > 0).OrderByDescending(x => x.Pct).ToList();
            if (p.Excl != null) r.ExclNote = Exclusions.Note(cat, p.Excl, state);
            r.Outcome = r.ExclNote != null && r.ExclNote.Clear == 0 ? ResponseOutcome.ExcludedAll : ResponseOutcome.Ok;
            if (r.Outcome == ResponseOutcome.ExcludedAll) r.TerpRank = new List<TerpRankRow>();
            return r;
        }

        static QueryResponse PriceOnly(Catalog cat, ParsedQuery p, ShopState state, int dow, QueryResponse r) // L16595-16612
        {
            r.Kind = ResponseKind.PriceOnly; r.Outcome = ResponseOutcome.Ok;
            if (p.PriceIntent.Type == PriceIntentType.Budget && Pricing.HasPricingConfigured(cat.Pricing))
                r.LowestPrices = cat.Groups().Where(g => g.Batches[0].InStock && Recommender.PassesTierChips(g.Batches[0], state))
                    .Select(g => (g.Name, c: Pricing.CheapestPostTax(cat.Pricing, Pricing.GetEffectivePrices(cat.Pricing, g.Batches[0].Tier ?? "", g.Batches[0].Brand ?? "", g.Name, dow))))
                    .Where(x => x.c != null).OrderBy(x => x.c.Value.Post).Take(3).Select(x => (x.Name, x.c.Value.Grams, x.c.Value.Post)).ToList();
            return r;
        }

        static QueryResponse RecommendFor(Catalog cat, ParsedQuery p, ShopState state, int dow, QueryResponse r) // L16616-16675
        {
            r.Kind = ResponseKind.Recommend;
            var opts = p.Opts?.Clone() ?? new FindOptions();
            p.Opts = opts; // the tool writes the effective opts back onto the parsed query (L16631); refine reads them
            opts.Dow = dow;
            if (p.PriceIntent?.Type == PriceIntentType.HasBudget && Pricing.HasPricingConfigured(cat.Pricing)) opts.MaxPrice = p.PriceIntent.Amount;
            if (p.Excl != null && p.Excl.Count > 0)
            {
                opts.Excl = p.Excl;
                r.ExclNote = Exclusions.Note(cat, p.Excl, state);
                if (r.ExclNote.Clear == 0) { r.Outcome = ResponseOutcome.ExcludedAll; return r; }
            }
            r.Recommend = Recommender.Recommend(cat, p.Crit, p.Neg, p.Primary, state, opts, p.Tf);
            r.Strains = r.Recommend.Strains;
            r.Outcome = r.Recommend.Outcome == Outcome.Ok ? ResponseOutcome.Ok : r.Recommend.Outcome == Outcome.Fallback ? ResponseOutcome.Fallback : ResponseOutcome.None;
            r.RoleTags = RoleTags.Build(r.Strains, p.Primary); // also on fallback results, which the tool renders without tags (L16645)
            r.AskEffectForBudget = r.Outcome == ResponseOutcome.Ok && p.PriceIntent?.Type == PriceIntentType.HasBudget && p.Crit.Count == 0;
            return r;
        }

        /// <summary>"Show more options" showMoreOptions L19442: rerun with n=40, tf re-sort, next 3 not yet shown.</summary>
        public static List<StrainResult> MoreOptions(Catalog cat, ParsedQuery p, ShopState state, IReadOnlyCollection<string> shownKeys, int take = 3)
        {
            var wide = new ShopState { ResultCount = 40, ActiveTiers = state.ActiveTiers, NewCustomer = state.NewCustomer, EmptyTierCountsAsHouse = state.EmptyTierCountsAsHouse };
            var all = Recommender.FindStrains(cat, p.Crit, p.Neg, p.Primary, wide, p.Opts);
            if (p.Tf != null) all = all.OrderByDescending(x => x.Profile.TryGetValue(p.Tf, out var v) ? v : 0).ToList();
            return all.Where(x => !shownKeys.Contains(x.Key)).Take(take).ToList();
        }
    }
}
