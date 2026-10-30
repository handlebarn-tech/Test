using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Dispo.Domain.Engine
{
    public enum ExclStatus { Clear, Contains, Unknown }

    /// <summary>What an exclusion left out, over in-stock groups in the active tiers (exclNote L16524).</summary>
    public sealed class ExclusionNote
    {
        public int Clear, Contains, Unknown;
        public string Names; // "A or B"
        /// <summary>The note's bold head line, as the tool words it.</summary>
        public string Head => Clear > 0
            ? $"Without {Names}: showing only strains whose lab results show under {QueryParser.ExclMaxPct.ToString(CultureInfo.InvariantCulture)}% or not detected in every in-stock batch."
            : $"No in-stock strain is verified free of {Names}.";
    }

    public static class Exclusions
    {
        /// <summary>
        /// exclStatus L16001 over the group's profile batches (in stock, or all when none is): contains if any value ≥ EXCL_MAX_PCT,
        /// else unknown if any value is missing (a missing lab value is never "absent"), else clear. Tested-ND zeros count as absent.
        /// </summary>
        public static ExclStatus Status(StrainGroup g, IReadOnlyList<Exclusion> excl)
        {
            bool unknown = false;
            var live = g.Batches.Where(b => b.InStock).ToList();
            foreach (var b in live.Count > 0 ? live : g.Batches)
                foreach (var e in excl)
                    foreach (var t in e.Ids)
                    {
                        if (!b.Terpenes.TryGetValue(t, out var v)) unknown = true;
                        else if (v >= QueryParser.ExclMaxPct) return ExclStatus.Contains;
                    }
            return unknown ? ExclStatus.Unknown : ExclStatus.Clear;
        }

        public static ExclusionNote Note(Catalog cat, IReadOnlyList<Exclusion> excl, ShopState state)
        {
            var n = new ExclusionNote { Names = string.Join(" or ", excl.Select(e => e.Name)) };
            foreach (var g in cat.Groups())
            {
                var rep = g.Batches[0];
                if (!rep.InStock || !Recommender.PassesTierChips(rep, state)) continue;
                switch (Status(g, excl))
                {
                    case ExclStatus.Clear: n.Clear++; break;
                    case ExclStatus.Contains: n.Contains++; break;
                    default: n.Unknown++; break;
                }
            }
            return n;
        }
    }
}
