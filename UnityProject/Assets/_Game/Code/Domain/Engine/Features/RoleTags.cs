using System.Collections.Generic;
using System.Linq;

namespace Dispo.Domain.Engine
{
    /// <summary>buildRoleTags L16264: card 1 = best_match; each later card takes the first unused role. Ids as in ROLE_CFG L16253.</summary>
    public static class RoleTags
    {
        public const string BestMatch = "best_match", MostSedating = "most_sedating", MostFunctional = "most_functional",
            MostUplifting = "most_uplifting", LowestAnxiety = "lowest_anxiety", MostPain = "most_pain", MostFocus = "most_focus", Gentle = "gentle";

        /// <summary>ROLE_CFG labels L16254-16261.</summary>
        public static readonly IReadOnlyDictionary<string, string> Labels = new Dictionary<string, string>
        {
            { BestMatch, "Best match" }, { MostSedating, "Heaviest body" }, { MostFunctional, "Most functional" }, { MostUplifting, "More uplifting" },
            { LowestAnxiety, "Lowest anxiety" }, { MostPain, "Strongest pain relief" }, { MostFocus, "Most focus" }, { Gentle, "Mildest option" },
        };

        static readonly string[] DomIds = { DomainIds.Sedation, DomainIds.Uplift, DomainIds.AnxietyRelief, DomainIds.PainInflammation, DomainIds.FocusCognitive };
        static readonly Dictionary<string, string> RoleOf = new Dictionary<string, string>
        {
            { DomainIds.Sedation, MostSedating }, { DomainIds.Uplift, MostUplifting }, { DomainIds.PainInflammation, MostPain }, { DomainIds.FocusCognitive, MostFocus },
        };

        /// <summary>One tag per result; all null when fewer than 2 results (L16265).</summary>
        public static List<string> Build(IReadOnlyList<StrainResult> results, string primary)
        {
            int n = results.Count;
            var tags = new List<string>(new string[n]);
            if (n < 2) return tags;
            tags[0] = BestMatch;
            var used = new HashSet<string> { BestMatch };
            var reference = results[0];
            int D(StrainResult s, string d) => s.Domains.TryGetValue(d, out var v) ? v : 0;
            int minAnx = results.Aggregate(100, (mn, x) => System.Math.Min(mn, x.AnxietyRisk));
            for (int i = 1; i < n; i++)
            {
                var a = results[i];
                string best = null; int bestDelta = 0;
                foreach (var d in DomIds) // 1. largest domain delta > 4 vs #1
                {
                    int delta = D(a, d) - D(reference, d);
                    if (delta > 4 && RoleOf.TryGetValue(d, out var r) && !used.Contains(r) && delta > bestDelta) { best = r; bestDelta = delta; }
                }
                if (best == null && D(reference, DomainIds.Sedation) - D(a, DomainIds.Sedation) > 5 && !used.Contains(MostFunctional)) best = MostFunctional; // 2
                if (best == null && a.AnxietyRisk < reference.AnxietyRisk - 6 && !used.Contains(LowestAnxiety)) best = LowestAnxiety; // 3
                if (best == null && primary != null && System.Math.Abs(D(a, primary) - D(reference, primary)) < 5) // 4. primary tie → secondary
                {
                    string sec = null; int secDelta = 0;
                    foreach (var d in DomIds.Where(d => d != primary))
                    {
                        int delta = D(a, d) - D(reference, d);
                        if (delta > secDelta) { secDelta = delta; sec = d; }
                    }
                    if (sec != null && secDelta > 4 && RoleOf.TryGetValue(sec, out var r) && !used.Contains(r)) best = r;
                }
                if (best == null && !used.Contains(LowestAnxiety) && a.AnxietyRisk <= minAnx) best = LowestAnxiety; // 5
                best = best ?? Gentle;
                tags[i] = best;
                used.Add(best);
            }
            return tags;
        }
    }
}
