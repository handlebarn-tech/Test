using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text.RegularExpressions;

namespace Dispo.Domain.Engine
{
    public enum Intent { Recommend, Compare, Strain, TerpeneRank, Unknown }

    public enum PriceIntentType { NoPrice, HasBudget, Budget }

    public sealed class PriceIntent
    {
        public PriceIntentType Type;
        public int Amount; // HasBudget only
    }

    /// <summary>A hard terpene exclusion: display name and the terpene ids it covers (_extractExclusions L15979).</summary>
    public sealed class Exclusion
    {
        public string Name;
        public List<string> Ids;
    }

    /// <summary>findStrains opts (L15355): exclusions, maxAnx (refine), exclude keys + likeKey (like-X), maxPrice (post-tax $).</summary>
    public sealed class FindOptions
    {
        public List<Exclusion> Excl;
        public int? MaxAnx;
        public List<string> Exclude;
        public string LikeKey;
        public double? MaxPrice;
        public int Dow; // for maxPrice day deals

        public FindOptions Clone() => new FindOptions
        {
            Excl = Excl, MaxAnx = MaxAnx, Exclude = Exclude == null ? null : new List<string>(Exclude), LikeKey = LikeKey, MaxPrice = MaxPrice, Dow = Dow,
        };
    }

    /// <summary>parseQuery result plus what submit L19542 adds (_priceIntent, drive).</summary>
    public sealed class ParsedQuery
    {
        public Intent Intent;
        public Dictionary<string, int> Crit = new Dictionary<string, int>(), Neg = new Dictionary<string, int>();
        public string Primary;
        public List<string> Lbls = new List<string>();
        public string Tf;                 // terpene sort (L16219)
        public string GroupKey;           // strain
        public List<string> Strains;      // compare
        public string Terpene;            // terpene_rank
        public List<Exclusion> Excl;      // recommend / terpene_rank / strain
        public FindOptions Opts = new FindOptions();
        public PriceIntent PriceIntent;
        public bool Drive;                // "Cannabis and driving don't mix." (L19545)
    }

    /// <summary>Store prefs the parser reads, plus the game's defect fixes (defaults = v7.11.4).</summary>
    public sealed class ParserOptions
    {
        public bool PainFunctional = true;  // _prefs.painFunctional L17517
        /// <summary>MC-7 (v7.11.5): "for the day" is an INTENTS key with the "daytime" numbers.</summary>
        public bool FixForTheDay;
        /// <summary>GAP-206: _sleepAsk L16086 also matches "sleeping"/"sleepy"/... (sleep\w*).</summary>
        public bool FixSleepAsk;

        public static ParserOptions V7114 => new ParserOptions();
        public static ParserOptions Game => new ParserOptions { FixForTheDay = true, FixSleepAsk = true };
    }

    /// <summary>
    /// The v7.11.4 natural-language parser: parseQuery L16013 + _parseQueryCore L16024-16247 + detectPriceIntent L21744
    /// + the drive flag L19545. Pure and deterministic; needs a catalog loaded with parser_tables.json.
    /// </summary>
    public static class QueryParser
    {
        const RegexOptions Js = ParserTables.Js;
        static Regex R(string p) => new Regex(p, Js);
        static string EscRe(string s) => Regex.Replace(s, @"[.*+?^${}()|[\]\\]", "\\$&"); // _escRe L15889

        public static ParsedQuery Parse(Catalog cat, string q, ParserOptions o = null)
        {
            o = o ?? ParserOptions.V7114;
            var p = ParseQuery(cat, q, false, o);
            p.PriceIntent = DetectPriceIntent(cat, q);
            p.Drive = Drive.IsMatch(q) && !NoDrive.IsMatch(q);
            return p;
        }

        static readonly Regex Drive = new Regex(@"\b(driv(e|es|ing)|drove)\b", Js | RegexOptions.IgnoreCase);
        static readonly Regex NoDrive = new Regex(@"\bno drive\b", Js | RegexOptions.IgnoreCase);

        // ── parseQuery L16013 ────────────────────────────────────────────
        static readonly Regex LikeWord = R(@"\b(like|similar to)\b");

        static ParsedQuery ParseQuery(Catalog cat, string q, bool noNames, ParserOptions o)
        {
            var ex = ExtractExclusions(cat, q.ToLowerInvariant().Trim());
            if (ex.Excl.Count == 0) return Core(cat, q, noNames, o);
            var r = Core(cat, ex.Text, noNames, o);
            if (r.Intent == Intent.Strain && LikeWord.IsMatch(ex.Text))
                r = new ParsedQuery { Intent = Intent.Recommend, Opts = new FindOptions { Exclude = new List<string> { r.GroupKey }, LikeKey = r.GroupKey } };
            if (r.Intent == Intent.Unknown)
                r = new ParsedQuery { Intent = Intent.Recommend, Lbls = { "no " + string.Join(", no ", ex.Excl.Select(e => e.Name)) } };
            if (r.Intent == Intent.Recommend || r.Intent == Intent.TerpeneRank || r.Intent == Intent.Strain) r.Excl = ex.Excl; // MC-1
            return r;
        }

        // ── _extractExclusions L15975-15999 ──────────────────────────────
        public const double ExclMaxPct = 0.01; // EXCL_MAX_PCT L15975
        static readonly Dictionary<string, string[]> ExclFamily = new Dictionary<string, string[]> // L15976
        {
            { "pinene", new[] { "alpha_pinene", "beta_pinene" } }, { "pinenes", new[] { "alpha_pinene", "beta_pinene" } },
            { "terpinene", new[] { "alpha_terpinene", "gamma_terpinene" } }, { "nerolidol", new[] { "nerolidol", "trans_nerolidol" } },
        };

        sealed class ExclRegexes { public Dictionary<string, string[]> Alias; public Regex One; public Regex[] Res; }
        static readonly Dictionary<Catalog, ExclRegexes> ExclCache = new Dictionary<Catalog, ExclRegexes>();

        static ExclRegexes ExclFor(Catalog cat)
        {
            lock (ExclCache)
            {
                if (ExclCache.TryGetValue(cat, out var c)) return c;
                var alias = new Dictionary<string, string[]> { { "bcp", new[] { "beta_caryophyllene" } } };
                var order = new List<string> { "bcp" };
                void Put(string k, string[] v) { if (!alias.ContainsKey(k)) order.Add(k); alias[k] = v; }
                foreach (var kv in ExclFamily) Put(kv.Key, kv.Value);
                foreach (var t in cat.Terpenes.Values)
                    foreach (var a in t.Aliases) { string al = a.ToLowerInvariant(); if (!ExclFamily.ContainsKey(al)) Put(al, new[] { t.Id }); }
                string T = "(?:" + string.Join("|", order.OrderByDescending(k => k.Length).Select(EscRe)) + ")";
                string L = "(" + T + @"(?:\s*(?:,|/|&|\band\b|\bor\b|\bnor\b)\s*(?:no\s+)?" + T + ")*)";
                c = new ExclRegexes
                {
                    Alias = alias,
                    One = R("(^|[^a-z0-9])(" + T + ")(?=[^a-z0-9]|$)"),
                    Res = new[]
                    {
                        R(@"(^|[^a-z0-9])(?:without|no|not|zero|avoid(?:s|ing)?|free of|allergic to)\s+(?:any\s+)?" + L + "(?=[^a-z0-9]|$)"),
                        R("(^|[^a-z0-9])" + L + @"[\s-]free(?=[^a-z0-9]|$)"),
                    },
                };
                return ExclCache[cat] = c;
            }
        }

        static readonly Regex WithoutAbbrev = R(@"\bw\/o\b");
        static readonly Regex IsomerSpace = R(@"\b(alpha|beta|gamma|dl|d)\s+(?=[a-z]+(?:ene|ol|ole|one)\b)");
        static readonly Regex Spaces = R(@"\s+");
        static readonly Regex TrailingS = R("s$");

        public static (List<Exclusion> Excl, string Text) ExtractExclusions(Catalog cat, string text)
        {
            var x = ExclFor(cat);
            var excl = new List<Exclusion>();
            string t = IsomerSpace.Replace(WithoutAbbrev.Replace(text, "without"), "$1-");
            foreach (var re in x.Res)
                t = re.Replace(t, m =>
                {
                    foreach (Match mm in x.One.Matches(m.Groups[2].Value))
                    {
                        string a = mm.Groups[2].Value;
                        var ids = x.Alias[a];
                        string name = ExclFamily.ContainsKey(a) ? TrailingS.Replace(a, "") : cat.Terpenes[ids[0]].Name;
                        if (!excl.Any(e => e.Name == name)) excl.Add(new Exclusion { Name = name, Ids = ids.ToList() });
                    }
                    return m.Groups[1].Value + " ";
                });
            return (excl, Spaces.Replace(t, " ").Trim());
        }

        // ── _parseQueryCore L16024 ───────────────────────────────────────
        static readonly (Regex re, string with)[] Strip = // L16030-16038
        {
            (R(@"\bw\/o\b"), "without"), (R(@"\bcouch-?lock"), "couch lock"),
            (R(@"\b(my |the )?(customer|patient|client|guest|he|she|they|this (guy|lady|person|woman|man))\b"), ""),
            (R(@"\b(want[s]?|need[s]?|looking for|asking for|coming in for|here for|said|told me|mentioned|says)\b"), ""),
            (R(@"\b(something|anything|a strain|a product|weed|flower|cannabis|marijuana)\b"), ""),
            (R(@"\b(pre-?rolls?|prerolls?|carts?|cartridges?|vapes?|dabs?|edibles?|gummies|concentrates?|eighths?|quarters?|half ?ounces?|ounces?|oz|grams?)\b"), ""),
            (R(@"\b(a|an|some|couple|few|one|two)\s+joints?\b(?!\s*(pain|ache|hurt|sore|stiff|swell))"), ""),
            (R(@"\s+"), " "),
        };
        static readonly Regex MoreLess = R(@"\b(but|more|less|except|without)\b");
        static readonly Regex RankWord = R(@"\b(highest|most|which.*most|most.*which|top.*for|which has)\b"); // L16058
        static readonly Regex SleepAsk = R(@"\b(sleep|insomnia)\b");        // _sleepAsk L16086
        static readonly Regex SleepAskFixed = R(@"\b(sleep\w*|insomnia)\b"); // GAP-206 game fix
        static readonly Regex WantsSedation = R(@"\b(heavy|heavier|sedating|sedation|knock.?out|couch.?lock|sleep|sleepy|don'?t care|don'?t mind|just knock|pass out|bed.?time|night.?time|night)\b"); // L16214

        static ParsedQuery Core(Catalog cat, string q, bool noNames, ParserOptions o)
        {
            if (cat.Parser == null) throw new InvalidOperationException("Catalog was loaded without parser_tables.json");
            string ql = q.ToLowerInvariant().Trim();
            string stripped = ql;
            foreach (var (re, with) in Strip) stripped = re.Replace(stripped, with);
            stripped = stripped.Trim();
            string qi = stripped.Length > 0 ? stripped : ql;

            // compare / like-X / strain lookup L16043-16054
            bool isCompare = ql.Contains("compare") || ql.Contains(" vs ") || ql.Contains("versus") || ql.Contains("difference between") || ql.Contains("which is better");
            var mentions = new List<string>(); string rest = null;
            if (!noNames)
            {
                (mentions, rest) = FindStrainMentions(cat, ql);
                if (mentions.Count == 0 || isCompare) FuzzyStrainMentions(cat, rest, mentions);
            }
            if (isCompare && mentions.Count >= 2) return new ParsedQuery { Intent = Intent.Compare, Strains = mentions.Take(3).ToList() };
            if (mentions.Count > 0 && !isCompare && LikeWord.IsMatch(ql) && MoreLess.IsMatch(ql))
            {
                var y = ParseQuery(cat, rest, true, o);
                if (y.Intent == Intent.Recommend) { y.Opts = new FindOptions { Exclude = new List<string> { mentions[0] }, LikeKey = mentions[0] }; return y; }
            }
            if (mentions.Count > 0 && !isCompare) return new ParsedQuery { Intent = Intent.Strain, GroupKey = mentions[0] };

            // terpene rank L16058
            if (RankWord.IsMatch(qi))
            {
                var tid = FindTerpMention(cat, qi);
                if (tid != null) return new ParsedQuery { Intent = Intent.TerpeneRank, Terpene = tid };
            }

            // negation patterns L16066-16093
            var P = cat.Parser;
            var negHints = new Dictionary<string, int>(); var posHints = new Dictionary<string, int>();
            bool sleepAsk = (o.FixSleepAsk ? SleepAskFixed : SleepAsk).IsMatch(qi) && !P.NegPatterns[0].R.IsMatch(qi);
            foreach (var np in P.NegPatterns)
            {
                if (np.Work && sleepAsk) continue;
                if (!np.R.IsMatch(np.Raw ? ql : qi)) continue;
                if (np.Positive) posHints[np.D] = Math.Max(posHints.TryGetValue(np.D, out var pv) ? pv : 0, np.V);
                else negHints[np.D] = negHints.TryGetValue(np.D, out var nv) && nv != 0 ? Math.Min(nv, np.V) : np.V;
            }

            var crit = new Dictionary<string, int>(); var neg = new Dictionary<string, int>(); var lbls = new List<string>();
            string primary = null; int primaryScore = 0;
            void Merge(Dictionary<string, int> d, Dictionary<string, int> n, string lbl, string pri)
            {
                foreach (var kv in d) crit[kv.Key] = Math.Max(crit.TryGetValue(kv.Key, out var c) ? c : 0, kv.Value);
                foreach (var kv in n) neg[kv.Key] = neg.TryGetValue(kv.Key, out var c) && c != 0 ? Math.Min(c, kv.Value) : kv.Value;
                if (!string.IsNullOrEmpty(lbl)) lbls.Add(lbl); // `if(cfg.lbl)`: some keys have lbl:''
                if (pri != null && d.TryGetValue(pri, out var sc) && sc != 0 && sc > primaryScore) { primaryScore = sc; primary = pri; }
            }

            // PHRASE_MAP L16165: test on qi, blank the first match in the keyword text
            string kwText = qi;
            foreach (var ph in P.PhraseMap)
            {
                if (!ph.R.IsMatch(qi)) continue;
                kwText = ph.R.Replace(kwText, m => new string(' ', m.Length), 1);
                Merge(ph.D, ph.Neg, ph.Lbl, ph.Pri);
            }

            // INTENTS keywords L16176, longest first, consumed spans blanked (_consumeKw L15900)
            foreach (var (kw, cfg) in IntentKeys(cat, o.FixForTheDay))
            {
                var m = KwRe(kw).Match(kwText);
                if (!m.Success) continue;
                int start = m.Index + m.Groups[1].Length, len = m.Groups[2].Length + m.Groups[3].Length;
                kwText = kwText.Substring(0, start) + new string(' ', len) + kwText.Substring(start + len);
                Merge(cfg.D, cfg.Neg, cfg.Label, cfg.Primary);
            }

            // negation hints L16191-16193
            foreach (var kv in negHints) neg[kv.Key] = neg.TryGetValue(kv.Key, out var c) && c != 0 ? Math.Min(c, kv.Value) : kv.Value;
            foreach (var kv in posHints) crit[kv.Key] = Math.Max(crit.TryGetValue(kv.Key, out var c) ? c : 0, kv.Value);

            // conflict resolution L16200-16209 (Without() keeps JS insertion order; Dictionary.Remove would let later adds reuse the slot)
            foreach (var d in neg.Keys.ToList())
            {
                if (!crit.TryGetValue(d, out var c)) continue;
                if (neg[d] > c + 5) continue;
                if (negHints.ContainsKey(d)) crit = Without(crit, d); else neg = Without(neg, d);
            }
            if (primary != null && !crit.ContainsKey(primary)) primary = BestDomain(crit);

            // pain functional default L16213
            if (crit.TryGetValue(DomainIds.PainInflammation, out var pain) && pain != 0
                && !(neg.TryGetValue(DomainIds.Sedation, out var ns) && ns != 0)
                && !(crit.TryGetValue(DomainIds.Sedation, out var cs) && cs >= EngineConstants.PainSedationCritMax)
                && o.PainFunctional && !WantsSedation.IsMatch(qi))
                neg[DomainIds.Sedation] = EngineConstants.PainFunctionalCap;

            string tf = FindTerpMention(cat, qi); // L16219
            if (crit.Count > 0 || neg.Count > 0) return new ParsedQuery { Intent = Intent.Recommend, Crit = crit, Neg = neg, Lbls = lbls, Tf = tf, Primary = primary };

            // fuzzy fallback L16226-16244: first match only
            foreach (var f in P.Fuzzy)
            {
                if (!f.R.IsMatch(qi)) continue;
                foreach (var kv in f.D) crit[kv.Key] = Math.Max(crit.TryGetValue(kv.Key, out var c) ? c : 0, kv.Value);
                lbls.Add(f.Lbl);
                if (primary == null) primary = f.Pri;
                break;
            }
            if (crit.Count > 0) return new ParsedQuery { Intent = Intent.Recommend, Crit = crit, Neg = neg, Lbls = lbls, Tf = tf, Primary = primary };
            return new ParsedQuery { Intent = Intent.Unknown };
        }

        internal static Dictionary<string, int> Without(Dictionary<string, int> d, string key) =>
            d.Where(kv => kv.Key != key).ToDictionary(kv => kv.Key, kv => kv.Value);

        /// <summary>Highest crit value, first wins on ties (L16207, refineSearch L19602).</summary>
        internal static string BestDomain(Dictionary<string, int> crit)
        {
            string best = null; int bv = 0;
            foreach (var kv in crit) if (kv.Value > bv) { bv = kv.Value; best = kv.Key; }
            return best;
        }

        // _kwRe L15891
        static readonly Dictionary<string, Regex> KwCache = new Dictionary<string, Regex>();
        static Regex KwRe(string kw)
        {
            lock (KwCache)
            {
                if (!KwCache.TryGetValue(kw, out var r)) KwCache[kw] = r = R("(^|[^a-z0-9])(" + EscRe(kw) + ")(s|es)?(?=[^a-z0-9]|$)");
                return r;
            }
        }

        // MC-7: v7.11.5 adds 'for the day' right after 'daytime' with the same numbers (dev/v7115/fixes.py L44-46).
        const string ForTheDay = "for the day";
        static List<(string, IntentEntry)> IntentKeys(Catalog cat, bool fixForTheDay)
        {
            var list = new List<(string, IntentEntry)>();
            foreach (var kv in cat.Intents)
            {
                list.Add((kv.Key, kv.Value));
                if (fixForTheDay && kv.Key == "daytime" && !cat.Intents.ContainsKey(ForTheDay)) list.Add((ForTheDay, kv.Value));
            }
            return list.OrderByDescending(x => x.Item1.Length).ToList(); // stable, like V8 sort
        }

        // ── strain mentions L15906-15954 ─────────────────────────────────
        static readonly Dictionary<Catalog, List<(string key, string n)>> NameCache = new Dictionary<Catalog, List<(string, string)>>();
        static List<(string key, string n)> NameIndex(Catalog cat) // _strainNameIndex L15908
        {
            lock (NameCache)
            {
                if (!NameCache.TryGetValue(cat, out var l))
                    NameCache[cat] = l = cat.Groups().Select(g => (g.Key, g.Name.ToLowerInvariant().Trim())).Where(x => x.Item2.Length >= 3)
                        .OrderByDescending(x => x.Item2.Length).ToList();
                return l;
            }
        }

        /// <summary>_findStrainMentions L15916: whole-word names, longest first; returns the keys and the text with names blanked.</summary>
        public static (List<string> Found, string Remaining) FindStrainMentions(Catalog cat, string ql)
        {
            string text = ql; var found = new List<string>();
            foreach (var (key, n) in NameIndex(cat))
            {
                if (text.IndexOf(n, StringComparison.Ordinal) < 0) continue; // fast reject; the regex decides
                var m = R("(^|[^a-z0-9])" + EscRe(n) + "(?=[^a-z0-9]|$)").Match(text);
                if (!m.Success) continue;
                if (!found.Contains(key)) found.Add(key);
                int s = m.Index + m.Groups[1].Length;
                text = text.Substring(0, s) + new string(' ', n.Length) + text.Substring(s + n.Length);
            }
            return (found, text);
        }

        /// <summary>_fuzzyStrainMentions L15933: Levenshtein ≤1 (5-7 letters) / ≤2 (8+), exact under 5, unique closest only, 3 rounds.</summary>
        public static void FuzzyStrainMentions(Catalog cat, string text, List<string> found)
        {
            var idx = NameIndex(cat).Select(x => { var t = Catalog.NormName(x.n).Split(' '); return (x.key, c: string.Concat(t), w: t.Length); }).ToList();
            for (int guard = 0; guard < 3; guard++)
            {
                var qt = Catalog.NormName(text).Split(' ').Where(s => s.Length > 0).ToList();
                string bestKey = null; int bestD = 0, bestI = 0, bestK = 0; bool tie = false;
                foreach (var (key, c, w) in idx)
                {
                    if (found.Contains(key)) continue;
                    int tol = c.Length >= 8 ? 2 : c.Length >= 5 ? 1 : 0;
                    for (int k = Math.Max(1, w - 1); k <= w + 1; k++)
                        for (int i = 0; i + k <= qt.Count; i++)
                        {
                            string s = string.Concat(qt.Skip(i).Take(k));
                            if (Math.Abs(s.Length - c.Length) > tol) continue;
                            int d = Lev(s, c); if (d > tol) continue;
                            if (bestKey == null || d < bestD) { bestKey = key; bestD = d; bestI = i; bestK = k; tie = false; }
                            else if (d == bestD && key != bestKey) tie = true;
                        }
                }
                if (bestKey == null || tie) break;
                found.Add(bestKey);
                text = string.Join(" ", qt.Where((_, j) => j < bestI || j >= bestI + bestK));
            }
        }

        static int Lev(string a, string b) // _lev L15930
        {
            var p = Enumerable.Range(0, b.Length + 1).ToArray();
            for (int i = 1; i <= a.Length; i++)
            {
                var c = new int[b.Length + 1]; c[0] = i;
                for (int j = 1; j <= b.Length; j++) c[j] = Math.Min(Math.Min(p[j] + 1, c[j - 1] + 1), p[j - 1] + (a[i - 1] == b[j - 1] ? 0 : 1));
                p = c;
            }
            return p[b.Length];
        }

        // ── terpene mention L15955-15970 ─────────────────────────────────
        static readonly (string a, string id)[] ExtraAliases = { ("pinene", "alpha_pinene"), ("bcp", "beta_caryophyllene"), ("lavender", "linalool") };
        static readonly Dictionary<Catalog, List<(string a, Regex re, string id)>> TerpCache = new Dictionary<Catalog, List<(string, Regex, string)>>();

        /// <summary>_findTerpMention L15958: longest alias wins.</summary>
        public static string FindTerpMention(Catalog cat, string text)
        {
            List<(string a, Regex re, string id)> list;
            lock (TerpCache)
            {
                if (!TerpCache.TryGetValue(cat, out list))
                    TerpCache[cat] = list = cat.Terpenes.Values.SelectMany(t => t.Aliases.Select(a => (a.ToLowerInvariant(), t.Id)))
                        .Concat(ExtraAliases).OrderByDescending(x => x.Item1.Length)
                        .Select(x => (x.Item1, R("(^|[^a-z0-9])" + EscRe(x.Item1) + "(?=[^a-z0-9]|$)"), x.Item2)).ToList();
            }
            foreach (var (a, re, id) in list) if (text.IndexOf(a, StringComparison.Ordinal) >= 0 && re.IsMatch(text)) return id;
            return null;
        }

        // ── detectPriceIntent L21744 ─────────────────────────────────────
        static readonly Regex Digits = R(@"^\d+$");
        public static PriceIntent DetectPriceIntent(Catalog cat, string q)
        {
            string ql = q.ToLowerInvariant().Trim();
            var P = cat.Parser;
            if (P.NoPrice.Any(r => r.IsMatch(ql))) return new PriceIntent { Type = PriceIntentType.NoPrice };
            foreach (var r in P.HasBudget)
            {
                var m = r.Match(ql);
                if (!m.Success) continue;
                var nums = m.Groups.Cast<Group>().Skip(1).Where(g => g.Success && Digits.IsMatch(g.Value)).ToList();
                if (nums.Count == 0) continue;
                // parseInt of a digit run; a run too long for long fails the 0 < amt < 10000 check in JS too
                if (long.TryParse(nums[nums.Count - 1].Value, NumberStyles.None, CultureInfo.InvariantCulture, out var amt) && amt > 0 && amt < 10000)
                    return new PriceIntent { Type = PriceIntentType.HasBudget, Amount = (int)amt };
            }
            if (P.Budget.Any(r => r.IsMatch(ql))) return new PriceIntent { Type = PriceIntentType.Budget };
            return null;
        }
    }
}
