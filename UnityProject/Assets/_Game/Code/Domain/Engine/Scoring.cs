using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Dispo.Domain.Engine
{
    /// <summary>Scalar constants of the v7.11.4 engine (index.html md5 228684e9). Tables live in the catalog.</summary>
    public static class EngineConstants
    {
        public const double NF = 2.7765;                                   // L15121
        public const double DominantPct = 0.20, ActivePct = 0.05, SubPct = 0.01; // getTierW L15041
        public const double DominantW = 1.00, ActiveW = 0.25, SubW = 0.02;
        public const double DominantBonusSpan = 0.60;                      // scoreDomains L15186: 2x at ≥0.80%
        public const double BaSesqui = 0.46, BaDefault = 0.55;             // getBaScalar L15138
        public const int DisplayMin = 2, DisplayMax = 99;                  // scoreDomains L15199
        public const double HalfLifeWeeks = 8, RecencyCapWeeks = 20;       // averageProfile L15491
        public const double PrimaryWeight = 1.5, NegPenalty = 0.25;        // findStrains L15391, L15398
        public const int NewCustomerMaxAnx = 60;                           // applyProfileFilter L14830
        public const double FallbackCritFactor = 0.60; public const int FallbackCapAdd = 12; // respond L16640-16641
        public const int PainFunctionalCap = 55, PainSedationCritMax = 45; // _parseQueryCore L16213-16215
        public static readonly HashSet<string> PrimaryOnly = new HashSet<string> { DomainIds.Sedation, DomainIds.PainInflammation }; // L15388
    }

    public static class DomainIds
    {
        public const string Sedation = "sedation", Uplift = "uplift", AnxietyRelief = "anxiety_relief",
            PainInflammation = "pain_inflammation", FocusCognitive = "focus_cognitive", Antimicrobial = "antimicrobial";
    }

    /// <summary>JS number semantics the goldens depend on.</summary>
    public static class JsMath
    {
        /// <summary>Math.round: half rounds up (toward +∞).</summary>
        public static double Round(double x) => Math.Floor(x + 0.5);
        /// <summary>parseFloat(x.toFixed(dp)).</summary>
        public static double ToFixed(double x, int dp) =>
            // round-trip ("R") digits, not (decimal)x, which keeps only 15 significant digits
            (double)Math.Round(decimal.Parse(x.ToString("R", CultureInfo.InvariantCulture), NumberStyles.Float, CultureInfo.InvariantCulture), dp, MidpointRounding.AwayFromZero);
    }

    public struct ClusterResult { public int Primary; public int? Secondary; }

    public static class Scoring
    {
        /// <summary>getTierW L15041.</summary>
        public static double GetTierW(double p) =>
            p >= EngineConstants.DominantPct ? EngineConstants.DominantW :
            p >= EngineConstants.ActivePct ? EngineConstants.ActiveW :
            p >= EngineConstants.SubPct ? EngineConstants.SubW : 0;

        /// <summary>getBaScalar L15138.</summary>
        public static double GetBaScalar(Catalog cat, string id)
        {
            if (cat.BaScalars.TryGetValue(id, out var v)) return v;
            if (!cat.Terpenes.TryGetValue(id, out var t)) return EngineConstants.BaDefault;
            return t.Cls == "sesqui" ? EngineConstants.BaSesqui : EngineConstants.BaDefault;
        }

        /// <summary>scoreRaw L15338: Σ DB.d × tierW × dominant bonus × BA, / NF. Unclamped; used for ranking.</summary>
        public static Dictionary<string, double> ScoreRaw(Catalog cat, IReadOnlyDictionary<string, double> p)
        {
            var s = new Dictionary<string, double>();
            foreach (var d in cat.Domains)
            {
                double r = 0;
                foreach (var kv in p)
                {
                    if (!cat.Terpenes.TryGetValue(kv.Key, out var t)) continue;
                    double w = GetTierW(kv.Value);
                    if (w == 0) continue;
                    t.D.TryGetValue(d, out var v);
                    double b = 1;
                    if (kv.Value >= EngineConstants.DominantPct) b = 1 + Math.Min(1.0, (kv.Value - EngineConstants.DominantPct) / EngineConstants.DominantBonusSpan);
                    r += v * w * b * GetBaScalar(cat, kv.Key);
                }
                s[d] = r / EngineConstants.NF;
            }
            return s;
        }

        /// <summary>scoreDomains L15169: display score = clamp(round(raw × 100), 2, 99).</summary>
        public static Dictionary<string, int> ScoreDomains(Catalog cat, IReadOnlyDictionary<string, double> p)
        {
            // Same sum as scoreRaw; scoreDomains computes (r/NF)*100 from r, so reuse raw = r/NF.
            return ScoreRaw(cat, p).ToDictionary(kv => kv.Key,
                kv => (int)Math.Min(EngineConstants.DisplayMax, Math.Max(EngineConstants.DisplayMin, JsMath.Round(kv.Value * 100))));
        }

        static double P(IReadOnlyDictionary<string, double> p, string id) => p.TryGetValue(id, out var v) ? v : 0;

        /// <summary>CL[n].chk L15107-15115 (cluster rules are code in the source, so they are code here).</summary>
        static bool Chk(int id, IReadOnlyDictionary<string, double> p)
        {
            switch (id)
            {
                case 1: return P(p, "beta_myrcene") >= .50;
                case 2: return P(p, "beta_caryophyllene") >= .20 && P(p, "alpha_humulene") >= .08;
                case 3: return P(p, "beta_caryophyllene") >= .20 && P(p, "dl_limonene") >= .20;
                case 4: return P(p, "alpha_pinene") >= .20 || (P(p, "alpha_pinene") + P(p, "beta_pinene")) >= .35;
                case 5:
                    if (P(p, "trans_beta_ocimene") >= .30) return true;
                    double t = P(p, "terpinolene");
                    if (t < .15) return false;
                    var v = p.Values.Where(x => x > 0).OrderByDescending(x => x).ToList();
                    return v.Count > 1 && t >= v[1]; // JS: t>=undefined is false
                case 6: return P(p, "linalool") >= .20;
                default: return false;
            }
        }

        /// <summary>classifyCluster L15202: priority [4,5,6,2,3,1] with myrcene tiebreakers and BCP solo.</summary>
        public static ClusterResult ClassifyCluster(IReadOnlyDictionary<string, double> p)
        {
            var m = new[] { 4, 5, 6, 2, 3, 1 }.Where(id => Chk(id, p)).ToList();
            double myr = P(p, "beta_myrcene"), apin = P(p, "alpha_pinene"), lin = P(p, "linalool"),
                ocim = P(p, "trans_beta_ocimene"), terp = P(p, "terpinolene");

            if (m.Count > 0 && m[0] == 4)
            {
                if (myr >= 0.80 && myr > apin * 3) m.Remove(4);
                else if (apin < 0.20 && myr > apin * 3 && myr >= 0.50) m.Remove(4);
            }
            if (m.Count > 0 && m[0] == 5 && myr >= 0.80 && myr > Math.Max(ocim, terp) * 2) m.Remove(5);
            if (m.Count > 0 && m[0] == 6 && myr >= 0.80 && lin > 0 && myr > lin * 4.5) m.Remove(6);

            double bcp = P(p, "beta_caryophyllene"), hum = P(p, "alpha_humulene");
            if (bcp >= 0.50 && hum < 0.08 && !m.Contains(2)) m.Insert(0, 2);

            if (m.Count == 0) return new ClusterResult { Primary = myr >= 0.20 ? 1 : 7, Secondary = null };
            return new ClusterResult { Primary = m[0], Secondary = m.Count > 1 ? m[1] : (int?)null };
        }

        /// <summary>calcAnxietyRisk L15288: heuristic 15..88.</summary>
        public static int CalcAnxietyRisk(IReadOnlyDictionary<string, double> p)
        {
            double r = 50;
            double lin = P(p, "linalool"), bcp = P(p, "beta_caryophyllene"), apin = P(p, "alpha_pinene"), bisa = P(p, "alpha_bisabolol");
            r -= Math.Min(30, lin * 80);
            r -= Math.Min(25, bcp * 30);
            r -= Math.Min(12, apin * 60);
            r -= Math.Min(10, bisa * 70);
            r -= Math.Min(10, P(p, "beta_myrcene") * 8);
            double lim = P(p, "dl_limonene"), terp = P(p, "terpinolene"), ocim = P(p, "trans_beta_ocimene");
            double linBuffer = Math.Max(0, lin - 0.10);
            r += Math.Max(0, Math.Min(20, lim * 12 - linBuffer * 40));
            r += Math.Min(18, terp * 30);
            r += Math.Min(14, ocim * 25);
            return (int)Math.Min(88, Math.Max(15, JsMath.Round(r)));
        }

        /// <summary>
        /// averageProfile L15483 (+ profileIds L15475): in-stock batches only (all if none in stock),
        /// weight exp(−ln2/8 × min(20, weeks older than newest dated)); undated = oldest dated weight; 6 dp; zeros dropped.
        /// </summary>
        public static Dictionary<string, double> AverageProfile(IReadOnlyList<Batch> batches)
        {
            var avg = new Dictionary<string, double>();
            if (batches.Count == 0) return avg;
            var ids = batches.Where(b => b.InStock).ToList();
            if (ids.Count == 0) ids = batches.ToList();

            double k = Math.Log(2) / EngineConstants.HalfLifeWeeks;
            var known = ids.Where(b => b.TestDate.HasValue).Select(b => b.TestDate.Value).ToList();
            DateTime? newest = known.Count > 0 ? known.Max() : (DateTime?)null;
            DateTime? oldest = known.Count > 0 ? known.Min() : (DateTime?)null;
            var w = ids.Select(b =>
            {
                if (newest == null) return 1.0;
                var d = b.TestDate ?? oldest.Value;
                return Math.Exp(-k * Math.Min(EngineConstants.RecencyCapWeeks, (newest.Value - d).TotalMilliseconds / (1000.0 * 60 * 60 * 24 * 7)));
            }).ToList();
            double totalW = w.Sum();
            if (totalW == 0) totalW = 1;

            var totals = new Dictionary<string, double>();
            for (int i = 0; i < ids.Count; i++)
            {
                double wn = w[i] / totalW;
                foreach (var kv in ids[i].Terpenes)
                    totals[kv.Key] = (totals.TryGetValue(kv.Key, out var cur) ? cur : 0) + kv.Value * wn;
            }
            foreach (var kv in totals)
            {
                double v = JsMath.ToFixed(kv.Value, 6);
                if (v > 0) avg[kv.Key] = v;
            }
            return avg;
        }
    }
}
