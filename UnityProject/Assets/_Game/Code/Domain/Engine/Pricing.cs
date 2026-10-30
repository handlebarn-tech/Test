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
    }

    /// <summary>TIER_DEFAULTS L21018, DEFAULT_DAY_DEALS L21036, taxRate L21062 (pricing.json).</summary>
    public sealed class PriceTables
    {
        public double TaxRate;
        public List<double> Weights;
        public Dictionary<string, Dictionary<double, double>> Tiers;
        public Dictionary<int, List<Deal>> DayDeals;

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
        /// <summary>
        /// getEffectivePrices L21172 for the slice: batch tier → MSRP, first active matching tier deal of the day
        /// (weight_table merge or weight_flat). No strain overrides / brand pricing classes (none in the snapshot).
        /// </summary>
        public static PriceQuote GetEffectivePrices(PriceTables t, string tier, int dow)
        {
            var prices = t.Tiers.TryGetValue(tier ?? "", out var msrp) ? new Dictionary<double, double>(msrp) : new Dictionary<double, double>();
            if (t.DayDeals.TryGetValue(dow, out var deals))
                foreach (var deal in deals)
                {
                    if (!deal.Active || deal.TargetType != "tier" || deal.TargetValue != (tier ?? "")) continue;
                    if (deal.DealType == "weight_table") { foreach (var kv in deal.W) prices[kv.Key] = kv.Value; }
                    else if (deal.DealType == "weight_flat") prices[deal.Weight] = deal.FlatPrice;
                    else throw new NotSupportedException("deal type " + deal.DealType + " is not ported (ENGINE.md)");
                    return new PriceQuote { Prices = prices, DealName = deal.Name };
                }
            return new PriceQuote { Prices = prices, DealName = null };
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
