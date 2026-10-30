#!/usr/bin/env node
// DATA-001 catalog importer (GAME-001). Deterministic: same sources -> byte-identical output.
// Reads (never writes) the TFS budtender tool: inventory master JSON + engine tables from v7.11.4 index.html.
// Writes allow-listed fields only (DATA_SCHEMA.md §5, DEC-006) to UnityProject/Assets/_Game/Data/Catalog/.
// Usage: node Tools/Data/import_catalog.js [--check]   (--check: re-validate existing output against the allow-list only)
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), crypto = require('crypto');

const IMPORTER_VERSION = '1.0.0';
const TFS_ROOT = process.env.TFS_BUDTENDER_ROOT || 'C:/Users/handl/Downloads/tfs-budtender';
const HTML = path.join(TFS_ROOT, 'deploy/2026-10-30-v7114/site/index.html');
const INV = path.join(TFS_ROOT, 'inventory/tfs-inventory-master.json');
const EXPECTED_HTML_MD5 = '228684e9f02d703cf3a36692baf10d18'; // v7.11.4 (DEC-001/002); line refs below depend on it
const OUT = path.join(__dirname, '../../UnityProject/Assets/_Game/Data/Catalog');

// Every key allowed anywhere in the output, per file. Anything else fails the run (PII guard, DEC-006).
const ALLOW = {
  'batches.json': ['batches', 'id', 'strainName', 'batchCode', 'brand', 'tier', 'inStock', 'testDate', 'dateInferred', 'total', 'terpenes'],
  'terpenes.json': ['domains', 'terpenes', 'id', 'name', 'cls', 'd', 'baScalars', 'sedation', 'uplift', 'anxiety_relief', 'pain_inflammation', 'focus_cognitive', 'antimicrobial'],
  'engine_tables.json': ['clusterBonus', 'tierNudge', 'intents', 'd', 'neg', 'lbl', 'pri', '1', '2', '4', '5', '6',
    'sedation', 'uplift', 'anxiety_relief', 'pain_inflammation', 'focus_cognitive', 'antimicrobial',
    'smalls', 'house', 'premium', 'fttp', 't1', 't2', 't3', 't4'],
  'pricing.json': ['taxRate', 'weights', 'tiers', 'dayDeals', 'id', 'name', 'gpg', 'w', 'dow', 'deals', 'active', 'target', 'type', 'value',
    'dealType', 'weight', 'flatPrice', '3.5', '7', '14', '28'],
  'manifest.json': ['importer', 'version', 'sources', 'outputs', 'counts', 'path', 'md5', 'invVersion', 'invExported', 'file',
    'batches', 'inStockBatches', 'strainGroups', 'terpenes', 'intents', 'skipped', 'deleted', 'datesInferred'],
};
// Intent keys are free-text search keys (e.g. 'knock me out'), so engine_tables.json/intents keys are checked by shape, not by list.
const INTENT_KEY_RE = /^[a-z0-9 '\-.\/&+]{1,40}$/;

function md5(buf) { return crypto.createHash('md5').update(buf).digest('hex'); }

// Pull the object/array literal assigned by `const NAME=` out of the page source (strings/comments aware).
function literal(src, name) {
  const start = src.indexOf(`const ${name}=`);
  if (start < 0) throw new Error(`literal ${name} not found`);
  let i = src.indexOf('=', start) + 1, depth = 0, q = null;
  const from = i;
  for (; i < src.length; i++) {
    const c = src[i];
    if (q) { if (c === '\\') i++; else if (c === q) q = null; continue; }
    if (c === "'" || c === '"' || c === '`') { q = c; continue; }
    if (c === '/' && src[i + 1] === '/') { i = src.indexOf('\n', i); continue; }
    if (c === '{' || c === '[') depth++;
    else if (c === '}' || c === ']') { if (--depth === 0) break; }
  }
  return vm.runInNewContext('(' + src.slice(from, i + 1) + ')', Object.create(null), { timeout: 1000 });
}

// v7.11.4 L14756 _cleanText
const cleanText = s => String(s ?? '').replace(/[<>\u0000-\u001f]/g, '').trim();
const safeTier = t => /^[A-Za-z0-9_-]{1,40}$/.test(String(t));
const safeId = id => /^[A-Za-z0-9._:-]{1,200}$/.test(String(id));
// v7.11.4 L15434 normName
const normName = n => n.toLowerCase().replace(/[^a-z0-9]/g, ' ').replace(/\s+/g, ' ').trim();
// v7.11.4 L20514 parseBatchDate
function parseBatchDate(batch) {
  if (!batch) return null;
  let m = batch.match(/(\d{2})(\d{2})(\d{2})$/);
  if (m) { const [, mo, dy, yr] = m; if (+mo >= 1 && +mo <= 12 && +dy >= 1 && +dy <= 31 && +yr >= 24 && +yr <= 30) return `20${yr}-${mo}-${dy}`; }
  m = batch.match(/(\d{2})(\d{2})(\d{2})/);
  if (m) { const [, a, b, c] = m; if (+a >= 24 && +a <= 30 && +b >= 1 && +b <= 12 && +c >= 1 && +c <= 31) return `20${a}-${b}-${c}`; }
  return null;
}

function checkAllowList(file, obj) {
  const bad = [];
  const walk = (v, p, inIntents) => {
    if (Array.isArray(v)) return v.forEach((x, i) => walk(x, `${p}[${i}]`, false));
    if (!v || typeof v !== 'object') return;
    for (const k of Object.keys(v)) {
      const isIntentKey = inIntents;
      const isTerpKey = file === 'batches.json' && p.endsWith('.terpenes');
      const isTerpId = file === 'terpenes.json' && p === '$.baScalars';
      const ok = isIntentKey ? INTENT_KEY_RE.test(k) : (isTerpKey || isTerpId) ? /^[a-z0-9_]{1,40}$/.test(k) : ALLOW[file].includes(k);
      if (!ok) bad.push(`${file}: ${p}.${k}`);
      walk(v[k], `${p}.${k}`, file === 'engine_tables.json' && p === '$' && k === 'intents');
    }
  };
  walk(obj, '$', false);
  return bad;
}

function write(file, obj) {
  const text = JSON.stringify(obj, null, 1) + '\n';
  fs.writeFileSync(path.join(OUT, file), text, 'utf8');
  return { file, md5: md5(Buffer.from(text, 'utf8')) };
}

function check() {
  const bad = [];
  for (const f of Object.keys(ALLOW)) bad.push(...checkAllowList(f, JSON.parse(fs.readFileSync(path.join(OUT, f), 'utf8'))));
  if (bad.length) { console.error('ALLOW-LIST FAIL\n' + bad.slice(0, 50).join('\n')); process.exit(1); }
  console.log('allow-list OK: ' + Object.keys(ALLOW).join(', '));
}

function main() {
  if (process.argv.includes('--check')) return check();
  const htmlBuf = fs.readFileSync(HTML), invBuf = fs.readFileSync(INV);
  if (md5(htmlBuf) !== EXPECTED_HTML_MD5) throw new Error(`index.html md5 ${md5(htmlBuf)} != pinned v7.11.4 ${EXPECTED_HTML_MD5}`);
  const src = htmlBuf.toString('utf8');
  const inv = JSON.parse(invBuf.toString('utf8'));

  // Engine tables (DATA_SCHEMA §2-4)
  const DOMS = literal(src, 'DOMS').map(d => d.id);           // L15042
  const DB = literal(src, 'DB');                               // L15044
  const BA = literal(src, 'BA_SCALARS');                       // L15127
  const CB = literal(src, 'CLUSTER_BONUS');                    // L15327
  const INTENTS = literal(src, 'INTENTS');                     // L15619
  const TIER_DEFAULTS = literal(src, 'TIER_DEFAULTS');         // L21018
  const DAY_DEALS = literal(src, 'DEFAULT_DAY_DEALS');         // L21036
  const WEIGHTS = literal(src, 'STD_WEIGHTS');                 // L21010
  const tierNudgeSrc = src.match(/const _tierVal=(\{[^}]*\});/); // findStrains L15408
  const tierNudge = vm.runInNewContext('(' + tierNudgeSrc[1] + ')', Object.create(null));
  const taxRate = Number(src.match(/let _pricing=\{\s*taxRate:([\d.]+)/)[1]); // L21062

  const pick = (o, keys) => Object.fromEntries(keys.filter(k => o[k] !== undefined).map(k => [k, o[k]]));
  const terpenes = {
    domains: DOMS,
    terpenes: Object.entries(DB).map(([id, t]) => ({ id, name: t.name, cls: t.cls, d: Object.fromEntries(DOMS.map(d => [d, t.d[d] || 0])) })),
    baScalars: BA,
  };
  const tables = {
    clusterBonus: CB,
    tierNudge,
    intents: Object.fromEntries(Object.entries(INTENTS).map(([k, v]) => [k, pick(v, ['d', 'neg', 'lbl', 'pri'])])),
  };
  const pricing = {
    taxRate,
    weights: WEIGHTS,
    tiers: Object.entries(TIER_DEFAULTS).map(([id, t]) => ({ id, gpg: t.gpg, w: t.w })),
    dayDeals: Object.keys(DAY_DEALS).map(Number).sort((a, b) => a - b).map(dow => ({
      dow, deals: DAY_DEALS[dow].map(x => pick(x, ['id', 'name', 'active', 'target', 'dealType', 'weight', 'flatPrice', 'w'])),
    })),
  };
  for (const day of Object.values(DAY_DEALS).flat())
    if (!['tier'].includes(day.target.type) || !['weight_table', 'weight_flat'].includes(day.dealType))
      throw new Error(`deal ${day.id} uses a target/dealType the slice engine does not port`);

  // Batches: _sanitizeImport L19718 + _safeRecord L14762 + deleted L17662 + _backfillDates L17674
  const deleted = new Set(inv.deleted || []);
  const batches = []; let skipped = 0, inferred = 0;
  for (const [id, s] of Object.entries(inv.custom || {})) {
    if (deleted.has(id)) continue;
    if (!safeId(id) || !s || typeof s !== 'object' || typeof s.name !== 'string' || !cleanText(s.name) || !s.p || typeof s.p !== 'object') { skipped++; continue; }
    const p = [];
    for (const [k, v] of Object.entries(s.p)) { const n = Number(v); if (Number.isFinite(n) && n >= 0 && n < 50) p.push([k, n]); }
    if (!p.some(([, v]) => v > 0)) { skipped++; continue; }
    const total = Number.isFinite(Number(s.total)) ? Number(s.total) : parseFloat(p.reduce((a, [, v]) => a + v, 0).toFixed(4));
    const tier = s.tier != null && s.tier !== '' && !safeTier(s.tier) ? '' : (s.tier || '');
    const batchCode = cleanText(typeof s.batch === 'string' || typeof s.batch === 'number' ? s.batch : '');
    let testDate = s.date || null, dateInferred = false;
    if (!testDate) { testDate = parseBatchDate(batchCode); dateInferred = !!testDate; if (dateInferred) inferred++; }
    batches.push({ id, strainName: cleanText(s.name), batchCode, brand: s.brand != null ? cleanText(s.brand) : '', tier,
      inStock: s.status !== 'oos', testDate, dateInferred, total, terpenes: Object.fromEntries(p) });
  }

  const files = { 'batches.json': { batches }, 'terpenes.json': terpenes, 'engine_tables.json': tables, 'pricing.json': pricing };
  const bad = Object.entries(files).flatMap(([f, o]) => checkAllowList(f, o));
  if (bad.length) throw new Error('ALLOW-LIST FAIL\n' + bad.slice(0, 50).join('\n'));

  fs.mkdirSync(OUT, { recursive: true });
  const outputs = Object.entries(files).map(([f, o]) => write(f, o));
  const manifest = {
    importer: { path: 'Tools/Data/import_catalog.js', version: IMPORTER_VERSION },
    sources: [
      { path: 'tfs-budtender/deploy/2026-10-30-v7114/site/index.html', md5: md5(htmlBuf), version: 'v7.11.4' },
      { path: 'tfs-budtender/inventory/tfs-inventory-master.json', md5: md5(invBuf), invVersion: inv.version, invExported: inv.exported },
    ],
    outputs,
    counts: { batches: batches.length, inStockBatches: batches.filter(b => b.inStock).length,
      strainGroups: new Set(batches.map(b => normName(b.strainName))).size, terpenes: terpenes.terpenes.length,
      intents: Object.keys(tables.intents).length, skipped, deleted: deleted.size, datesInferred: inferred },
  };
  const bm = checkAllowList('manifest.json', manifest);
  if (bm.length) throw new Error('ALLOW-LIST FAIL\n' + bm.join('\n'));
  write('manifest.json', manifest);
  console.log(JSON.stringify(manifest.counts), 'manifest md5', md5(fs.readFileSync(path.join(OUT, 'manifest.json'))));
}

main();
