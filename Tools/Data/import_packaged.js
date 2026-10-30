#!/usr/bin/env node
// DATA-002 packaged-goods importer (SPEC_GAME004). Deterministic: same export -> byte-identical output.
// Reads (never writes, never copies) a Dutchie "Current Inventory" .xlsx export. Only WHITELIST columns are read; cost, vendor,
// quantity, package/batch/external IDs, location and dates never reach the output (DEC-006).
// Writes UnityProject/Assets/_Game/Data/Catalog/packaged_catalog.json (categories DEC-034, limits DEC-048, storage DEC-050).
// Usage: node Tools/Data/import_packaged.js [export.xlsx]        (default: the one .xlsx in Downloads/Dispo Game Imports/, else the archived 2026-10-30 export, DEC-070)
//        node Tools/Data/import_packaged.js --check [export.xlsx] (re-validate the existing output; with the export, also the dropped-value scan)
//        node Tools/Data/import_packaged.js --selftest            (asserts the guards catch planted leaks)
'use strict';
const fs = require('fs'), path = require('path'), zlib = require('zlib'), crypto = require('crypto'), assert = require('assert');

const IMPORTER_VERSION = '1.0.0';
const DROP_DIR = 'C:/Users/handl/Downloads/Dispo Game Imports'; // fresh imports only (DEC-070)
const ARCHIVE_DIR = 'C:/Users/handl/Downloads/Dispo Game Imports Archive/2026-10-30_dutchie-inventory'; // the export DATA-002 was built from
const OUT = path.join(__dirname, '../../UnityProject/Assets/_Game/Data/Catalog');
const OUT_FILE = 'packaged_catalog.json';

// The only export columns read. The export has no SKU, size or THC/CBD columns: size, pack count and mg are parsed from Product Name.
// Inventory Room is used only to drop non-sellable rows and derive medicalOnly; the room string is not output.
const WHITELIST = ['Product Name', 'Category', 'Brand Name', 'Inventory Price', 'Strain Name', 'Inventory Room'];
const SELLABLE_ROOMS = ['Back of House', 'RECREATIONAL PRODUCT', 'MEDICAL PRODUCT']; // skipped: Quarantine, POS RETURN, SAMPLES/PROMOS
const ALLOW = ['importer', 'path', 'version', 'source', 'kind', 'md5', 'rows', 'deliCatalogMd5', 'counts', 'items', 'byCategory', 'skipped',
  'deliFlower', 'nonSellableRoom', 'zeroPrice', 'priceConflicts', 'id', 'name', 'brand', 'category', 'subcategory', 'sizeG', 'packCount',
  'thcMg', 'cbdMg', 'price', 'infused', 'medicalOnly', 'strainKey', 'limit', 'pool', 'grams', 'gap', 'storage',
  'PRE-PACK', 'PREROLL', 'VAPE', 'EDIBLE', 'EXTRACT', 'BEVERAGE', 'TOPICAL', 'MERCH'];

// Dutchie subcategory -> [DEC-034 category, DEC-050 storage]. An unmapped subcategory fails the run (never silently guessed).
// GAP storage = DEC-050 doesn't say (GAP-PKG-02). 'cooler' for BAKED GOOD reads "perishable edibles"; plain prerolls GAP, infused FOH.
const CATS = {
  'PRE-PACK': ['PRE-PACK', 'GAP'], 'Infused Flower': ['PRE-PACK', 'GAP'], 'Shake': ['PRE-PACK', 'GAP'],
  '1G PREROLL': ['PREROLL', 'GAP'], 'PREROLL PACK': ['PREROLL', 'GAP'], 'INFUSED Preroll': ['PREROLL', 'FOH'], 'INFUSED Preroll Pack': ['PREROLL', 'FOH'],
  'READY TO USE': ['VAPE', 'FOH'], '510 THREAD': ['VAPE', 'FOH'], 'POD': ['VAPE', 'FOH'],
  'EXTRACT': ['EXTRACT', 'cooler'], 'SHATTER': ['EXTRACT', 'cooler'], 'BADDER': ['EXTRACT', 'cooler'], 'LIVE RESIN SUGAR': ['EXTRACT', 'cooler'],
  'LIVE ROSIN': ['EXTRACT', 'cooler'], 'LIVE RESIN BADDER': ['EXTRACT', 'cooler'], 'SUGAR': ['EXTRACT', 'cooler'], 'SAUCE': ['EXTRACT', 'cooler'],
  'CRUMBLE': ['EXTRACT', 'cooler'], 'BUDDER': ['EXTRACT', 'cooler'], 'RSO': ['EXTRACT', 'cooler'],
  'GUMMY': ['EDIBLE', 'FOH'], 'CHEW': ['EDIBLE', 'FOH'], 'HARD CANDY': ['EDIBLE', 'FOH'], 'OTHER - EDIBLE (THC)': ['EDIBLE', 'FOH'],
  'SYRUP': ['EDIBLE', 'FOH'], 'DROPPER': ['EDIBLE', 'FOH'], 'SUBLINGUAL': ['EDIBLE', 'FOH'], 'BAKED GOOD': ['EDIBLE', 'cooler'], 'CHOCOLATE': ['EDIBLE', 'GAP'],
  'SODA': ['BEVERAGE', 'fridge'], 'SELTZER': ['BEVERAGE', 'fridge'], 'JUICE': ['BEVERAGE', 'fridge'], 'ELIXIR': ['BEVERAGE', 'fridge'],
  'BALM': ['TOPICAL', 'GAP'], 'SALVE': ['TOPICAL', 'GAP'], 'BATH SOAK': ['TOPICAL', 'GAP'], 'ROLL-ON': ['TOPICAL', 'GAP'], 'PATCH': ['TOPICAL', 'GAP'],
  'OTHER - CBD': ['TOPICAL', 'GAP'],
  'BATTERY': ['MERCH', 'GAP'], 'ROLLING PAPERS': ['MERCH', 'GAP'], 'ACCESSORY': ['MERCH', 'GAP'], 'PIPE': ['MERCH', 'GAP'], 'T SHIRT': ['MERCH', 'GAP'],
  'HAT': ['MERCH', 'GAP'], 'OTHER - MERCH': ['MERCH', 'GAP'],
};
const DELI = 'Bulk Flower'; // deli flower comes from the budtender tool (import_catalog.js), not this export
const STRAIN_CATS = ['PRE-PACK', 'PREROLL', 'VAPE', 'EXTRACT']; // SPEC_GAME004 §4: strainKey only where the engine profile applies

// DEC-048: 28 g flower / 5 g concentrate per transaction; an edible counts ~0.1 g. Anything DEC-048 doesn't state carries gap GAP-COMP-02.
function limitOf(cat, infused, sizeG) {
  const g = (pool, grams, gap = null) => ({ pool, grams, gap: grams == null ? 'GAP-COMP-02' : gap });
  switch (cat) {
    case 'PRE-PACK': case 'PREROLL': return g('flower', sizeG, infused ? 'GAP-COMP-02' : null); // infused: concentrate share unknown
    case 'VAPE': case 'EXTRACT': return g('concentrate', sizeG);
    case 'EDIBLE': case 'BEVERAGE': return g('concentrate', 0.1, 'GAP-COMP-02'); // 0.1 g is DEC-048; pool and per-package basis unconfirmed
    case 'TOPICAL': return g('GAP', null);
    case 'MERCH': return g('none', 0);
  }
}

function md5(buf) { return crypto.createHash('md5').update(buf).digest('hex'); }
const cleanText = s => String(s ?? '').replace(/[<>\u0000-\u001f]/g, '').replace(/\s+/g, ' ').trim();
// v7.11.4 L15434 normName (same as import_catalog.js)
const normName = n => n.toLowerCase().replace(/[^a-z0-9]/g, ' ').replace(/\s+/g, ' ').trim();
const num = (re, s) => { const m = s.match(re); return m ? Number(m[1]) : null; };

// Minimal .xlsx reader: zip central directory -> sharedStrings + sheet1. Returns rows as arrays of strings.
// shortcut: no zip64 / multi-sheet / CSV support; Dutchie's export is one small sheet. Add if a drop ever fails here.
function readXlsx(buf) {
  const eocd = buf.lastIndexOf(Buffer.from([0x50, 0x4b, 0x05, 0x06]));
  if (eocd < 0) throw new Error('not an .xlsx (zip) file');
  const files = {};
  for (let i = 0, n = buf.readUInt16LE(eocd + 10), p = buf.readUInt32LE(eocd + 16); i < n; i++) {
    const method = buf.readUInt16LE(p + 10), size = buf.readUInt32LE(p + 20), nl = buf.readUInt16LE(p + 28), off = buf.readUInt32LE(p + 42);
    const name = buf.toString('utf8', p + 46, p + 46 + nl), at = off + 30 + buf.readUInt16LE(off + 26) + buf.readUInt16LE(off + 28);
    const data = buf.subarray(at, at + size);
    files[name] = method === 8 ? zlib.inflateRawSync(data) : data;
    p += 46 + nl + buf.readUInt16LE(p + 30) + buf.readUInt16LE(p + 32);
  }
  if (!files['xl/worksheets/sheet1.xml']) throw new Error('xlsx has no sheet1');
  const dec = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(+d)).replace(/&amp;/g, '&');
  const texts = x => [...x.matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(m => m[1]).join('');
  const ss = files['xl/sharedStrings.xml'] ? [...files['xl/sharedStrings.xml'].toString('utf8').matchAll(/<si>([\s\S]*?)<\/si>/g)].map(m => dec(texts(m[1]))) : [];
  const col = r => [...r].reduce((n, c) => n * 26 + c.charCodeAt(0) - 64, 0) - 1;
  return [...files['xl/worksheets/sheet1.xml'].toString('utf8').matchAll(/<row[^>]*>([\s\S]*?)<\/row>/g)].map(m => {
    const r = [];
    for (const c of m[1].matchAll(/<c r="([A-Z]+)\d+"([^>]*?)(?:\/>|>([\s\S]*?)<\/c>)/g)) {
      const t = (c[2].match(/t="(\w+)"/) || [])[1], body = c[3] || '', v = (body.match(/<v>([\s\S]*?)<\/v>/) || [])[1];
      r[col(c[1])] = t === 's' ? ss[+v] : t === 'inlineStr' ? dec(texts(body)) : v == null ? '' : dec(v);
    }
    return Array.from(r, x => x ?? '');
  });
}

// Split the export into whitelisted records and the set of dropped-column text values (for the leak scan).
function load(file) {
  const buf = fs.readFileSync(file), rows = readXlsx(buf);
  // Some exports start with a preamble (export dates, location legal name): the header is the first row with 'Product Name'.
  const hi = rows.findIndex(r => r.map(cleanText).includes('Product Name')), header = (rows[hi] || []).map(cleanText);
  const missing = WHITELIST.filter(c => !header.includes(c));
  if (missing.length) throw new Error(`export is missing whitelisted column(s): ${missing.join(', ')}`);
  const keep = WHITELIST.map(c => header.indexOf(c)), body = rows.slice(hi + 1);
  const records = body.filter(r => r.some(x => x !== '')).map(r => Object.fromEntries(WHITELIST.map((c, i) => [c, cleanText(r[keep[i]])])));
  const kept = new Set(records.flatMap(Object.values).map(v => v.toLowerCase()));
  const dropped = new Set();
  const drop = v => { const s = cleanText(v).toLowerCase(); if (s.length >= 6 && !/^[\d.\-\/: ]+$/.test(s) && !kept.has(s)) dropped.add(s); }; // a value also in a kept column is already public
  rows.slice(0, hi).flat().forEach(drop);
  body.forEach(r => r.forEach((v, i) => { if (!keep.includes(i)) drop(v); }));
  // A dropped value that is a substring of kept text (e.g. a merch batch named after the product's colour) leaks nothing.
  for (const d of [...dropped]) for (const k of kept) if (k.includes(d)) { dropped.delete(d); break; }
  return { md5: md5(buf), rows: body.length, records, dropped };
}

function build(src, deliMd5, strains) {
  const skipped = { deliFlower: 0, nonSellableRoom: 0, zeroPrice: 0 };
  const byName = new Map();
  for (const r of src.records) {
    if (r.Category === DELI) { skipped.deliFlower++; continue; }
    if (!CATS[r.Category]) throw new Error(`unmapped Dutchie category "${r.Category}" (add it to CATS; DEC-047: ask the Hub if unclear)`);
    if (!SELLABLE_ROOMS.includes(r['Inventory Room'])) { skipped.nonSellableRoom++; continue; }
    const price = Number(r['Inventory Price']);
    if (!Number.isFinite(price) || price <= 0) { skipped.zeroPrice++; continue; }
    const key = r['Product Name'];
    if (!byName.has(key)) byName.set(key, []);
    byName.get(key).push({ ...r, price });
  }
  let priceConflicts = 0;
  const items = [], ids = new Set();
  for (const key of [...byName.keys()].sort()) {
    const rs = byName.get(key), r = rs[0], sub = r.Category, [category, storage] = CATS[sub];
    if (rs.some(x => x.Category !== sub)) throw new Error(`product listed under two categories: ${sub}`);
    // Modal shelf price across packages; tie -> lowest.
    const freq = {}; rs.forEach(x => freq[x.price] = (freq[x.price] || 0) + 1);
    const prices = Object.keys(freq).map(Number).sort((a, b) => freq[b] - freq[a] || a - b);
    if (prices.length > 1) priceConflicts++;
    const pipe = key.indexOf(' | '), name = pipe >= 0 ? key.slice(pipe + 3).trim() : key;
    const brand = r['Brand Name'] || (pipe >= 0 ? key.slice(0, pipe).trim() : '');
    const N = name.toUpperCase();
    // \d*\.?\d+ also reads leading-dot sizes (".5G" = 0.5, not 5; REVIEW-W4O).
    const sizeG = num(/(\d*\.?\d+)\s?G\b/, N), packCount = num(/(\d+)\s?PK\b/, N), totalMg = num(/(\d*\.?\d+)\s?MG\b/, N);
    let thcMg = num(/(\d*\.?\d+)\s?MG\s+THC/, N), cbdMg = num(/(\d*\.?\d+)\s?MG\s+CBD/, N);
    if (thcMg == null && cbdMg == null && totalMg != null) { if (/\bCBD\b/.test(N) && !/\bTHC\b/.test(N)) cbdMg = totalMg; else thcMg = totalMg; }
    const infused = /INFUSED/i.test(sub) || /\bINFUSED\b/.test(N) || sub === 'Infused Flower';
    const strainKey = STRAIN_CATS.includes(category) ? normName(r['Strain Name'].replace(/\s+-\s+.*$/, '')) : '';
    let id = (category + '-' + normName(brand + ' ' + name)).toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 72).replace(/-+$/, '');
    for (let n = 2; ids.has(id); n++) id = id.replace(/~\d+$/, '') + '~' + n;
    ids.add(id);
    items.push({ id, name, brand, category, subcategory: sub, sizeG, packCount, thcMg, cbdMg, price: prices[0], infused,
      medicalOnly: rs.every(x => x['Inventory Room'] === 'MEDICAL PRODUCT'), strainKey: strains.has(strainKey) ? strainKey : null,
      limit: limitOf(category, infused, sizeG), storage });
  }
  const byCategory = {};
  for (const c of ['PRE-PACK', 'PREROLL', 'VAPE', 'EDIBLE', 'EXTRACT', 'BEVERAGE', 'TOPICAL', 'MERCH']) byCategory[c] = items.filter(i => i.category === c).length;
  return {
    importer: { path: 'Tools/Data/import_packaged.js', version: IMPORTER_VERSION },
    source: { kind: 'dutchie-current-inventory', md5: src.md5, rows: src.rows, deliCatalogMd5: deliMd5 },
    counts: { items: items.length, byCategory, skipped, priceConflicts },
    items,
  };
}

// --- guards ---
function strings(o, out = []) {
  if (typeof o === 'string') out.push(o); else if (o && typeof o === 'object') Object.values(o).forEach(v => strings(v, out));
  return out;
}
function checkKeys(o, p = '$', bad = []) {
  if (Array.isArray(o)) o.forEach((x, i) => checkKeys(x, `${p}[${i}]`, bad));
  else if (o && typeof o === 'object') for (const k of Object.keys(o)) { if (!ALLOW.includes(k)) bad.push(`${p}.${k}`); checkKeys(o[k], `${p}.${k}`, bad); }
  return bad;
}
const PII = [
  ['email', /[\w.+-]+@[\w-]+\.[a-z]{2,}/i], ['phone', /\(?\b\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b/], ['ssn', /\b\d{3}-\d{2}-\d{4}\b/],
  ['date', /\b\d{1,2}\/\d{1,2}\/\d{2,4}\b|\b20\d\d-\d\d-\d\d\b/], ['honorific+name', /\b(Mr|Mrs|Ms|Miss)\.? [A-Z][a-z]+/],
  ['license/METRC-like id', /\b(?=[A-Z0-9]*\d)(?=[A-Z0-9]*[A-Z])[A-Z0-9]{10,}\b/i], ['person role word', /\b(patient|customer|employee|budtender|cashier)\b/i],
];
function guard(cat, dropped) {
  const bad = checkKeys(cat).map(k => `key not allow-listed: ${k}`);
  for (const s of strings(cat)) {
    for (const [what, re] of PII) if (re.test(s) && !/^[0-9a-f]{32}$/.test(s)) bad.push(`PII pattern (${what}): ${s.slice(0, 80)}`);
    if (dropped) { const l = s.toLowerCase(); for (const d of dropped) if (l.includes(d)) bad.push(`dropped-column value survived in: ${s.slice(0, 80)}`); }
  }
  if (bad.length) throw new Error('GUARD FAIL\n' + bad.slice(0, 50).join('\n'));
}

function selftest() {
  const ok = { importer: { path: 'x', version: '1' }, items: [{ id: 'a', name: 'GUMMIES 100MG', brand: 'B' }] };
  guard(ok, new Set(['secret vendor']));
  const leaks = [
    { items: [{ id: 'a', cost: 3 }] },                         // non-whitelisted field
    { items: [{ id: 'a', name: 'jo@example.com' }] },          // email
    { items: [{ id: 'a', name: 'call 602-555-0142' }] },       // phone
    { items: [{ id: 'a', name: '1A4060300003D1E000012345' }] }, // METRC tag
    { items: [{ id: 'a', name: 'via SECRET VENDOR llc' }] },   // dropped-column value
  ];
  for (const l of leaks) assert.throws(() => guard(l, new Set(['secret vendor'])), /GUARD FAIL/);
  assert.deepStrictEqual(limitOf('EDIBLE', false, null), { pool: 'concentrate', grams: 0.1, gap: 'GAP-COMP-02' });
  assert.strictEqual(limitOf('VAPE', false, null).gap, 'GAP-COMP-02');
  assert.deepStrictEqual(limitOf('EXTRACT', false, 1), { pool: 'concentrate', grams: 1, gap: null });
  assert.strictEqual(num(/(\d*\.?\d+)\s?G\b/, 'DAB PEN .75G'), 0.75);
  console.log('selftest OK');
}

function defaultExport() {
  const xlsx = d => fs.existsSync(d) ? fs.readdirSync(d).filter(f => /\.xlsx$/i.test(f)).sort() : [];
  const fresh = xlsx(DROP_DIR), dir = fresh.length ? DROP_DIR : ARCHIVE_DIR, xs = fresh.length ? fresh : xlsx(ARCHIVE_DIR);
  if (xs.length !== 1) throw new Error(`pass the export path, or put exactly one .xlsx in ${DROP_DIR} (found ${xs.length} in ${dir})`);
  return path.join(dir, xs[0]);
}

function main() {
  const args = process.argv.slice(2), file = args.find(a => !a.startsWith('--'));
  if (args.includes('--selftest')) return selftest();
  if (args.includes('--check')) {
    const cat = JSON.parse(fs.readFileSync(path.join(OUT, OUT_FILE), 'utf8'));
    let dropped = null;
    if (file) { const src = load(file); if (src.md5 !== cat.source.md5) throw new Error('export md5 differs from the one the output was built from'); dropped = src.dropped; }
    guard(cat, dropped);
    return console.log(`guard OK: ${OUT_FILE} (${cat.items.length} items${dropped ? ', dropped-value scan on' : ', no export given: dropped-value scan skipped'})`);
  }
  const src = load(file || defaultExport());
  const deliBuf = fs.readFileSync(path.join(OUT, 'batches.json'));
  const strains = new Set(JSON.parse(deliBuf.toString('utf8')).batches.map(b => normName(b.strainName)));
  const cat = build(src, md5(deliBuf), strains);
  guard(cat, src.dropped);
  const text = JSON.stringify(cat, null, 1) + '\n';
  fs.writeFileSync(path.join(OUT, OUT_FILE), text, 'utf8');
  console.log(JSON.stringify(cat.counts), 'md5', md5(Buffer.from(text, 'utf8')));
}

main();
