using System;
using System.Collections.Generic;
using System.Linq;

namespace Dispo.Domain.Engine
{
    public sealed class SimilarResult
    {
        public StrainResult Strain;
        public double Sim;
    }

    public static class Similarity
    {
        /// <summary>slCosineSim L20813: cosine over the union of terpene keys; 0 if either profile is empty.</summary>
        public static double Cosine(IReadOnlyDictionary<string, double> pA, IReadOnlyDictionary<string, double> pB)
        {
            double dot = 0, na = 0, nb = 0;
            foreach (var k in pA.Keys.Concat(pB.Keys.Where(k => !pA.ContainsKey(k))))
            {
                double a = pA.TryGetValue(k, out var x) ? x : 0, b = pB.TryGetValue(k, out var y) ? y : 0;
                dot += a * b; na += a * a; nb += b * b;
            }
            if (na == 0 || nb == 0) return 0;
            return dot / (Math.Sqrt(na) * Math.Sqrt(nb));
        }

        /// <summary>
        /// Similar tab slRunEngine L20841-20866: blended profile = plain mean of the liked strains' averaged profiles;
        /// candidates = in-stock, not liked, sim &gt; 0, best first, top 6. Unknown keys contribute an empty profile, like the tool.
        /// </summary>
        public static List<SimilarResult> Similar(Catalog cat, IReadOnlyList<string> likedKeys, int n = 6)
        {
            if (likedKeys.Count == 0) return new List<SimilarResult>();
            var blended = new Dictionary<string, double>();
            foreach (var key in likedKeys)
            {
                var g = cat.Group(key);
                var p = g == null ? new Dictionary<string, double>() : Scoring.AverageProfile(g.Batches);
                foreach (var kv in p) blended[kv.Key] = (blended.TryGetValue(kv.Key, out var v) ? v : 0) + kv.Value;
            }
            foreach (var k in blended.Keys.ToList()) blended[k] /= likedKeys.Count;
            return cat.Groups().Where(g => !likedKeys.Contains(g.Key) && g.Batches[0].InStock)
                .Select(g => { var a = Recommender.AnalyzeGroup(cat, g); return new SimilarResult { Strain = a, Sim = Cosine(blended, a.Profile) }; })
                .Where(x => x.Sim > 0).OrderByDescending(x => x.Sim).Take(n).ToList();
        }
    }
}
