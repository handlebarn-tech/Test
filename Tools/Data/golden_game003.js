#!/usr/bin/env node
// GAME-003 parser goldens: runs the v7.11.4 engine's own source (MIG-001 harness, GOLDEN_CASES.md Appendix A) on extra queries,
// and on a copy of the page with the two game fixes patched in (DEC-016), so game-expected values are executed, not hand-written.
// Reads the tool read-only (copies to a temp dir). Usage: node Tools/Data/golden_game003.js [out.json]
'use strict';
process.env.TZ = 'America/Phoenix';
const fs = require('fs'), path = require('path'), os = require('os'), crypto = require('crypto');

const TFS_ROOT = process.env.TFS_BUDTENDER_ROOT || 'C:/Users/handl/Downloads/tfs-budtender';
const HTML = path.join(TFS_ROOT, 'deploy/2026-10-30-v7114/site/index.html');
const INV = path.join(TFS_ROOT, 'inventory/tfs-inventory-master.json');
const REPO = path.join(__dirname, '../..');
const OUT = process.argv[2] || path.join(REPO, 'Docs/Reconstruction/golden_cases_game003.json');
const md5 = b => crypto.createHash('md5').update(b).digest('hex');

// Game fixes as exact one-line source patches (line numbers unchanged, so the harness ranges stay valid).
const FIXES = {
  // MC-7, as v7.11.5 ships it (dev/v7115/fixes.py L44-46): 'for the day' gets the daytime numbers
  'MC-7': [15658, "daytime:{d:{uplift:22,focus_cognitive:14},neg:{sedation:32},lbl:'daytime',pri:'uplift'},",
    "daytime:{d:{uplift:22,focus_cognitive:14},neg:{sedation:32},lbl:'daytime',pri:'uplift'},'for the day':{d:{uplift:22,focus_cognitive:14},neg:{sedation:32},lbl:'daytime',pri:'uplift'},"],
  // GAP-206: _sleepAsk also matches "sleeping"
  'GAP-206': [16086, 'const _sleepAsk=/\\b(sleep|insomnia)\\b/.test(qi)', 'const _sleepAsk=/\\b(sleep\\w*|insomnia)\\b/.test(qi)'],
};

// Parser coverage under v7.11.4: PHRASE_MAP, negation patterns, fuzzy fallback, price intents, exclusions, names, terpenes.
const V7114 = ['back is killing me', 'knee pain', 'racing thoughts', 'morning pick me up', 'before the gym', 'going out tonight',
  'lost my appetite', 'low tolerance', 'brain fog', 'tossing and turning', 'wired but tired', 'jet lag', 'micro dose', 'nothing too strong',
  'sciatica', 'need to drive later, something for pain', 'no couch lock, still be able to work', 'not too racy, energy',
  'without getting too heavy for anxiety', 'indica', 'hybrid please', 'tense', 'sativa', 'relax', 'best value for sleep',
  'budget of $40 for pain', "money isn't an issue, something for sleep", '$30 budget', 'cheap', 'linalool-free sleep',
  'allergic to limonene and pinene, pain', 'avoid bcp', 'compare Kush Cake, Squid Ink and Bubba Verde',
  'something like Squid Ink but without myrcene', 'something like Bubba Verde but less sedating', 'most terpinolene',
  'sleep high in linalool', 'lavender', 'bubba verd', 'which has the most bcp', 'help me sleep', 'first time user',
  'creative energy but not too racy', 'a couple joints for joint pain', 'customer wants pre-rolls for sleep', 'kush', 'Kush Cake vs',
  'w/o limonene for focus', 'alpha pinene free', 'he says his back hurts and he has to drive', 'i have $12, something for anxiety',
  'night shift', 'overthinking', 'philosophical'];
// Each defect query under v7.11.4 and under its fix
const DEFECT_CASES = [{ id: 'MC-7', q: 'something for the day' }, { id: 'GAP-206', q: 'trouble sleeping but gotta work at 6' }];

function harness(dir) {
  const md = fs.readFileSync(path.join(REPO, 'Docs/Reconstruction/GOLDEN_CASES.md'), 'utf8');
  const a = md.slice(md.indexOf('## Appendix A'));
  const code = a.slice(a.indexOf('```js') + 5, a.indexOf('```', a.indexOf('```js') + 5));
  fs.writeFileSync(path.join(dir, 'engine.js'), code);
  return require(path.join(dir, 'engine.js'));
}

function run(E, q) {
  E.setProfile(null); E.setTiers([]); E.calls.length = 0;
  const parsed = E.parseQuery(q);
  parsed._priceIntent = E.detectPriceIntent(q);
  const drive = /\b(driv(e|es|ing)|drove)\b/i.test(q) && !/\bno drive\b/i.test(q); // submit L19545
  const html = E.respond(parsed);
  const shown = [...html.matchAll(/<<([^>]+)>>/g)].map(m => m[1]);
  const r4 = x => Math.round(x * 1e4) / 1e4;
  const brief = s => ({ key: s.id, ms: s.ms === undefined ? undefined : r4(s.ms) });
  const res = { q, parsed: JSON.parse(JSON.stringify({ intent: parsed.intent, crit: parsed.crit, neg: parsed.neg, primary: parsed.primary,
      lbls: parsed.lbls, tf: parsed.tf, opts: parsed.opts, excl: parsed.excl && parsed.excl.map(e => e.name), strains: parsed.strains,
      groupKey: parsed.groupKey, terpene: parsed.terpene, priceIntent: parsed._priceIntent, drive })),
    outcome: /No exact match/.test(html) ? 'fallback' : /Nothing matched/.test(html) ? 'none' : /verified free/.test(html) && !shown.length ? 'excluded-all'
      : /<div class="no-res">Try:/.test(html) ? 'help' : 'ok',
    calls: E.calls.map(k => ({ crit: k.crit, neg: k.neg, top: k.r.map(brief) })), shown };
  if (E.calls.length && E.calls[E.calls.length - 1].r.length) res.roleTags = E.buildRoleTags(E.calls[E.calls.length - 1].r, parsed.primary);
  if (parsed.intent === 'terpene_rank') res.terpRank = [...html.matchAll(/<span class="tr-name">([^<]+?)(?: <span|<\/span>)[\s\S]*?<span class="tr-pct">([\d.]+)%/g)].map(m => [m[1].trim(), +m[2]]);
  if (parsed.intent === 'compare') res.compareNote = (html.match(/Key difference: ([^<]+)<\/strong>: ([^<]+?)\. /) || []).slice(1);
  if (/excl-note/.test(html)) res.exclNote = html.match(/<strong>([^<]+)<\/strong>/)[1];
  if (parsed.intent === 'recommend' && res.outcome === 'ok') // Show more options L19450: n=40 with the effective opts, next 3 unseen
  { const all = E.findStrains(parsed.crit, parsed.neg, 40, parsed.primary, parsed.opts || {});
    if (parsed.tf) all.sort((a, b) => (b.strain.p[parsed.tf] || 0) - (a.strain.p[parsed.tf] || 0));
    res.more = all.map(s => s.id).filter(k => !shown.includes(k)).slice(0, 3); }
  return res;
}

function main() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'game003-'));
  try {
    const htmlBuf = fs.readFileSync(HTML);
    if (md5(htmlBuf) !== '228684e9f02d703cf3a36692baf10d18') throw new Error('index.html is not the pinned v7.11.4');
    fs.copyFileSync(INV, path.join(tmp, 'inv.json'));
    const lines = htmlBuf.toString('utf8').split('\n');
    for (const [id, [ln, from, to]] of Object.entries(FIXES)) {
      if (!lines[ln - 1].includes(from)) throw new Error(`${id}: L${ln} does not contain the expected source`);
      lines[ln - 1] = lines[ln - 1].replace(from, to);
    }
    fs.writeFileSync(path.join(tmp, 'v7114.html'), htmlBuf);
    fs.writeFileSync(path.join(tmp, 'game.html'), lines.join('\n'));
    const load = harness(tmp);
    const E = load(path.join(tmp, 'v7114.html'), path.join(tmp, 'inv.json'));
    const G = load(path.join(tmp, 'game.html'), path.join(tmp, 'inv.json'));
    const out = {
      meta: { generator: 'Tools/Data/golden_game003.js', htmlMd5: md5(htmlBuf), invMd5: md5(fs.readFileSync(INV)), clock: 'Thu dow 4 (MIG-001 harness)',
        state: 'MIG-001 local-mode defaults', fixes: Object.fromEntries(Object.entries(FIXES).map(([k, v]) => [k, `L${v[0]}: ${v[2]}`])) },
      v7114: V7114.map(q => run(E, q)),
      defects: DEFECT_CASES.map(c => ({ id: c.id, v7114: run(E, c.q), game: run(G, c.q) })),
    };
    fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + '\n');
    for (const c of out.v7114) console.log(c.outcome.padEnd(12), c.parsed.intent.padEnd(13), JSON.stringify(c.q), '->', c.shown.join(', '));
    for (const d of out.defects) console.log(d.id, 'v7.11.4', d.v7114.outcome, d.v7114.shown.join(', '), '| game', d.game.outcome, d.game.shown.join(', '));
  } finally { fs.rmSync(tmp, { recursive: true, force: true }); }
}
main();
