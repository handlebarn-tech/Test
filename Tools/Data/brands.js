#!/usr/bin/env node
// BRAND-001 (DEC-071): only the approved real brands ship. Shared by both importers; also a CLI check.
// The alias table is brand_aliases.json (importer input, never shipped). Brand is engine-neutral at v7.11.4: the tool reads it only in
// getEffectivePrices (brand pricing class + 'brand' deals), and the imported data has neither, so a 1:1 rename keeps output identical.
// Usage: node Tools/Data/brands.js --check     (fails if a non-approved real brand appears in shipped data or strings)
//        node Tools/Data/brands.js --selftest
'use strict';
const fs = require('fs'), path = require('path'), assert = require('assert'), { execFileSync } = require('child_process');

const ROOT = path.join(__dirname, '../..');
const TABLE = JSON.parse(fs.readFileSync(path.join(__dirname, 'brand_aliases.json'), 'utf8'));
const key = s => String(s).toUpperCase().replace(/[^A-Z0-9]/g, '');
const APPROVED = new Set(TABLE.approved.map(key));
const BY_KEY = new Map(TABLE.aliases.flatMap(a => a.real.map(r => [key(r), a])));
const FICTIONAL = new Set(TABLE.aliases.map(a => a.name));

// Whole-word, case-insensitive, any punctuation between words ("MOHAVE CANNABIS CO." = "Mohave Cannabis Co").
const wordRe = s => new RegExp('(?<![A-Za-z0-9])' + s.match(/[A-Za-z0-9]+/g).join('[^A-Za-z0-9]*') + '(?![A-Za-z0-9])', 'gi');
const caseLike = (m, s) => m === m.toUpperCase() ? s.toUpperCase() : s;
// [regex, replacement, label]. Common-word brands (text:false) are only checked in brand fields.
const TEXT_RULES = TABLE.aliases.flatMap(a => [
  ...(a.text === false ? [] : a.real.map(r => [wordRe(r), a.name, r])),
  ...Object.entries(a.lines || {}).map(([r, f]) => [wordRe(r), f, r]),
]);

/** Brand field -> shipped brand. Approved brands pass unchanged; an unknown non-approved brand throws (add it to brand_aliases.json). */
function aliasBrand(brand) {
  if (!brand || APPROVED.has(key(brand))) return brand;
  const a = BY_KEY.get(key(brand));
  if (!a) throw new Error(`BRAND-001: brand "${brand}" is not approved and has no alias in Tools/Data/brand_aliases.json`);
  return a.name;
}

/** Free text (item names) with real brand and product-line words swapped for the fictional ones. */
const scrubText = s => TEXT_RULES.reduce((t, [re, f]) => t.replace(re, m => caseLike(m, f)), s);

/** Real-brand words found in a string. */
const textHits = s => TEXT_RULES.filter(([re]) => (re.lastIndex = 0, re.test(s))).map(([, , r]) => r);

/** Problems in a parsed catalog: every brand field approved or fictional, no real brand words in any string. */
function guardCatalog(obj, file) {
  const bad = [];
  (function walk(o, p) {
    if (typeof o === 'string') { for (const r of textHits(o)) bad.push(`${file} ${p}: "${r}" in "${o.slice(0, 80)}"`); return; }
    if (!o || typeof o !== 'object') return;
    for (const [k, v] of Object.entries(o)) {
      if (k === 'brand' && typeof v === 'string' && v && !APPROVED.has(key(v)) && !FICTIONAL.has(v)) bad.push(`${file} ${p}.brand: "${v}" not approved`);
      walk(v, `${p}.${k}`);
    }
  })(obj, '$');
  return bad;
}

// Shipped text: everything tracked under the Unity project's _Game folder plus the PROC params/manifest that feed labels.
const SCAN = ['UnityProject/Assets/_Game', 'Tools/Blender/params', 'Art/Exports/Procedural/manifest.json'];
const TEXT_EXT = /\.(json|cs|uxml|uss|txt|csv|md|asset|prefab|unity|mat|shader|py)$/i;

function check() {
  const files = execFileSync('git', ['ls-files', '--', ...SCAN], { cwd: ROOT, encoding: 'utf8' }).split('\n').filter(f => TEXT_EXT.test(f));
  const bad = [];
  for (const f of files) {
    const text = fs.readFileSync(path.join(ROOT, f), 'utf8');
    if (/Data\/Catalog\/[^/]+\.json$/.test(f)) { bad.push(...guardCatalog(JSON.parse(text), f)); continue; }
    text.split('\n').forEach((line, i) => { for (const r of textHits(line)) bad.push(`${f}:${i + 1}: "${r}"`); });
  }
  if (bad.length) { console.error('BRAND CHECK FAIL (DEC-071)\n' + bad.slice(0, +process.env.BRAND_MAX || 60).join('\n') + (bad.length > (+process.env.BRAND_MAX || 60) ? `\n... ${bad.length} total` : '')); process.exit(1); }
  console.log(`brand check OK: ${files.length} files, ${TABLE.aliases.length} aliases, approved: ${TABLE.approved.join(', ')}`);
}

function selftest() {
  const names = TABLE.aliases.map(a => a.name);
  assert.strictEqual(new Set(names.map(key)).size, names.length, 'fictional names must be unique');
  for (const n of names) {
    assert.ok(!APPROVED.has(key(n)) && !BY_KEY.has(key(n)), `fictional "${n}" collides with a real brand`);
    assert.deepStrictEqual(textHits(n), [], `fictional "${n}" contains a real brand word`);
  }
  for (const a of TABLE.aliases) for (const f of Object.values(a.lines || {})) assert.deepStrictEqual(textHits(f), [], f);
  assert.strictEqual(aliasBrand('ToK'), 'ToK');
  assert.strictEqual(aliasBrand("DR. GREENTHUMB'S"), "DR. GREENTHUMB'S");
  assert.strictEqual(aliasBrand('MOHAVE CANNABIS CO.'), aliasBrand('Mohave Cannabis Co'));
  assert.throws(() => aliasBrand('Totally New Brand'), /BRAND-001/);
  assert.strictEqual(scrubText('HYPHEN FULL STOP ROSIN AIO 1G'), 'DASHWELL FULL STOP ROSIN AIO 1G');
  assert.strictEqual(scrubText('LIL LEAFERS 10PK'), 'LIL SPRIGLINE 10PK');
  assert.strictEqual(scrubText('ORANGE COOKIES 3.5G'), 'ORANGE COOKIES 3.5G'); // common-word brand: strain names untouched
  assert.ok(guardCatalog({ items: [{ brand: 'MADE', name: 'X' }] }, 't').length === 1);
  assert.ok(guardCatalog({ items: [{ brand: 'Wrought', name: 'STIIIZY POD' }] }, 't').length === 1);
  assert.deepStrictEqual(guardCatalog({ items: [{ brand: 'Wrought', name: 'POD 1G' }, { brand: 'ToK' }] }, 't'), []);
  console.log('selftest OK');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.includes('--selftest')) selftest();
  else if (args.includes('--check')) check();
  else console.log('usage: node Tools/Data/brands.js --check | --selftest');
}
module.exports = { aliasBrand, scrubText, guardCatalog };
