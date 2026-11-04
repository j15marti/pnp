#!/usr/bin/env node
// Independent finite verifier for REFEREE327; no producer import.
const fs = require('fs');
const raw = JSON.parse(fs.readFileSync('results/raw/arc/lspv5_327/uniform_generator_collapse_referee327.json', 'utf8'));
let assertions = 0;
const check = (v, m) => { if (!v) throw new Error(m); assertions++; };
const models = x => {
  if (!Number.isInteger(x) || x < 1 || x > 255) return 0;
  let c = 0; for (let a = 0; a < 8; a++) c += Number(((x >> a) & 1) === 0); return c;
};
const label = x => Number(Number.isInteger(x) && x >= 1 && x <= 255 && models(x) > 0);
const table = Array.from({length: 256}, (_, i) => label(i));
check(table.reduce((a,b) => a+b, 0) === 254, 'SAT total');
check(table[255] === 0, 'full-mask UNSAT');
for (let i = 0; i < 256; i++) check(table[i] === label(i), `label ${i}`);
for (const x of [-3, -1, 256, 999, '1', 'p cnf', null, true, [], {}]) check(label(x) === 0, 'malformed');
for (const h of raw.horizon_ledgers) {
  check(h.serialized_table_bits === h.cutoff + 1, 'serialization');
  check(h.prefix_correct === true, 'prefix status');
}
check(raw.normal_generation.delay_steps === 0, 'normal delay');
check(raw.delayed_generation.delay_steps === 10000, 'charged delay');
check(raw.tiny_language.corrupt_table_rejected === true, 'corrupt advice');
check(raw.k4_tseitin.odd_models === 0 && raw.k4_tseitin.even_models === 8, 'K4 parity');
check(raw.xor_offline.zero_to_correct_endpoint_delta === 254, 'endpoint delta');
check(raw.xor_offline.changed_then_restored_sum_adjacent_label_deltas === 256, 'restoration path');
check(raw.xor_offline.changed_then_restored_endpoint_delta === 254, 'restoration endpoint');
check(raw.xor_offline.delay_loop_data_bit_delta === 0, 'delay zero delta');
check(raw.xor_offline.d_phys === null, 'must not claim d_phys');
check(raw.status.B1_B2_B3_Rmix341 === 'OPEN', 'B bridge');
check(raw.status.P_vs_NP === 'OPEN', 'P vs NP');
console.log(JSON.stringify({verified: true, assertions, producer_assertions: raw.assertions}));
