#!/usr/bin/env node
// Independent finite verifier for REFEREE326; does not import producer code.
const fs = require('fs');
const raw = JSON.parse(fs.readFileSync('results/raw/arc/lspv5_326/description_time_minimax_referee326.json', 'utf8'));
let assertions = 0;
const check = (x, msg) => { if (!x) throw new Error(msg); assertions++; };
const modelCount = mask => { let n = 0; for (let a = 0; a < 8; a++) if (((mask >> a) & 1) === 0) n++; return n; };
const label = x => Number(Number.isInteger(x) && x >= 1 && x <= 255 && modelCount(x) > 0);
const table = Array.from({length: 256}, (_, x) => label(x));
for (let x = 0; x < 256; x++) check(table[x] === label(x), `table mismatch ${x}`);
check(table.reduce((a, b) => a + b, 0) === 254, 'SAT count');
check(table[255] === 0, 'UNSAT full mask');
for (const x of [-3, -1, 256, 999, '1', 'p cnf', null, true, [], {}]) check(label(x) === 0, 'malformed accepted');
const corrupt = table.slice(); corrupt[255] = 1;
check(corrupt[255] !== label(255), 'corruption not detected');
check(raw.tiny_complete_clause_universe.valid_records === 255, 'raw valid count');
check(raw.tiny_complete_clause_universe.sat_records === 254, 'raw SAT count');
check(raw.k4_tseitin.odd_charge_models === 0, 'raw odd K4');
check(raw.k4_tseitin.even_charge_models === 8, 'raw even K4');
check(raw.accounting.correct_to_corrupt_table_offline_xor_popcount === 1, 'raw xor');
check(raw.accounting.d_phys === null, 'physical XOR must be unclaimed');
check(raw.status.B1_B2_B3_Rmix341 === 'OPEN', 'B bridges overstated');
check(raw.status.P_vs_NP === 'OPEN', 'P vs NP overstated');
console.log(JSON.stringify({verified: true, assertions, producer_assertions: raw.assertions}));
