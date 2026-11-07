#!/usr/bin/env node
// Independent replay of the raw ledger's exact finite assertions.
import fs from 'node:fs';
import crypto from 'node:crypto';

const path = 'results/raw/review/2026-11-07_0048_LSPV5_CONTEXT_TYPED_UNION405.json';
const raw = fs.readFileSync(path, 'utf8');
const d = JSON.parse(raw);
const fail = (m) => { throw new Error(m); };
if (d.schema !== 'lspv5-context-typed-affine-union-v1') fail('schema');
if (d.valid_union.q_distinct_inference_vertices !== 7) fail('q');
if (d.valid_union.tags.W_shared !== 0) fail('shared tag');
if (d.valid_union.tags.F0 !== 1 || d.valid_union.tags.F1 !== 1) fail('terminal tags');
if (d.retraction.one_extra_join.mask !== 0 || d.retraction.one_extra_join.const !== 1) fail('join');
if (d.retraction.actual_common_source_refutation_inferences > d.retraction.q_plus_one_upper_bound) fail('bound');
const w = d.equal_label_distinct_context_witness;
if (w.node0.row.mask !== w.node1.row.mask || w.node0.row.const !== w.node1.row.const) fail('equal label');
if (JSON.stringify(w.node0.parents) === JSON.stringify(w.node1.parents)) fail('parents not distinct');
if (w.node0.scope === w.node1.scope) fail('scope not distinct');
if (d.negative_controls.length !== 6 || d.negative_controls.some(x => !x.rejected)) fail('negative controls');
const names = new Set(d.negative_controls.map(x => x.name));
for (const name of ['omitted_AND_branch','cross_branch_reuse','forged_row','duplicate_numeric_or_text_id','forward_edge_cycle_control','equal_row_illegal_merge']) {
  if (!names.has(name)) fail(`missing ${name}`);
}
const digest = crypto.createHash('sha256').update(raw).digest('hex');
console.log(JSON.stringify({status:'PASS', raw_sha256:digest, bytes:Buffer.byteLength(raw), q:d.valid_union.q_distinct_inference_vertices, negative_controls:d.negative_controls.length}));
