using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace Dispo.Domain.Engine
{
    /// <summary>negPatterns entry, _parseQueryCore L16066-16081.</summary>
    public sealed class NegPattern
    {
        public Regex R;
        public string D;
        public int V;
        public bool Positive, Raw, Work;
    }

    /// <summary>PHRASE_MAP L16098 / fuzzy fallback L16226 entry ({r, d, neg, lbl, pri}).</summary>
    public sealed class PhraseEntry
    {
        public Regex R;
        public Dictionary<string, int> D, Neg;
        public string Lbl, Pri;
    }

    /// <summary>
    /// The parser's regex tables (parser_tables.json, importer 1.1.0), stored as the tool's own regex source text.
    /// Built with RegexOptions.ECMAScript so \b, \d and \w keep JS (ASCII) meaning.
    /// </summary>
    public sealed class ParserTables
    {
        public const RegexOptions Js = RegexOptions.ECMAScript | RegexOptions.CultureInvariant;

        public List<NegPattern> NegPatterns;
        public List<PhraseEntry> PhraseMap, Fuzzy;
        public List<Regex> NoPrice, HasBudget, Budget; // PRICE_INTENTS L21696

        internal static ParserTables FromJson(Dictionary<string, object> j)
        {
            var pi = Catalog.Obj(j["priceIntents"]);
            List<Regex> Res(object o) => Catalog.Arr(o).Select(x => new Regex((string)x, Js)).ToList();
            return new ParserTables
            {
                NegPatterns = Catalog.Arr(j["negPatterns"]).Select(Catalog.Obj).Select(x => new NegPattern
                {
                    R = new Regex((string)x["r"], Js), D = (string)x["d"], V = (int)(double)x["v"],
                    Positive = Flag(x, "positive"), Raw = Flag(x, "raw"), Work = Flag(x, "work"),
                }).ToList(),
                PhraseMap = Phrases(j["phraseMap"]),
                Fuzzy = Phrases(j["fuzzy"]),
                NoPrice = Res(pi["noPrice"]), HasBudget = Res(pi["hasBudget"]), Budget = Res(pi["budget"]),
            };
        }

        static bool Flag(Dictionary<string, object> x, string k) => x.TryGetValue(k, out var v) && v is bool b && b;

        static List<PhraseEntry> Phrases(object o) => Catalog.Arr(o).Select(Catalog.Obj).Select(x => new PhraseEntry
        {
            R = new Regex((string)x["r"], Js),
            D = Catalog.Ints(x["d"]),
            Neg = x.TryGetValue("neg", out var n) ? Catalog.Ints(n) : new Dictionary<string, int>(),
            Lbl = x.TryGetValue("lbl", out var l) ? l as string : null,
            Pri = x.TryGetValue("pri", out var p) ? p as string : null,
        }).ToList();
    }
}
