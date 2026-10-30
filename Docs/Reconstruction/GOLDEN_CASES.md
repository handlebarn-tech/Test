# Golden cases: TFS Budtender v7.11.4 engine, executed (MIG-001)

These outputs come from the shipped engine code running, not from documents. They are what GAME-001's C# port must reproduce before any game tuning.

## Method (reproducible)

1. Inputs, copied read-only into a private temp dir (never run inside `tfs-budtender`):
   - `deploy/2026-10-30-v7114/site/index.html`, md5 **228684e9f02d703cf3a36692baf10d18**
   - `inventory/tfs-inventory-master.json`, md5 **09bfa4f00206b25f77fb2a49db2eea9c** (`version tfs-3.3`, exported `2026-10-29T19:13:36.534Z`, 1207 batches, 366 strain groups, **67 in-stock groups** / 77 in-stock batches by its `status` field)
2. `engine.js` (appendix A) slices the engine's own source lines (ranges listed in the file) into a Node 22 `vm` context, with stubs for `document`/`localStorage`. It loads the inventory the way the page does (`_sanitizeImport` → apply `deleted` → `_backfillDates` → `loadPricing` defaults). The only replacements: `renderStrain` returns a `<<key>>` marker so the HTML from `respond()` can be read back, and `findStrains` is wrapped to record its calls.
3. The clock is pinned to `2026-10-29T19:13:36.534Z` (Thursday, dow 4), with `TZ=America/Phoenix`. Ranking does not depend on the clock; the clock only affects day deals, max-price checks and the age badge.
4. State: local-mode defaults (`resultCount 3`, `painFunctional true`, no customer profile, no tier chips, built-in prices, tax 25.1%). The case table lists any per-case overrides.
5. Run: `node golden.js index.html tfs-inventory-master.json golden_cases.json` (appendix B). Two runs gave byte-identical output, md5 **782427de4f75c910e8448e52b5a06bc3** = `golden_cases.json` in this folder. Harness md5: engine.js `1efb4d4f46b4463a1a857cdc04b0a039`, golden.js `a139b45c1aac219cbff7289b6721b7f4`.

**Caveat:** stock is the master file's `status` snapshot. The live tool reads per-store stock from Supabase, so the live top 3 can differ on any day. The *algorithm* is what is golden; the inventory snapshot is a fixture.

`golden_cases.json` holds, per case: the parsed query (`intent`, `crit`, `neg`, `primary`, `lbls`, `opts`, `excl`, price intent), outcome, every `findStrains` call with its top N (key, name, `ms` to 4 dp, tier, cluster, anxiety risk, the six display domains), role tags, and compare, strain or terpene-rank cards. It also holds `pricing` (all 9 tiers × 7 days × 4 weights, pre and post tax), `batchScores` (single-batch `scoreDomains`/`scoreRaw`/cluster/anxiety for 4 real batches) and `averaging` (Zero Gravity: 25 batches, 3 in stock, recency-weighted top-5 profile).

## Cases (top 3 shown as `name (ms, role tag)`)

The RC-01 to RC-21 queries are the tool's own regression set (`tests/tests/rank_compare.py`).

| ID | Query [state] | Parsed | Outcome | Ranked output |
|---|---|---|---|---|
| RC-01 | `something for sleep` | recommend {sedation:38} pri=sedation | ok | Kush Cake (1.347, best_match); Squid Ink (1.343, most_sedating); Double OG Sour (1.3187, lowest_anxiety) |
| RC-02 | `can't sleep` | recommend {sedation:55,anxiety_relief:40} pri=sedation | ok | Kush Cake (1.467, best_match); Double OG Sour (1.4387, lowest_anxiety); Peak OG (1.4178, gentle) |
| RC-03 | `stress relief` | recommend {anxiety_relief:32} pri=anxiety | ok | Rainbow Drip (2.0382, best_match); Bubba Verde (2.0343, most_focus); Kush Cake (1.9667, most_sedating) |
| RC-04 | `pain` | recommend {pain_inflammation:38} cap {sedation:55} pri=pain | ok | Bubba Verde (1.7844, best_match); Honeycomb Pave #4 (1.6624, lowest_anxiety); Zero Gravity (1.5957, most_sedating) |
| RC-05 | `focus for work` | recommend {focus_cognitive:22} pri=focus | ok | Bubba Verde (1.2666, best_match); Honeycomb Pave #4 (1.2256, lowest_anxiety); Peach Wave (1.1665, most_sedating) |
| RC-06 | `creative` | recommend {focus_cognitive:5,uplift:18} pri=uplift | ok | Bubba Verde (2.2101, best_match); Honeycomb Pave #4 (2.1193, lowest_anxiety); Scented Marker (1.8628, most_functional) |
| RC-07 | `uplifting but no couch lock` | recommend {uplift:24} cap {sedation:42} pri=uplift | ok | Scented Marker (1.2534, best_match); Bubba Verde (1.2155, most_pain); Honeycomb Pave #4 (1.1699, most_sedating) |
| RC-08 | `need to drive` | recommend {} cap {sedation:38} | ok | Beaver Cookies (0.0547, best_match); Papaya Melonz (0.0482, lowest_anxiety); McLaren (0.0071, most_functional) |
| RC-09 | `anxiety` | recommend {anxiety_relief:35} pri=anxiety | ok | Rainbow Drip (2.0382, best_match); Bubba Verde (2.0343, most_focus); Kush Cake (1.9667, most_sedating) |
| RC-10 | `energy` | recommend {uplift:28} cap {sedation:36} pri=uplift | ok | Scented Marker (1.2494, best_match); Honeycomb Pave #4 (1.1361, most_pain); Saffire (1.0639, most_sedating) |
| RC-11 | `insomnia` | recommend {sedation:55,anxiety_relief:40} pri=sedation | ok | Kush Cake (1.467, best_match); Double OG Sour (1.4387, lowest_anxiety); Peak OG (1.4178, gentle) |
| RC-12 | `relaxing body high` | recommend {sedation:35,pain_inflammation:30,anxiety_relief:30} cap {sedation:55} pri=sedation | ok | Wookie Grease (0.9352, best_match); T-Rekt (0.9184, gentle); Double OG Chem 5 (0.8994, lowest_anxiety) |
| RC-13 | `happy social` | recommend {uplift:28,anxiety_relief:30} cap {sedation:40} pri=uplift | ok | Bubba Verde (2.4407, best_match); Honeycomb Pave #4 (2.3176, lowest_anxiety); Slurricane (1.9983, most_functional) |
| RC-14 | `inflammation` | recommend {pain_inflammation:42} cap {sedation:55} pri=pain | ok | Bubba Verde (1.7844, best_match); Honeycomb Pave #4 (1.6624, lowest_anxiety); Zero Gravity (1.5957, most_sedating) |
| RC-15 | `calming` | recommend {anxiety_relief:30} pri=anxiety | ok | Rainbow Drip (2.0382, best_match); Bubba Verde (2.0343, most_focus); Kush Cake (1.9667, most_sedating) |
| RC-16 | `something for the day` | unknown | help | (none). **Known defect MC-7**, fixed in unreleased v7.11.5 |
| RC-17 | `heavy indica` | recommend {sedation:40} pri=sedation | ok | Kush Cake (1.347, best_match); Squid Ink (1.343, most_sedating); Double OG Sour (1.3187, lowest_anxiety) |
| RC-18 | `back pain without sedation` | recommend {pain_inflammation:50,sedation:30} cap {sedation:40} pri=pain | ok | Bubba Verde (1.7214, best_match); Honeycomb Pave #4 (1.6044, lowest_anxiety); Goo Lagoon (1.3699, gentle) |
| RC-19 | `chill evening` | recommend {sedation:25,anxiety_relief:30} pri=anxiety | ok | Kush Cake (2.7714, best_match); Rainbow Drip (2.7706, most_uplifting); Blue Mamba #24 (2.7694, most_sedating) |
| RC-20 | `something cheap for sleep` | recommend {sedation:38} pri=sedation, price=budget | ok | Kush Cake (1.347, best_match); Squid Ink (1.343, most_sedating); Double OG Sour (1.3187, lowest_anxiety). "cheap" adds only a price banner; ranking unchanged |
| RC-21 | `what has the most limonene` | terpene_rank terp=dl_limonene | ok | Scented Marker 1.52%; Bubba Verde 1.2586%; Honeycomb Pave #4 0.9771% |
| X-01 | `sleep without limonene` | recommend {sedation:38} excl=D-Limonene | excluded-all | none. "No in-stock strain is verified free of D-Limonene." (not enough data: a missing value counts as unknown) |
| X-02 | `no pinene, something for pain` | recommend {pain_inflammation:38} cap {sedation:55} excl=pinene(α+β) | ok | Limon Catorce (0.7798), the only verified-clear strain (single candidate) |
| X-03 | `sleep` [profile=new] | recommend {sedation:38} | ok | Kush Cake (1.347); Neapolitan (1.2567, most_functional); Blue Mamba #24 (1.2507, most_sedating). Squid Ink (myrcene 1.35%, −0.45) and Double OG Sour (0.95%, −0.22) drop below vs X-04 because of the new-customer myrcene onset penalty; all four have anxiety risk 15, so the >60 filter does not apply |
| X-04 | `sleep` | recommend {sedation:38} | ok | Kush Cake (1.347); Squid Ink (1.343); Double OG Sour (1.3187) |
| X-05 | `sleep` [tiers=t3] | recommend {sedation:38} | ok | Blue Mamba #24 (1.2507); SFV OG (1.1258, most_functional); Peach Tree (0.9426, gentle) |
| X-06 | `I only have $15 for sleep` | recommend {sedation:38} maxPrice=15 | ok | same as X-04: each passes because its cheapest weight (smalls 3.5 g on Thu: $10.50 → $13.10 with tax) is ≤ $15 |
| X-07 | `sinking` [tiers=t1] | recommend {sedation:55} | **fallback** | 1st pass empty; 2nd pass {sedation:33} → SoHo (0.9443); Citrus Punch (0.9192, gentle); J-31 (0.6645, most_focus). "No exact match … Closest available" |
| X-08 | `first time, wont make me paranoid` | recommend {anxiety_relief:55,sedation:20} cap {uplift:50} | ok | Kush Cake (2.5764); Blue Mamba #24 (2.5694, most_sedating); Rainbow Drip (2.5306, most_uplifting) |
| X-09 | `compare Kush Cake vs Squid Ink` | compare | ok | Kush Cake vs Squid Ink. "Key difference: Uplift: Kush Cake scores notably higher (12 pts)" |
| X-10 | `Kush Cake` | strain | ok | Kush Cake card (in stock, so no alternates) |
| X-11 | `Amplified` | strain (out of stock) | ok | Amplified card + "In stock and close to it" by cosine: Baklava; Permafrost; Verzace |
| X-12 | `something like Kush Cake but more uplifting` | recommend {uplift:24} like=kush cake, exclude kush cake | ok | Bubba Verde (2.2245); Honeycomb Pave #4 (2.1673); Saffire (1.9534) |
| X-13 | `squid inc` | strain (fuzzy, 1 edit) | ok | Squid Ink |
| X-14 | `hello there` | unknown | help | help text |
| X-15 | `trouble sleeping but gotta work at 6` | recommend {anxiety_relief:40} cap {sedation:38} | ok | Bubba Verde (1.7909); Honeycomb Pave #4 (1.693); Slurricane (1.5316). **New defect candidate**: `_sleepAsk` (L16086) matches only `sleep|insomnia`, not "sleeping", so the work cap removes the sleep request. See GAP-206 |
| X-16 | `most myrcene without linalool` | terpene_rank excl=Linalool | ok | empty: 61 strains contain linalool, 5 have no linalool result, and the one clear strain has no myrcene |
| X-17 | `Kush Cake without myrcene` | strain excl=β-Myrcene | ok | Kush Cake card + "Kush Cake contains β-Myrcene." (MC-1 behaviour) |
| X-18 | `energy` [tiers=premium] | recommend {uplift:28} cap {sedation:36} | **none** | both passes empty → "Nothing matched" with retry chips |

## Unit goldens (in `golden_cases.json`)

- `batchScores`: single batches, so no averaging. Examples: Kush Cake `FLOK020926` → domains {sed 50, up 31, anx 68, pain 59, foc 12, anti 41}, cluster 6 / secondary 1, anxiety risk 24. Amplified `AMPD081825` → {61, 52, 99, 99, 33, 91}, cluster 6/2, anxiety 15.
- `averaging`: Zero Gravity, 25 batches of which 3 are in stock (dated 2026-07-01 / 08-04 / 08-25). Recency-weighted average: BCP 0.833411, limonene 0.465071, humulene 0.419378, linalool 0.287876, ocimene 0.277476.
- `pricing`: for example House Fresh Thu = 14/28/56/66.99 → $17.50/$35.00/$70.05/$83.80 post-tax. House Fresh Tue/Sat deal = 10.50/21/42/56.99 → $13.10/$26.25/$52.50/$71.25. Tier 3 Mon = 3.5 g $19.99 → $25.00. No tier → all 0 (no price).

## Invariants the port must hold (from the cases)

1. An out-of-stock strain is never in a recommend, terpene-rank or Similar result (X-11 shows it only as the looked-up card).
2. An excluded terpene with a missing lab value means the strain is excluded, not assumed clear (X-01, X-16).
3. Ranking uses unclamped raw scores. Ties on display 99 still order deterministically (RC-03, RC-09, RC-15 are identical because the parse is equivalent).
4. A price intent of type `budget` does not change ranking. `hasBudget` filters but does not re-rank (RC-20, X-06).
5. A query with only negative constraints ranks by the tier nudge minus the headroom penalty (RC-08: ms values near 0).
6. The fallback runs exactly once, with crit ×0.60 floored and caps +12 (X-07). If that fails, the result is "none" (X-18).

---

## Appendix A: `engine.js`

```js
// MIG-001 headless harness: runs the v7.11.4 engine's own source lines in a Node vm.
// Usage: const E=require('./engine')(htmlPath, inventoryJsonPath)
const fs = require('fs'), vm = require('vm'), crypto = require('crypto');

// 1-based inclusive line ranges in deploy/2026-10-30-v7114/site/index.html (md5 228684e9...)
const RANGES = [
  [14755, 14771], // esc, _cleanText, _safeId/_safeTier/_safeColor, _safeRecord, _safeBrand
  [14806, 14846], // _customerProfile, setCustomerProfile, applyProfileFilter, applyProfileSort
  [15040, 16686], // tiers, DOMS, DB, CL, NF, BA, freshness, scoring, clusters, findStrains, grouping, INTENTS, parser, roles, renderStrain, respond
  [17512, 17528], // SK keys, _prefs defaults
  [17650, 17650], // let _brands
  [17674, 17680], // _backfillDates
  [18594, 18594], // let _activeTiers
  [19718, 19732], // _sanitizeImport
  [20514, 20533], // parseBatchDate
  [20813, 20822], // slCosineSim
  [21008, 21256], // pricing constants + resolver
  [21696, 21795], // PRICE_INTENTS, detectPriceIntent, buildPriceResponse
];

// Clock pinned to the inventory export time so dow-dependent pricing and display ages are reproducible.
const FIXED_NOW = Date.parse('2026-10-29T19:13:36.534Z'); // Thursday (dow 4) in UTC and in Arizona (UTC-7)
class FixedDate extends Date { constructor(...a) { a.length ? super(...a) : super(FIXED_NOW); } static now() { return FIXED_NOW; } }
module.exports = function load(htmlPath, invPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const lines = html.split('\n');
  const src = RANGES.map(([a, b]) => lines.slice(a - 1, b).join('\n')).join('\n');
  const store = {};
  const ctx = {
    console, Math, Date: FixedDate, JSON, Object, Array, Set, Map, RegExp, String, Number, parseInt, parseFloat, isNaN, encodeURIComponent,
    localStorage: { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); }, removeItem: k => { delete store[k]; } },
    document: { getElementById: () => null, body: { classList: { toggle() {} } } },
    window: {}, _cloud: null, _staffCur: '', _usage: [],
  };
  vm.createContext(ctx);
  // expose let/const bindings through a getter object
  vm.runInContext(src + `
    ;globalThis.__E={
      get STRAINS(){return STRAINS}, setProfile(v){_customerProfile=v}, setTiers(a){_activeTiers=new Set(a)},
      setBrands(b){_brands=b}, prefs:_prefs, pricing(){return _pricing},
      parseQuery, detectPriceIntent, findStrains, respond, analyzeGroup, getStrainGroups, averageProfile, scoreDomains, scoreRaw,
      classifyCluster, calcAnxietyRisk, buildRoleTags, slCosineSim, getEffectivePrices, buildPriceRows, applyTax, priceFloor,
      exclStatus, profileIds, batchInStock, _sanitizeImport, _backfillDates, _invalidateCache, loadPricing, INTENTS, DB, CL, NF,
      setRender(f){renderStrain=f},
      calls:[], wrapFind(){const o=findStrains;const c=this.calls;findStrains=function(...a){const r=o.apply(this,a);c.push({crit:a[0],neg:a[1],primary:a[3],r});return r;};}
    };`, ctx, { filename: 'tfs-v7114-slices.js' });
  const E = ctx.__E;
  const raw = fs.readFileSync(invPath);
  const inv = JSON.parse(raw);
  const san = E._sanitizeImport(inv.custom);
  Object.assign(E.STRAINS, san.clean);
  (inv.deleted || []).forEach(id => { delete E.STRAINS[id]; }); // loadStorage line 17662
  E.setBrands(inv.brands || []);
  E._invalidateCache(); E._backfillDates();
  E.loadPricing(); // no saved pricing in the snapshot -> TIER_DEFAULTS / DEFAULT_DAY_DEALS / tax 25.1
  E.meta = {
    htmlMd5: crypto.createHash('md5').update(html).digest('hex'),
    invMd5: crypto.createHash('md5').update(raw).digest('hex'),
    invVersion: inv.version, invExported: inv.exported, records: Object.keys(inv.custom).length,
    kept: Object.keys(E.STRAINS).length, skipped: san.skipped,
  };
  // renderStrain is DOM-string heavy; replace with a marker so respond() can be read back
  E.setRender((a, rank, ms) => `<<${a.id}>>`);
  E.wrapFind();
  return E;
};
```

## Appendix B: `golden.js`

```js
// MIG-001 golden-case generator. node golden.js <index.html> <tfs-inventory-master.json> <out.json>
process.env.TZ = 'America/Phoenix';
const fs = require('fs');
const [, , HTML, INV, OUT] = process.argv;
const E = require('./engine')(HTML, INV);

// q: query as typed into the chat box. Optional state: profile ('new'|'exp'), tiers (active tier chips), resultCount.
const CASES = [
  // the tool's own 21 fixed ranking questions (tfs-budtender tests/tests/rank_compare.py QUERIES)
  ...["something for sleep", "can't sleep", "stress relief", "pain", "focus for work", "creative",
    "uplifting but no couch lock", "need to drive", "anxiety", "energy", "insomnia", "relaxing body high",
    "happy social", "inflammation", "calming", "something for the day", "heavy indica",
    "back pain without sedation", "chill evening", "something cheap for sleep", "what has the most limonene"]
    .map((q, i) => ({ id: `RC-${String(i + 1).padStart(2, '0')}`, q, why: 'rank_compare.py fixed question' })),
  { id: 'X-01', q: 'sleep without limonene', why: 'hard terpene exclusion (EXCL_MAX_PCT, unknown = excluded)' },
  { id: 'X-02', q: 'no pinene, something for pain', why: 'family exclusion (pinene -> alpha+beta)' },
  { id: 'X-03', q: 'sleep', profile: 'new', why: 'new-customer profile: anxietyRisk<=60 filter + myrcene onset penalty' },
  { id: 'X-04', q: 'sleep', why: 'baseline for X-03' },
  { id: 'X-05', q: 'sleep', tiers: ['t3'], why: 'tier chip filter' },
  { id: 'X-06', q: 'I only have $15 for sleep', why: 'hasBudget -> opts.maxPrice post-tax' },
  { id: 'X-07', q: 'sinking', tiers: ['t1'], why: 'Tier 1 only: no strain meets sedation>=55, so the relaxed pass runs (crit x0.60 floored, caps +12)' },
  { id: 'X-08', q: 'first time, wont make me paranoid', why: 'beginner: high anxiety_relief floor + uplift cap' },
  { id: 'X-09', q: 'compare Kush Cake vs Squid Ink', why: 'compare intent: key difference domain' },
  { id: 'X-10', q: 'Kush Cake', why: 'in-stock strain lookup' },
  { id: 'X-11', q: 'Amplified', why: 'out-of-stock strain lookup -> "in stock and close to it" by cosine' },
  { id: 'X-12', q: 'something like Kush Cake but more uplifting', why: 'like-X-but: likeKey cosine bonus, X excluded' },
  { id: 'X-13', q: 'squid inc', why: 'fuzzy strain name (Levenshtein tolerance 1 for 5-7 letters)' },
  { id: 'X-14', q: 'hello there', why: 'unknown intent -> help text' },
  { id: 'X-15', q: 'trouble sleeping but gotta work at 6', why: 'sleep ask keeps sedation (work cap suppressed)' },
  { id: 'X-16', q: 'most myrcene without linalool', why: 'terpene rank with exclusion' },
  { id: 'X-18', q: 'energy', tiers: ['premium'], why: 'TFS Premium only: nothing passes even relaxed -> "Nothing matched"' },
  { id: 'X-17', q: 'Kush Cake without myrcene', why: 'strain lookup keeps exclusion (MC-1) -> contains note' },
];

const r4 = x => Math.round(x * 1e4) / 1e4;
const brief = a => ({ key: a.id, name: a.strain.name, ms: a.ms === undefined ? undefined : r4(a.ms),
  batches: a.strain.batchCount, tier: E.STRAINS[E.getStrainGroups()[a.id].ids[0]].tier || '',
  cluster: a.cluster.primary, cluster2: a.cluster.secondary, anxietyRisk: a.anxietyRisk, domains: a.domains });

const out = { meta: { ...E.meta, clock: '2026-10-29T19:13:36.534Z (Thu, dow 4), TZ America/Phoenix',
  state: 'local mode defaults: _prefs.resultCount 3, painFunctional true, _customerProfile null, _activeTiers empty, pricing = TIER_DEFAULTS + DEFAULT_DAY_DEALS, tax 25.1',
  inStockGroups: Object.keys(E.getStrainGroups()).filter(k => E.batchInStock(E.STRAINS[E.getStrainGroups()[k].ids[0]])).length,
  groups: Object.keys(E.getStrainGroups()).length }, cases: [] };

for (const c of CASES) {
  E.setProfile(c.profile || null); E.setTiers(c.tiers || []); E.calls.length = 0;
  const parsed = E.parseQuery(c.q);                         // submit(), line 19542
  parsed._priceIntent = E.detectPriceIntent(c.q);
  const html = E.respond(parsed);
  const shown = [...html.matchAll(/<<([^>]+)>>/g)].map(m => m[1]);
  const p = { intent: parsed.intent, crit: parsed.crit, neg: parsed.neg, primary: parsed.primary, lbls: parsed.lbls, tf: parsed.tf,
    opts: parsed.opts, excl: parsed.excl && parsed.excl.map(e => e.name), strains: parsed.strains, groupKey: parsed.groupKey,
    terpene: parsed.terpene, priceIntent: parsed._priceIntent };
  const res = { ...c, parsed: JSON.parse(JSON.stringify(p)),
    outcome: /No exact match/.test(html) ? 'fallback' : /Nothing matched/.test(html) ? 'none' : /verified free/.test(html) && !shown.length ? 'excluded-all'
      : /<div class="no-res">Try:/.test(html) ? 'help' : 'ok',
    findStrainsCalls: E.calls.map(k => ({ crit: k.crit, neg: k.neg, primary: k.primary, top: k.r.map(brief) })),
    shown };
  if (E.calls.length && E.calls[E.calls.length - 1].r.length) {
    const final = E.calls[E.calls.length - 1].r;
    res.roleTags = E.buildRoleTags(final, parsed.primary);
  }
  if (parsed.intent === 'terpene_rank') res.terpRank = [...html.matchAll(/<span class="tr-name">([^<]+?)(?: <span|<\/span>)[\s\S]*?<span class="tr-pct">([\d.]+)%/g)].map(m => [m[1].trim(), +m[2]]);
  if (parsed.intent === 'compare') res.compareNote = (html.match(/Key difference: ([^<]+)<\/strong>: ([^<]+?)\. /) || []).slice(1);
  if (parsed.intent === 'strain' || parsed.intent === 'compare') res.cards = shown.map(k => brief(E.analyzeGroup(k, E.getStrainGroups())));
  if (/excl-note/.test(html)) res.exclNote = html.match(/<strong>([^<]+)<\/strong>/)[1];
  out.cases.push(res);
}

// Pricing goldens: every tier x every weekday, pre-tax and post-tax (getEffectivePrices + buildPriceRows)
out.pricing = {};
for (const t of ['smalls', 'house', 'premium', 'fttp', 't1', 't2', 't3', 't4', ''])
  out.pricing[t || '(none)'] = [0, 1, 2, 3, 4, 5, 6].map(dow => { const e = E.getEffectivePrices(t, '', 'x', dow);
    return { dow, deal: e.dealActive ? e.dealLabel : null, rows: E.buildPriceRows(e.prices).map(r => [r.g, r.pre, r.post]) }; });

// Scoring unit goldens on single real batches (no averaging): scoreDomains / scoreRaw / classifyCluster / calcAnxietyRisk
out.batchScores = ['Kush Cake', 'Scented Marker', 'Bubba Verde', 'Amplified'].map(n => {
  const id = Object.keys(E.STRAINS).find(k => E.STRAINS[k].name === n); const s = E.STRAINS[id];
  return { id, name: n, batch: s.batch, date: s.date || null, p: s.p, domains: E.scoreDomains(s.p, 0),
    raw: Object.fromEntries(Object.entries(E.scoreRaw(s.p, 0)).map(([k, v]) => [k, r4(v)])),
    cluster: E.classifyCluster(s.p), anxietyRisk: E.calcAnxietyRisk(s.p) };
});
// Batch-averaging golden on a multi-batch in-stock strain
{ const g = E.getStrainGroups()['zero gravity']; const live = E.profileIds(g.ids);
  out.averaging = { key: 'zero gravity', batchesTotal: g.ids.length, liveBatches: live.map(id => ({ id, batch: E.STRAINS[id].batch, date: E.STRAINS[id].date || null })),
    avgTop5: Object.entries(E.averageProfile(g.ids)).sort((a, b) => b[1] - a[1]).slice(0, 5) }; }

fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.log(out.cases.map(c => `${c.id.padEnd(6)} ${c.outcome.padEnd(9)} ${c.parsed.intent.padEnd(13)} ${JSON.stringify(c.q)} -> ${(c.findStrainsCalls.at(-1)?.top.map(t => t.name + ':' + t.ms) || c.cards?.map(t => t.name) || c.terpRank?.slice(0, 3) || []).join(' | ')}`).join('\n'));
```
