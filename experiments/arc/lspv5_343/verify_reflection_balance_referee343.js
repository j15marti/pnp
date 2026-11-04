#!/usr/bin/env node
// Independent finite-control verifier for REFEREE343 raw summary.
const fs = require('fs');
const p = 'results/raw/arc/2026-11-04_1248_LSPV5_343_REFLECTION_BALANCE.json';
const x = JSON.parse(fs.readFileSync(p, 'utf8'));
let checks = 0;
function ok(v, msg) { checks++; if (!v) throw new Error(msg); }
ok(x.cnf_cases === 256, 'case count');
ok(x.sat_cases === 95, 'SAT count');
ok(x.unsat_cases === 161, 'UNSAT count');
ok(x.minimum_paid_nodes['1'] === 112, 'q=1');
ok(x.minimum_paid_nodes['2'] === 48, 'q=2');
ok(x.minimum_paid_nodes['3'] === 1, 'q=3');
ok(x.prefix_queries === 161 * 44, 'prefix-query count');
ok(x.fixed_proof_bits === 44, 'proof width');
ok(x.malformed_or_corrupt_rejected === 161 * 4, 'malformed controls');
ok(x.k4_tseitin_models.odd_charge === 0, 'odd K4');
ok(x.k4_tseitin_models.even_zero_charge === 8, 'even K4');
for (const r of x.reflection_quantifier_truth_table) {
  ok(r.B3 === r.forall_A_if_P_then_short_HA, 'universal B3 form');
  ok(r.exists_A_P_and_short_HA === (r.sat_in_p && r.wbar_poly), 'existential form');
}
for (const r of x.packed_payload_control) {
  ok(r.paid_nodes === 1, 'packed node');
  ok(r.payload_bits === 2 ** r.parameter_n, 'packed payload');
}
ok(/^[0-9a-f]{64}$/.test(x.cases_sha256), 'case digest');
console.log(JSON.stringify({status: 'PASS', checks}, null, 2));
