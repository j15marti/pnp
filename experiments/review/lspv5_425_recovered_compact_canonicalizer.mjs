// LSPV-5/425: canonical compression for the recovered SOURCE/AND3/XOR packet.
// Scope is exactly the preserved independent checker in replay/413.  This is
// not an authoritative historical R_mix341 parser and does not add rules.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const PACKET = path.join(ROOT, 'replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const CHECKER = path.join(ROOT, 'replay/413/lspv2_341_independent_verify.js');
const baselineRaw = fs.readFileSync(PACKET, 'utf8');
let checks = 0;
function assert(x, message) { checks++; if (!x) throw new Error(message); }
function sha(raw) { return crypto.createHash('sha256').update(raw).digest('hex'); }

function runChecker(raw) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-425-'));
  const file = path.join(dir, 'packet.json');
  fs.writeFileSync(file, raw);
  const cp = spawnSync(process.execPath, [CHECKER, file], {encoding:'utf8'});
  fs.rmSync(dir, {recursive:true, force:true});
  return {accepted: cp.status === 0, status: cp.status, stdout_sha256: sha(cp.stdout), stderr: cp.stderr.split('\n')[0] || ''};
}

function canonicalize(parsed) {
  if (!parsed || !Array.isArray(parsed.fixtures)) throw new Error('fixtures missing');
  const fixtures = parsed.fixtures.map((f) => {
    const V = f.graph.n;
    const E = f.graph.edges.length;
    const keep = (1n << BigInt(E)) - 1n;
    const ids = new Map(); // SameValueZero, exactly as the recovered checker.
    const put = (oldId, fresh) => {
      if (ids.has(oldId)) throw new Error('duplicate parsed identity');
      ids.set(oldId, fresh);
      return fresh;
    };
    const get = (oldId) => {
      if (!ids.has(oldId)) throw new Error('missing parsed identity');
      return ids.get(oldId);
    };
    const clauses = f.clauses.map((c, i) => ({
      id: put(c.id, `s${i}`), vertex: c.vertex, literals: [...c.literals]
    }));
    const row = (r) => ({mask: '0x' + (BigInt(r.mask) & keep).toString(16), rhs: r.rhs});
    const proof = f.proof.map((p, i) => {
      const out = {id: `d${i}`, kind: p.kind, rule: p.rule, parents: p.parents.map(get)};
      put(p.id, out.id);
      if (p.rule === 'AND3') {
        out.support = [...p.support];
        out.table = p.table;
        if (p.row) out.row = row(p.row);
      } else if (p.rule === 'XOR') {
        out.row = row(p.row);
      } else throw new Error('unknown rule');
      return out;
    });
    return {
      graph: {name: f.graph.name === 'BRIDGE_K4x2' ? 'BRIDGE_K4x2' : 'G', n: V, edges: f.graph.edges.map(e => [...e])},
      charges: [...f.charges],
      clauses,
      proof,
      deleted: f.deleted.map(d => ({sourceId: get(d.sourceId), assignment: d.assignment})),
      evenWitness: f.evenWitness,
      properties: {essential: f.properties.essential}
    };
  });
  return {fixtures, summary: fixtures.map(() => null)};
}

function canonicalRaw(raw) { return JSON.stringify(canonicalize(JSON.parse(raw))) + '\n'; }

const baseParsed = JSON.parse(baselineRaw);
const baseline = runChecker(baselineRaw);
assert(baseline.accepted, 'baseline rejected');
const baseCanonRaw = canonicalRaw(baselineRaw);
const baseCanon = runChecker(baseCanonRaw);
assert(baseCanon.accepted, 'canonical baseline rejected');

// Accepted parser-semantic variants: ignored metadata, paired affine ghosts,
// unsafe and lexical Number aliases, and duplicate JSON member last-wins.
const variants = [];
variants.push({name:'baseline', raw:baselineRaw});
const metadata = structuredClone(baseParsed);
metadata.version = 'X'.repeat(1 << 20);
metadata.definition = 'Y'.repeat(1 << 20);
metadata.summary = metadata.summary.map((_, i) => ({index:i, ignored:'Z'.repeat(4096)}));
metadata.unknown = 'U'.repeat(1 << 20);
variants.push({name:'ignored_metadata_3MiB', raw:JSON.stringify(metadata)});
const ghost = structuredClone(baseParsed);
const rows = ghost.fixtures[0].proof.filter(p => p.rule === 'AND3' && p.row);
for (const p of rows.slice(0,2)) p.row.mask = '0x' + (BigInt(p.row.mask) ^ (1n << 8192n)).toString(16);
variants.push({name:'paired_affine_ghost_8192', raw:JSON.stringify(ghost)});

const compact = JSON.stringify(baseParsed);
const unsafe = compact
  .replace('"id":"s0"', '"id":9007199254740992')
  .replace('"parents":["s0","s1"]', '"parents":[9007199254740993,"s1"]')
  .replace('"sourceId":"s0"', '"sourceId":9007199254740993');
variants.push({name:'unsafe_numeric_id_alias', raw:unsafe});
const lexical = compact
  .replace('"id":"s0"', '"id":1')
  .replace('"parents":["s0","s1"]', '"parents":[1e0,"s1"]')
  .replace('"sourceId":"s0"', '"sourceId":1.0');
variants.push({name:'safe_lexical_id_alias', raw:lexical});
const duplicate = compact.replace('"id":"s0"', '"id":"ignored-first","id":"s0"');
variants.push({name:'duplicate_member_last_wins', raw:duplicate});

const rowsOut = [];
for (const v of variants) {
  const before = runChecker(v.raw);
  assert(before.accepted, `${v.name}: input variant rejected`);
  const cr = canonicalRaw(v.raw);
  const after = runChecker(cr);
  assert(after.accepted, `${v.name}: canonical output rejected`);
  assert(sha(cr) === sha(baseCanonRaw), `${v.name}: canonical form differs`);
  rowsOut.push({name:v.name, input_bytes:Buffer.byteLength(v.raw), canonical_bytes:Buffer.byteLength(cr), input_sha256:sha(v.raw), canonical_sha256:sha(cr), accepted_before:true, accepted_after:true});
}

// Corruptions remain rejected after canonicalization (or canonicalization
// itself rejects a missing identity).
const corruptions = [];
for (const [name, mutate] of [
  ['sink_rhs', x => { x.fixtures[0].proof.at(-1).row.rhs ^= 1; }],
  ['bad_literal', x => { x.fixtures[0].clauses[0].literals[0] = 999; }],
  ['bad_table', x => { x.fixtures[0].proof[0].table ^= 1; }],
  ['missing_parent', x => { x.fixtures[0].proof[0].parents[0] = 'missing'; }]
]) {
  const x = structuredClone(baseParsed); mutate(x); const raw = JSON.stringify(x);
  const before = runChecker(raw);
  let canonRejected = false, after = {accepted:false};
  try { after = runChecker(canonicalRaw(raw)); canonRejected = !after.accepted; }
  catch { canonRejected = true; }
  assert(!before.accepted && canonRejected, `${name}: corruption survived`);
  corruptions.push({name, rejected_before:true, rejected_after_or_during:true});
}

const canonical = JSON.parse(baseCanonRaw);
const fixtureBounds = canonical.fixtures.map((f, i) => {
  const V=f.graph.n, E=f.graph.edges.length, W=f.proof.length;
  const bound=512*(V+1)*(E+W+1);
  const bytes=Buffer.byteLength(JSON.stringify({fixtures:[f],summary:[null]}));
  assert(bytes <= bound, `fixture ${i} conservative size bound`);
  return {index:i,V,E,W,canonical_bytes:bytes,conservative_bound:bound};
});

console.log(JSON.stringify({
  run:'LSPV-5/425',
  status:'PROVED-RESTRICTED recovered-sublanguage canonical compression; COMPUTATIONAL replay',
  checker:'replay/413/lspv2_341_independent_verify.js',
  checker_sha256:sha(fs.readFileSync(CHECKER)),
  packet:'replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',
  packet_sha256:sha(baselineRaw),
  checks,
  baseline_bytes:Buffer.byteLength(baselineRaw),
  canonical_bytes:Buffer.byteLength(baseCanonRaw),
  canonical_sha256:sha(baseCanonRaw),
  variants:rowsOut,
  corruptions,
  fixture_bounds:fixtureBounds,
  theorem:'Every accepted parsed packet in this fixed SOURCE/AND3/XOR schema has an accepted canonical packet with dense string IDs, projected E-bit affine masks, required fields only, and O(sum V(E+W+1)) bits; here W=4V-1.',
  limitations:['post-JSON-parse semantics only; duplicate raw members are last-wins','not authoritative historical parser','no RES/LOCAL-CONVERT/DEF/branching grammar','compactness does not prove B3 or construct proofs']
}, null, 2));
