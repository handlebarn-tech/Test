using System.Collections.Generic;

namespace Dispo.Domain.Engine
{
    /// <summary>Display labels copied from v7.11.4 (GAME-002 S2). Text only; no scoring uses them.</summary>
    public static class Labels
    {
        /// <summary>CL[n].lbl L15107-15115 (classifyCluster result → card label).</summary>
        static readonly Dictionary<int, string> Cluster = new Dictionary<int, string>
        {
            { 1, "Myrcene-Forward / Body" }, { 2, "Anti-Inflammatory" }, { 3, "Balanced Hybrid" }, { 4, "Cognitive Clarity" },
            { 5, "Creative / Cerebral" }, { 6, "Anxiety / Mental Calm" }, { 7, "Multi-Domain / Minor Terps" },
        };

        /// <summary>CL[n].name L15107-15115.</summary>
        static readonly Dictionary<int, string> ClusterNames = new Dictionary<int, string>
        {
            { 1, "Myrcene-Dominant" }, { 2, "BCP Sesquiterpene" }, { 3, "BCP / Limonene" }, { 4, "Pinene-Dominant" },
            { 5, "Terpinolene / Ocimene" }, { 6, "Linalool-Anchored" }, { 7, "Complex Minor Terpene" },
        };

        /// <summary>tierLabels2 defaults L16463 (TIER_LABELS overrides are empty in local mode).</summary>
        static readonly Dictionary<string, string> Tiers = new Dictionary<string, string>
        {
            { "smalls", "House Smalls" }, { "house", "House Fresh" }, { "premium", "TFS Premium" }, { "fttp", "FttP" },
            { "t1", "Tier 1" }, { "t2", "Tier 2" }, { "t3", "Tier 3" }, { "t4", "Tier 4" },
        };

        public static string ClusterLabel(int cluster) => Cluster.TryGetValue(cluster, out var s) ? s : "";
        public static string ClusterName(int cluster) => ClusterNames.TryGetValue(cluster, out var s) ? s : "";
        /// <summary>L16464: unknown or empty tier → "".</summary>
        public static string TierLabel(string tier) => Tiers.TryGetValue(tier ?? "", out var s) ? s : "";
    }
}
