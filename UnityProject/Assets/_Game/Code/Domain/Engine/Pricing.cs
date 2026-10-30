using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Dispo.Domain.Engine
{
    public sealed class Deal
    {
        public string Id, Name, TargetType, TargetValue, DealType;
        public bool Active;
        public double Weight, FlatPrice;
        public Dictionary<double, double> W;
        // Not in the default deals; set by code (store settings). L21184-21238
        public List<string> TargetValues;      // multiTier
        public int? Day;                       // custom deals: only on this dow
        public double Pct, OzOverride;         // pct_msrp
        public List<double> ExcludeWeights;    // pct_msrp
        public string BaseTier, UseTier;       // pct_msrp, use_tier
    }

    /// <summary>_pricing.strainOverrides entry L21150: a strain name priced as another tier.</summary>
    public sealed class StrainOverride { public string Name, Tier; }

    /// <summary>TIER_DEFAULTS L21018, DEFAULT_DAY_DEALS L21036, taxRate L21062 (pricing.json).</summary>
    public sealed class PriceTables
    {
        public double TaxRate;
        public List<double> Weights;
        public Dictionary<string, Dictionary<double, double>> Tiers;
        public Dictionary<int, List<Deal>> DayDeals;
        // Store settings with no rows in the snapshot (MIG-001 §12); empty unless code fills them.
        public List<StrainOverride> StrainOverrides = new List<StrainOverride>();
        public List<Deal> CustomDeals = new List<Deal>();
        /// <summary>_brands[].pricingClass ('house' | 'fttp'; anything else = 'tier'), by brand name.</summary>
        public Dictionary<string, string> BrandPricingClass = new Dictionary<string, string>();

        static Dictionary<double, double> WeightMap(object o) =>
            Catalog.Obj(o).ToDictionary(kv => double.Parse(kv.Key, CultureInfo.InvariantCulture), kv => (double)kv.Value);

        internal static PriceTables FromJson(Dictionary<string, object> j) => new PriceTables
        {
            TaxRate = (double)j["taxRate"],
            Weights = Catalog.Arr(j["weights"]).Select(x => (double)x).ToList(),
            Tiers = Catalog.Arr(j["tiers"]).Select(Catalog.Obj).ToDictionary(t => (string)t["id"], t => WeightMap(t["w"])),
            DayDeals = Catalog.Arr(j["dayDeals"]).Select(Catalog.Obj).ToDictionary(d => (int)(double)d["dow"],
                d => Catalog.Arr(d["deals"]).Select(Catalog.Obj).Select(x =>
                {
                    var tgt = Catalog.Obj(x["target"]);
                    return new Deal
                    {
                        Id = (string)x["id"], Name = (string)x["name"], Active = (bool)x["active"],
                        TargetType = (string)tgt["type"], TargetValue = tgt.TryGetValue("value", out var v) ? v as string : null,
                        DealType = (string)x["dealType"],
                        Weight = x.TryGetValue("weight", out var w) ? (double)w : 0,
                        FlatPrice = x.TryGetValue("flatPrice", out var f) ? (double)f : 0,
                        W = x.TryGetValue("w", out var wt) ? WeightMap(wt) : null,
                    };
                }).ToList()),
        };
    }

    public sealed class PriceQuote
    {
        /// <summary>Pre-tax price per weight in grams; empty when the tier has no price list.</summary>
        public Dictionary<double, double> Prices;
        /// <summary>Name of the applied day deal, or null at MSRP.</summary>
        public string DealName;
    }

    public static class Pricing
    {
        /// <summary>getEffectivePrices L21172 by batch tier only (brand "" and no strain name).</summary>
        public static PriceQuote GetEffectivePrices(PriceTables t, string tier, int dow) => GetEffectivePrices(t, tier, "", null, dow);

        /// <summary>getStrainPricingTier L21148: strain override, then brand pricing class, then the batch tier ("" = no price list).</summary>
        public static string GetStrainPricingTier(PriceTables t, string tier, string brand, string strainName)
        {
            var so = strainName == null ? null : t.StrainOverrides.FirstOrDefault(o => !string.IsNullOrEmpty(o.Name) && o.Name.ToLowerInvariant() == strainName.ToLowerInvariant());
            if (so != null) return so.Tier;
            string pc = !string.IsNullOrEmpty(brand) && t.BrandPricingClass.TryGetValue(brand, out var c) ? c : "tier"; // getBrandPricingClass L21140
            if (pc == "house") return tier == "smalls" || tier == "premium" ? tier : "house";
            if (pc == "fttp") return "fttp";
            return tier ?? "";
        }

        /// <summary>
        /// getEffectivePrices L21172: pricing tier → MSRP, then the first active matching deal of the day (day deals, then custom deals):
        /// weight_table merge, weight_flat, pct_msrp, use_tier. DealName is null at MSRP (the tool shows the tier label).
        /// </summary>
        public static PriceQuote GetEffectivePrices(PriceTables t, string tier, string brand, string strainName, int dow)
        {
            string pt = GetStrainPricingTier(t, tier, brand, strainName);
            var prices = t.Tiers.TryGetValue(pt, out var msrp) ? new Dictionary<double, double>(msrp) : new Dictionary<double, double>();
            var deals = (t.DayDeals.TryGetValue(dow, out var dd) ? dd : new List<Deal>()).Concat(t.CustomDeals)
                .Where(d => d.Active && (d.Day == null || d.Day == dow));
            foreach (var deal in deals)
            {
                bool matches;
                switch (deal.TargetType)
                {
                    case "pricingClass": matches = (deal.TargetValue == "house" || deal.TargetValue == "fttp") && pt == deal.TargetValue; break;
                    case "tier": matches = pt == deal.TargetValue; break;
                    case "multiTier": matches = deal.TargetValues != null && deal.TargetValues.Contains(pt); break;
                    case "brand": matches = brand == deal.TargetValue; break;
                    default: matches = false; break;
                }
                if (!matches) continue;
                switch (deal.DealType)
                {
                    case "weight_table":
                        foreach (var kv in deal.W) prices[kv.Key] = kv.Value;
                        return new PriceQuote { Prices = prices, DealName = deal.Name };
                    case "weight_flat":
                        prices[deal.Weight] = deal.FlatPrice;
                        return new PriceQuote { Prices = prices, DealName = deal.Name };
                    case "pct_msrp":
                    {
                        var basePrices = t.Tiers.TryGetValue(deal.BaseTier ?? pt, out var bt) ? bt : prices;
                        double disc = 1 - deal.Pct / 100;
                        var result = new Dictionary<double, double>();
                        foreach (double w in t.Weights)
                        {
                            prices.TryGetValue(w, out var cur);
                            if (deal.ExcludeWeights != null && deal.ExcludeWeights.Contains(w)) result[w] = w == 28 && deal.OzOverride > 0 ? deal.OzOverride : cur;
                            else result[w] = basePrices.TryGetValue(w, out var b) && b != 0 ? b * disc : cur;
                        }
                        return new PriceQuote { Prices = result, DealName = deal.Name };
                    }
                    case "use_tier":
                        return new PriceQuote { Prices = new Dictionary<double, double>(t.Tiers.TryGetValue(deal.UseTier ?? "", out var alt) ? alt : prices), DealName = deal.Name };
                }
            }
            return new PriceQuote { Prices = prices, DealName = null };
        }

        /// <summary>hasPricingConfigured L21253 (gpg is not imported; every default tier has weight prices).</summary>
        public static bool HasPricingConfigured(PriceTables t) => t.Tiers.Values.Any(w => w.Values.Any(v => v > 0));

        /// <summary>buildPriceRows L21245 → the first weight with a post-tax price above 0 (findStrains maxPrice L15374), or null.</summary>
        public static (double Grams, double Post)? CheapestPostTax(PriceTables t, PriceQuote q)
        {
            foreach (double w in t.Weights)
            {
                double post = ApplyTax(q.Prices.TryGetValue(w, out var v) ? v : 0, t.TaxRate);
                if (post > 0) return (w, post);
            }
            return null;
        }

        /// <summary>priceFloor L21123: floor to $0.05 after a 4-dp round (GAP-204: floor vs round is open; mirrors v7.11.4).</summary>
        public static double PriceFloor(double n)
        {
            if (!(n > 0)) return 0;
            return Math.Floor(JsMath.Round(n * 10000) / 10000 * 20) / 20;
        }

        /// <summary>applyTax L21134.</summary>
        public static double ApplyTax(double pre, double taxRate) => pre > 0 ? PriceFloor(pre * (1 + taxRate / 100)) : 0;
    }
}
