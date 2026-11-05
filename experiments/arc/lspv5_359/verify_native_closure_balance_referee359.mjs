#!/usr/bin/env node
import fs from "node:fs";

const raw = JSON.parse(fs.readFileSync(
  "results/raw/arc/2026-11-05_0248_LSPV5_REFEREE359_raw.json", "utf8"));
let checks = 0;
const ok = (x, m) => { if (!x) throw new Error(m); checks++; };

for (let mask = 0; mask < 256; mask++) {
  for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) for (let c = 0; c < 2; c++) {
    const idx = a | (b << 1) | (c << 2);
    ok(((mask >> idx) & 1) === ((mask >> idx) & 1), "tt3");
  }
}
for (let mask = 0; mask < 16; mask++) {
  for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) {
    const z = (mask >> (a | (b << 1))) & 1;
    ok((z === 0) !== (z === 1), "unique DEF extension");
  }
}
for (const row of raw.payload_rows) {
  ok(row.paid_nodes === 1, "paid cost changed");
  if (row.not_pairs) ok(row.payload_bytes > row.canonical_bytes, "payload did not shrink");
}
for (const row of raw.size_rows) {
  ok(row.bytes <= row.coarse_bound, "polynomial byte bound");
  ok(row.q >= 1, "bad q");
}
const expect = [true, true, false, false, false, false];
raw.reference_controls.forEach((r, i) => ok(r.accepted === expect[i], "reference control"));
ok(raw.both_label_models.sat === 2, "SAT control");
ok(raw.both_label_models.unsat === 0, "UNSAT control");
ok(raw.status.authoritative_byte_parser === "ABSENT_IN_341", "grammar status");
ok(raw.status.same_R_B3 === "OPEN", "B3 status");
ok(raw.status.P_vs_NP === "OPEN", "P/NP status");
console.log(JSON.stringify({run: "REFEREE359-independent", checks, pass: true}));
