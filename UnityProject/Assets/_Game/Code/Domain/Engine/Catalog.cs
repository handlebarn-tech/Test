using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text.RegularExpressions;

namespace Dispo.Domain.Engine
{
    public sealed class Batch
    {
        public string Id, StrainName, BatchCode, Brand, Tier;
        public bool InStock, DateInferred;
        public DateTime? TestDate;
        public double Total;
        /// <summary>Terpene id → % (tested-ND zeros kept), in source order.</summary>
        public Dictionary<string, double> Terpenes;
    }

    public sealed class Terpene
    {
        public string Id, Name, Cls;
        public Dictionary<string, double> D;
        /// <summary>DB[t].aliases (search names, as written in the tool); empty when the catalog predates importer 1.1.0.</summary>
        public List<string> Aliases = new List<string>();
    }

    public sealed class IntentEntry
    {
        public Dictionary<string, int> D, Neg;
        public string Label, Primary;
    }

    public sealed class StrainGroup
    {
        public string Key, Name;
        /// <summary>Batches in stock first, then file order (getStrainGroups L15442-15466).</summary>
        public List<Batch> Batches = new List<Batch>();
    }

    /// <summary>The imported, PII-free catalog (Data/Catalog/*.json, see Docs/Specs/ENGINE.md).</summary>
    public sealed class Catalog
    {
        public List<string> Domains;
        public List<Batch> Batches;
        public Dictionary<string, Terpene> Terpenes;
        public Dictionary<string, double> BaScalars;
        public Dictionary<string, IntentEntry> Intents;
        public Dictionary<int, Dictionary<string, double>> ClusterBonus;
        public Dictionary<string, double> TierNudge;
        public PriceTables Pricing;
        /// <summary>Parser regex tables (parser_tables.json); null when Load got no parser JSON.</summary>
        public ParserTables Parser;

        List<StrainGroup> _groups;
        Dictionary<string, StrainGroup> _byKey;

        /// <summary>The group for a normName key, or null.</summary>
        public StrainGroup Group(string key)
        {
            if (_byKey == null) _byKey = Groups().ToDictionary(g => g.Key);
            return key != null && _byKey.TryGetValue(key, out var g) ? g : null;
        }

        public static Catalog Load(string batchesJson, string terpenesJson, string tablesJson, string pricingJson, string parserJson = null)
        {
            var c = new Catalog();
            var b = Obj(Json.Parse(batchesJson));
            c.Batches = Arr(b["batches"]).Select(o =>
            {
                var x = Obj(o);
                return new Batch
                {
                    Id = (string)x["id"], StrainName = (string)x["strainName"], BatchCode = (string)x["batchCode"],
                    Brand = (string)x["brand"], Tier = (string)x["tier"], InStock = (bool)x["inStock"],
                    DateInferred = (bool)x["dateInferred"], Total = (double)x["total"],
                    TestDate = ParseDate(x["testDate"] as string),
                    Terpenes = Nums(x["terpenes"]),
                };
            }).ToList();

            var t = Obj(Json.Parse(terpenesJson));
            c.Domains = Arr(t["domains"]).Cast<string>().ToList();
            c.Terpenes = Arr(t["terpenes"]).Select(Obj).ToDictionary(x => (string)x["id"],
                x => new Terpene { Id = (string)x["id"], Name = (string)x["name"], Cls = (string)x["cls"], D = Nums(x["d"]),
                    Aliases = x.TryGetValue("aliases", out var al) ? Arr(al).Cast<string>().ToList() : new List<string>() });
            c.BaScalars = Nums(t["baScalars"]);

            var e = Obj(Json.Parse(tablesJson));
            c.Intents = Obj(e["intents"]).ToDictionary(kv => kv.Key, kv =>
            {
                var x = Obj(kv.Value);
                return new IntentEntry { D = Ints(x["d"]), Neg = Ints(x["neg"]), Label = x.TryGetValue("lbl", out var l) ? l as string : null, Primary = x.TryGetValue("pri", out var p) ? p as string : null };
            });
            c.ClusterBonus = Obj(e["clusterBonus"]).ToDictionary(kv => int.Parse(kv.Key, CultureInfo.InvariantCulture), kv => Nums(kv.Value));
            c.TierNudge = Nums(e["tierNudge"]);

            c.Pricing = PriceTables.FromJson(Obj(Json.Parse(pricingJson)));
            if (parserJson != null) c.Parser = ParserTables.FromJson(Obj(Json.Parse(parserJson)));
            return c;
        }

        /// <summary>normName L15434: lowercase, non-alphanumerics → space, collapse, trim.</summary>
        public static string NormName(string name) =>
            Regex.Replace(Regex.Replace(name.ToLowerInvariant(), "[^a-z0-9]", " "), "\\s+", " ").Trim();

        /// <summary>getStrainGroups L15442: groups in first-seen order; in-stock batches first (stable).</summary>
        public List<StrainGroup> Groups()
        {
            if (_groups != null) return _groups;
            var byKey = new Dictionary<string, StrainGroup>();
            var list = new List<StrainGroup>();
            foreach (var bt in Batches)
            {
                string key = NormName(bt.StrainName);
                if (!byKey.TryGetValue(key, out var g))
                {
                    g = new StrainGroup { Key = key, Name = bt.StrainName };
                    byKey[key] = g; list.Add(g);
                }
                g.Batches.Add(bt);
            }
            foreach (var g in list) g.Batches = g.Batches.OrderBy(x => x.InStock ? 0 : 1).ToList();
            return _groups = list;
        }

        static DateTime? ParseDate(string s) =>
            s != null && DateTime.TryParseExact(s, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out var d) ? d : (DateTime?)null;

        internal static Dictionary<string, object> Obj(object o) => (Dictionary<string, object>)o;
        internal static List<object> Arr(object o) => (List<object>)o;
        internal static Dictionary<string, double> Nums(object o) => Obj(o).ToDictionary(kv => kv.Key, kv => (double)kv.Value);
        internal static Dictionary<string, int> Ints(object o) => Obj(o).ToDictionary(kv => kv.Key, kv => (int)(double)kv.Value);
    }
}
