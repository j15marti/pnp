#!/usr/bin/env node
// Independent arithmetic and coverage replay of the LSPV-5/406 raw ledger.
import fs from 'node:fs';
import crypto from 'node:crypto';

const path = 'results/raw/review/2026-11-07_0148_LSPV5_AFFINE_MULTISPLIT_RANK406.json';
const raw = fs.readFileSync(path, 'utf8');
const d = JSON.parse(raw);
const fail = m => { throw new Error(m); };
if (d.schema !== 'lspv5-affine-multisplit-rank-v1') fail('schema');
if (d.cases.length !== 6) fail('case count');
for (const c of d.cases) {
  if (c.branches !== 2 ** c.k) fail(`branches k=${c.k}`);
  if (c.q !== 3 * 2 ** c.k + c.k) fail(`q k=${c.k}`);
  if (c.unique_discharged_rows !== c.k + 1) fail(`rows k=${c.k}`);
  if (c.basis_rows.length !== c.k + 1) fail(`basis k=${c.k}`);
  if (c.extra_binary_joins !== c.k) fail(`joins k=${c.k}`);
  if (c.q_plus_k_bound !== c.q + c.k) fail(`bound k=${c.k}`);
  if (c.shared_non_source_tag !== 0 || !c.all_branches_excluded) fail(`sharing/coverage k=${c.k}`);
  let mask = 0, constant = 0;
  for (const r of c.basis_rows) { mask ^= r.mask; constant ^= r.const; }
  if (mask !== 0 || constant !== 1) fail(`basis contradiction k=${c.k}`);
  for (let bits = 0; bits < 2 ** c.k; bits++) {
    const violated = c.basis_rows.some(r => (((popcnt(r.mask & bits) & 1) ^ r.const) === 1));
    if (!violated) fail(`uncovered assignment k=${c.k} bits=${bits}`);
  }
}
for (const a of d.exhaustive_affine_cover_audit) {
  const rows = [];
  for (let mask=0; mask<2**a.k; mask++) for (const constant of [0,1]) rows.push({mask,constant});
  let covering=0, failures=0;
  for (let subset=0; subset<2**rows.length; subset++) {
    const chosen=[]; let cover=0;
    for (let i=0;i<rows.length;i++) if ((subset >> i) & 1) {
      chosen.push(rows[i]);
      for (let bits=0;bits<2**a.k;bits++) if (((popcnt(rows[i].mask & bits)&1)^rows[i].constant)===1) cover |= 2**bits;
    }
    if (cover === 2**(2**a.k)-1) {
      covering++;
      if (!spanOne(chosen,a.k)) failures++;
    }
  }
  if (a.affine_rows!==rows.length || a.subsets_checked!==2**rows.length || a.cube_covering_subsets!==covering || a.coverage_without_constant_one_span!==failures || failures!==0) fail(`exhaustive k=${a.k}`);
}
if (d.negative_controls.length !== 6 || d.negative_controls.some(x => !x.rejected)) fail('negative controls');
const names = new Set(d.negative_controls.map(x => x.name));
for (const n of ['omitted_AND_branch','duplicate_node_id','forged_row','cross_branch_reuse','branch_label_assumption_mismatch','forward_or_cyclic_dependency']) if (!names.has(n)) fail(`missing ${n}`);
const digest = crypto.createHash('sha256').update(raw).digest('hex');
console.log(JSON.stringify({status:'PASS',cases:d.cases.length,max_k:d.cases.at(-1).k,negative_controls:d.negative_controls.length,raw_sha256:digest,bytes:Buffer.byteLength(raw)}));

function popcnt(x) { let n=0; while (x) { x &= x-1; n++; } return n; }
function spanOne(rows,k) {
  const basis=Array(k+1).fill(0);
  for (const r of rows) {
    let x=r.mask | (r.constant<<k);
    while (x) { const p=31-Math.clz32(x); if (basis[p]) x^=basis[p]; else { basis[p]=x; break; } }
  }
  let x=1<<k;
  while (x) { const p=31-Math.clz32(x); if (basis[p]) x^=basis[p]; else return false; }
  return true;
}
