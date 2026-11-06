#!/usr/bin/env node
// Independent REFEREE384 verifier.  No producer code is imported.

import fs from 'node:fs';
import crypto from 'node:crypto';

const rawPath = 'results/raw/review/2026-11-06_0348_LSPV5_RECOVERY_NORMAL_FORM384.json';
const inputPath = 'results/raw/review/2026-11-06_0248_LSPV5_ORIGINAL_COORDINATE_RECOVERY383.json';
const outPath = 'results/raw/review/2026-11-06_0348_LSPV5_RECOVERY_NORMAL_FORM384_verify.json';
const expectedInputSha = '524f65bf4f033000ccaa675e14c870654eb758621d26cdb282f95b604b93df7b';

const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const inputBytes = fs.readFileSync(inputPath);
if (sha(inputBytes) !== expectedInputSha) throw new Error('input SHA mismatch');
const prior = JSON.parse(inputBytes.toString('utf8'));
const result = JSON.parse(fs.readFileSync(rawPath, 'utf8'));
let checks = 0;
const ok = (x, label) => { checks++; if (!x) throw new Error(label); };

const canon = xs => {
  const s = [...new Set(xs)].sort((a,b) => Math.abs(a)-Math.abs(b) || a-b);
  for (const x of s) if (s.includes(-x)) return null;
  return s;
};
const key = c => c.join(',');
const resolveAll = (a,b) => {
  const out = new Map();
  for (const p of a) if (b.includes(-p)) {
    const c = canon([...a.filter(x=>x!==p), ...b.filter(x=>x!==-p)]);
    if (c) out.set(key(c), c);
  }
  return [...out.values()];
};

function exactMin(sources, target, cutoff) {
  const src = sources.map(canon);
  const srcKeys = new Set(src.map(key));
  const targetKey = key(canon(target));
  let states = new Map([['', []]]);
  const counts = [];
  for (let d=1; d<=cutoff; d++) {
    const next = new Map();
    for (const derived of states.values()) {
      const clauses = [...src, ...derived];
      for (let i=0; i<clauses.length; i++) for (let j=i+1; j<clauses.length; j++) {
        for (const c of resolveAll(clauses[i], clauses[j])) {
          const ck = key(c);
          if (srcKeys.has(ck) || derived.some(x => key(x)===ck)) continue;
          if (ck === targetKey) { counts.push(next.size + 1); return {minimum:d, counts}; }
          const nd = [...derived, c].sort((x,y)=>key(x).localeCompare(key(y)));
          const sk = nd.map(key).join('|');
          if (!next.has(sk)) next.set(sk, nd);
        }
      }
    }
    counts.push(next.size);
    states = next;
  }
  return {minimum:null, counts};
}

ok(result.run === 'LSPV-5/REFEREE384', 'run id');
ok(result.input_trace_sha256 === expectedInputSha, 'recorded input sha');
ok(result.normal_form.work_theorem === 'W_recovery(K(F_h)) = 12h+2', 'work theorem');
ok(result.normal_form.global_warning.includes('globally only'), 'global scope warning');

const pads = [[-1,2,3],[-1,2,-3],[-1,-2,3],[-1,-2,-3]];
const pad = exactMin(pads, [-1], 3);
ok(pad.minimum === 3, 'pad min');

ok(result.canonical_block_searches.length === 8, 'eight sign patterns');
for (const item of result.canonical_block_searches) {
  const got = exactMin(item.sources, item.target, 5);
  ok(got.minimum === 5, 'block minimum');
  ok(JSON.stringify(got.counts.slice(0,4)) === JSON.stringify([9,56,316,1690]), 'block frontier counts');
  ok(item.equivalent_increment_after_shared_not_g === 2, 'shared increment');
}

ok(result.instances.length === prior.instances.length, 'instance count');
for (let i=0; i<result.instances.length; i++) {
  const x = result.instances[i], p = prior.instances[i], h=x.h;
  ok(x.graph === p.graph && h === p.h, 'instance identity');
  ok(x.exact_route_work === 12*h+2, 'work formula');
  ok(x.global_mixed_floor_only === 8*h+3, 'global floor');
  ok(x.route_phase_work.shared_not_g === 3, 'pad count');
  ok(x.route_phase_work.recover_original_clauses === 8*h, 'recovery count');
  ok(x.route_phase_work.and3_vertex_rows === 3*h, 'AND3 count');
  ok(x.route_phase_work.xor_all_rows === h-1, 'XOR count');
  ok(x.exact_route_span === 5 + Math.ceil(Math.log2(h)), 'span formula');

  const edges = p.edges.map(e => [e[0],e[1]]);
  let empty = [];
  for (let subset=1; subset < (1<<h); subset++) {
    let mask=0, rhs=0;
    for (let v=0; v<h; v++) if ((subset>>v)&1) {
      rhs ^= p.charges[v];
      for (let e=0; e<edges.length; e++) if (edges[e][0]===v || edges[e][1]===v) mask ^= (1<<e);
    }
    if (mask===0) empty.push([subset,rhs]);
  }
  ok(empty.length===1 && empty[0][0]===(1<<h)-1 && empty[0][1]===1, 'all rows necessary');
}

// Hostile controls must all be rejected by the assertions above.
const mutations = [
  x => x.run='wrong',
  x => x.input_trace_sha256='0'.repeat(64),
  x => x.normal_form.work_theorem='W=0',
  x => x.normal_form.global_warning='global optimum',
  x => x.canonical_block_searches.pop(),
  x => x.instances[0].exact_route_work--,
  x => x.instances[1].route_phase_work.and3_vertex_rows--,
  x => x.instances[2].global_mixed_floor_only++
];

function shallowAudit(x) {
  if (x.run !== 'LSPV-5/REFEREE384') return false;
  if (x.input_trace_sha256 !== expectedInputSha) return false;
  if (x.normal_form.work_theorem !== 'W_recovery(K(F_h)) = 12h+2') return false;
  if (!x.normal_form.global_warning.includes('globally only')) return false;
  if (x.canonical_block_searches.length !== 8) return false;
  for (const y of x.instances) {
    const h=y.h;
    if (y.exact_route_work !== 12*h+2) return false;
    if (y.global_mixed_floor_only !== 8*h+3) return false;
    if (y.route_phase_work.and3_vertex_rows !== 3*h) return false;
  }
  return true;
}
let rejected=0;
for (const mutate of mutations) {
  const x=structuredClone(result); mutate(x);
  if (!shallowAudit(x)) rejected++;
}
ok(rejected===mutations.length, 'all hostile mutations rejected');

const summary = {
  status:'PASS', checks, hostile_rejected:rejected,
  raw_sha256:sha(fs.readFileSync(rawPath)), input_sha256:sha(inputBytes),
  scope:'exact only for declared recovery normal form; global R_mix341 minimum and B3 open'
};
fs.writeFileSync(outPath, JSON.stringify(summary,null,2)+'\n');
console.log(JSON.stringify(summary));
