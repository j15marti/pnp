#!/usr/bin/env node
"use strict";
const fs = require("fs");
const d = JSON.parse(fs.readFileSync(
  "results/raw/arc/lspv5_331/proof_padding_firewall_referee331.json", "utf8"));
let checks = 0;
function ok(v, m) { if (!v) throw new Error(m); checks++; }
ok(d.artifact === "PROOF-PADDING-FIREWALL-REFEREE331", "artifact");
ok(d.rows.length === 11, "row count");
for (let i = 0; i < d.rows.length; i++) {
  const r = d.rows[i], n = 4 + i, ticks = 2 ** n;
  ok(r.source_bits === n, "source length");
  ok(r.explicit_tick_nodes === ticks, "tick nodes");
  ok(r.explicit_tick_payload_bytes === ticks, "unary bytes");
  ok(r.indexed_tick_upper_bytes === n * ticks, "indexed bytes");
  ok(r.stream_counter_bits === n + 1, "counter bits");
  ok(r.compact_run_integer_bits === n + 1, "macro integer bits");
  ok(r.unary_to_compact_payload_ratio_lower === ticks / (n + 1), "ratio");
}
ok(d.both_label_controls.length === 4, "both-label controls");
ok(d.both_label_controls.every(x => x.label === "SAT" && x.both_verifiers_reject), "SAT rejected");
ok(d.malformed_rejected === 8, "malformed");
ok(d.charged_ledger.unary_stream_peak.startsWith("O(N)"), "stream space");
ok(d.charged_ledger.compact_macro.includes("outside unary Pad grammar"), "macro grammar");
ok(d.classification.padded_system.B1.startsWith("false"), "Pad B1");
ok(d.classification.padded_system.B2.startsWith("false"), "Pad B2");
ok(d.classification.padded_system.B3.includes("equivalent"), "Pad B3");
ok(d.classification.open.includes("B3_Rmix341") && d.classification.open.includes("P!=NP"), "open status");
console.log(JSON.stringify({artifact: d.artifact, independent_checks: checks, pass: true}));
