#!/usr/bin/env node
"use strict";

const fs = require("fs");
const d = JSON.parse(fs.readFileSync(
  "results/raw/arc/lspv5_329/end_to_end_sign_acquisition_referee329.json", "utf8"));
let checks = 0;
function ok(v, m) { if (!v) throw new Error(m); checks++; }

ok(d.artifact === "END-TO-END-SIGN-ACQUISITION-REFEREE329", "artifact");
ok(d.fixtures.length === 9, "fixtures");
ok(d.total_sign_flip_neighbors === 90, "neighbors");
for (const f of d.fixtures) {
  ok(f.base_models === 0, "base UNSAT");
  ok(f.neighbors === f.occurrence_signs, "neighbor count");
  ok(f.neighbor_model_counts.every(x => x === 1), "neighbor SAT");
}
ok(d.php_fixtures.length === 3, "PHP fixtures");
ok(d.php_sign_flip_neighbors === 70, "PHP neighbors");
for (const f of d.php_fixtures) {
  ok(f.base_models === 0, "PHP UNSAT");
  ok(f.neighbor_models_min > 0, "PHP neighbors SAT");
  ok(f.occurrence_signs === f.h * (f.h + 1) * (f.h + 1), "PHP L");
}
ok(d.strategies.length === 25, "strategies");
for (const s of d.strategies) {
  const frac = z => z.includes("/") ? z.split("/").map(Number) : [Number(z), 1];
  const [en, ed] = frac(s.epsilon), [pn, pd] = frac(s.read_all_probability);
  ok(pn * ed === (ed - 2 * en) * pd, "p=1-2e");
}
ok(d.packed_probe_controls.length === 12, "packed");
ok(d.representation.supplied_recoded_star_queries === 1, "recoded collapse");
ok(d.k4_models.odd === 0 && d.k4_models.even === 8, "K4 labels");
ok(d.malformed_rejected === 8, "malformed");
ok(d.classification.open.includes("B3") && d.classification.open.includes("P!=NP"), "open status");
console.log(JSON.stringify({artifact: d.artifact, independent_checks: checks, pass: true}));
