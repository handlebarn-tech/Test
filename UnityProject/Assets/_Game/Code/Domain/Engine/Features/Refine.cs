using System;
using System.Collections.Generic;
using System.Linq;

namespace Dispo.Domain.Engine
{
    /// <summary>
    /// Refine chips REFINE L19583 + refineSearch L19596: edit the previous search's numbers, then drop a crit its cap no longer
    /// clears by 5, re-pick the primary, and append the chip label. In the game these are follow-up dialogue options.
    /// </summary>
    public static class Refine
    {
        public static readonly IReadOnlyDictionary<string, string> Labels = new Dictionary<string, string>
        {
            { "lighter", "something lighter" }, { "heavier", "more sedating" }, { "addPain", "add pain relief" }, { "addSleep", "add sleep support" },
            { "lowerAnx", "lower anxiety risk" }, { "moreEnergy", "more energetic" }, { "functional", "keep it functional" }, { "moreBody", "more body" },
            { "addFocus", "add focus" }, { "moreUplift", "more uplifting" }, { "addAnx", "add anxiety relief" },
        };

        /// <summary>Apply a REFINE key to a responded query (its Opts hold the effective options, as _regParsed stores them).</summary>
        public static ParsedQuery Apply(ParsedQuery b, string key)
        {
            if (!Labels.TryGetValue(key, out var lbl)) throw new ArgumentException("unknown refine key " + key);
            var crit = new Dictionary<string, int>(b.Crit); var neg = new Dictionary<string, int>(b.Neg);
            var opts = b.Opts?.Clone() ?? new FindOptions();
            void Mx(Dictionary<string, int> d, string k, int v) => d[k] = Math.Max(d.TryGetValue(k, out var x) ? x : 0, v); // _mx
            void Mn(Dictionary<string, int> d, string k, int v) => d[k] = d.TryGetValue(k, out var x) ? Math.Min(x, v) : v; // _mn
            const string sed = DomainIds.Sedation;
            switch (key)
            {
                case "lighter": crit = QueryParser.Without(crit, sed); Mn(neg, sed, 40); if (crit.Count == 0) crit[DomainIds.AnxietyRelief] = 30; break;
                case "heavier": Mx(crit, sed, 50); neg = QueryParser.Without(neg, sed); break;
                case "addPain": Mx(crit, DomainIds.PainInflammation, 40); break;
                case "addSleep": Mx(crit, sed, 40); neg = QueryParser.Without(neg, sed); break;
                case "lowerAnx": opts.MaxAnx = 42; break;
                case "moreEnergy": crit = QueryParser.Without(crit, sed); Mn(neg, sed, 38); Mx(crit, DomainIds.Uplift, 25); break;
                case "functional": crit = QueryParser.Without(crit, sed); Mn(neg, sed, 40); break;
                case "moreBody":
                    Mx(crit, sed, 25); Mx(crit, DomainIds.PainInflammation, 25);
                    if (neg.TryGetValue(sed, out var ns) && ns < 55) neg[sed] = 55;
                    break;
                case "addFocus": Mx(crit, DomainIds.FocusCognitive, 20); break;
                case "moreUplift": Mx(crit, DomainIds.Uplift, 28); break;
                case "addAnx": Mx(crit, DomainIds.AnxietyRelief, 40); break;
            }
            foreach (var d in neg.Keys.ToList()) if (crit.TryGetValue(d, out var c) && neg[d] <= c + 5) crit = QueryParser.Without(crit, d); // L19601
            string primary = b.Primary != null && crit.ContainsKey(b.Primary) ? b.Primary : QueryParser.BestDomain(crit);
            return new ParsedQuery
            {
                Intent = Intent.Recommend, Crit = crit, Neg = neg, Primary = primary, Tf = b.Tf, Opts = opts,
                Lbls = b.Lbls.Where(x => !string.IsNullOrEmpty(x)).Concat(new[] { lbl }).ToList(),
            };
        }
    }
}
