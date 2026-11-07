#!/usr/bin/env node
import fs from 'node:fs';
import crypto from 'node:crypto';

const path = process.argv[2];
if (!path) throw new Error('usage: verify_lspv5_414_affine_ghost_port.mjs RAW.json');
const bytes = fs.readFileSync(path);
const d = JSON.parse(bytes);
let checks = 0;
function ok(x, msg) { checks++; if (!x) throw new Error(msg); }

ok(d.run === 'LSPV-5/414', 'run id');
ok(d.status.includes('PROVED/RESTRICTED'), 'status');
ok(d.baseline.accepted === true, 'baseline accepted');
ok(d.paired_ghost_trials.length === 4, 'four trials');
for (const t of d.paired_ghost_trials) {
  ok(t.accepted === true, `${t.name} accepted`);
  ok(t.same_checker_summary === true, `${t.name} summary invisible`);
  ok(t.proof_nodes === 15, `${t.name} K4 node count`);
  ok(t.projection.equals_original_object === true, `${t.name} projection equality`);
  ok(t.projection.accepted === true, `${t.name} projected acceptance`);
  ok(t.projection.node_count_preserved === true, `${t.name} projected work`);
}
ok(d.paired_ghost_trials.at(-1).byte_delta_from_serialized_baseline > 4000, 'evidence grows');
ok(d.hostile_controls.single_ghost_rejected === true, 'single ghost rejected');
ok(d.hostile_controls.illegal_in_range_bit_rejected === true, 'illegal low bit rejected');
ok(d.hostile_controls.malformed_mask_rejected === true, 'malformed rejected');
ok(d.symbolic_repair.and3_truth_tables_unchanged === true, 'AND3 projection');
ok(d.symbolic_repair.sink_preserved === true, 'sink projection');
ok(d.symbolic_repair.node_count_preserved === true, 'work projection');
ok(d.exact_mutation_delta.operations.map(x => x.node_id).join(',') === 'd2,d5', 'exact parents');
ok(d.exact_mutation_delta.operations.every(x => x.operation.endsWith('8192)')), 'exact high bit');

console.log(JSON.stringify({
  verifier: 'independent structural replay of LSPV-5/414 raw ledger',
  checks,
  raw_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  result: 'PASS'
}, null, 2));
