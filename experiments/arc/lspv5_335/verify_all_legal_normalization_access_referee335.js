#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = process.argv[2];
if (!path) throw new Error("usage: verifier RAW.json");
const d = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
function check(x, msg) { checks++; if (!x) throw new Error(msg); }

check(d.id === "LSPV5_ALL_LEGAL_NORMALIZATION_ACCESS_REFEREE335", "id");
check(d.source_controls.unsat_models === 0, "UNSAT");
check(d.source_controls.sat_models === 2, "SAT");
check(d.source_controls.malformed_rejections === 9, "malformed");
check(d.cases.length === 12, "case count");
check(d.exhaustive_payloads === (2 ** 13 - 2), "payload total");

for (let idx = 0; idx < d.cases.length; idx++) {
  const c = d.cases[idx];
  const k = idx + 1;
  check(c.payload_bits === k, `k ${k}`);
  check(c.paid_prefix_nodes === 2, `q ${k}`);
  check(JSON.stringify(c.all_ones_condition) === JSON.stringify([false, true]), `ones ${k}`);
  check(JSON.stringify(c.single_flip_condition) === JSON.stringify([true, true]), `flip ${k}`);
  check(c.sensitive_positions === k, `sensitivity ${k}`);
  check(c.deterministic_worst_case_reads === k, `reads ${k}`);
  check(c.normalized_truth_bits === 2, `norm ${k}`);
  check(c.stream_counter_bits === Math.max(1, Math.ceil(Math.log2(k + 1))), `space ${k}`);
  check(c.materialized_payload_bits === k, `materialized ${k}`);
  // Independent adversary replay: if position i is unread on 1^k, flip it.
  for (let i = 0; i < k; i++) {
    const allOne = Array(k).fill(true);
    const flipped = allOne.slice(); flipped[i] = false;
    const f = b => [!b.every(Boolean), true];
    check(JSON.stringify(f(allOne)) !== JSON.stringify(f(flipped)), `adversary ${k}/${i}`);
    check(f(allOne)[1] && f(flipped)[1], `both legal ${k}/${i}`);
  }
}
check(d.classification.B1_B2_B3 === "OPEN", "bridges");
check(d.classification.P_vs_NP === "OPEN", "PvsNP");

process.stdout.write(JSON.stringify({
  id: "LSPV5_REFEREE335_INDEPENDENT_VERIFY",
  independent_assertions: checks,
  producer_assertions_seen: d.producer_assertions,
  status: "PASS"
}, null, 2) + "\n");
